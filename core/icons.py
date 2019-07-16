import os
import shutil
import tempfile
import zipfile

import sublime

from ..common import settings
from ..common.utils import path
from ..common.utils import icons
from ..common.utils.logging import log, dump

from . import themes


def init():
    log("Initializing icons")

    try:
        general_path = path.overlay_patches_general_path()
        if os.path.isdir(general_path):
            dump("All the necessary icons are provided")
        else:
            _init_overlay(general_path)
        _copy_specific()
    except Exception as error:
        log("Error during copy")
        dump(error)


def _init_overlay(dest):
    """Create the icon overlay package.

    In order to make sure to override existing icons provided by the themes
    icons need to be copied to a package, which is loaded as late as possible.

    This function therefore creates a package named `zzz A File Icon zzz` and
    copies all icons over there.
    """
    # initializes path variables
    dest_multi = os.path.join(dest, "multi")
    dest_single = os.path.join(dest, "single")

    # copy icons from the loosen package folder
    src = path.package_icons_path()
    try:
        shutil.copytree(os.path.join(src, "single"), dest_single)
    except FileNotFoundError:
        os.makedirs(dest_single, exist_ok=True)

    try:
        shutil.copytree(os.path.join(src, "multi"), dest_multi)
    except FileNotFoundError:
        os.makedirs(dest_multi, exist_ok=True)

    # extract remaining icons from the package archive
    try:
        with zipfile.ZipFile(path.installed_package_path(), "r") as z:
            for m in z.namelist():
                if m.startswith("icons/single") or m.startswith("icons/multi"):
                    _, color, name = m.split("/")
                    try:
                        with open(os.path.join(dest, color, name), "xb") as f:
                            f.write(z.read(m))
                    except FileExistsError:
                        pass
    except FileNotFoundError:
        pass


def _copy_specific():
    log("Checking theme specific icons")

    customizable_themes = themes.get_customizable(themes.get_installed())
    general_path = path.overlay_patches_general_path()
    specific_path = path.overlay_patches_specific_path()

    src_multi = os.path.join(general_path, "multi")
    src_single = os.path.join(general_path, "single")

    multi_files = os.listdir(src_multi)
    single_files = os.listdir(src_single)

    for theme_package in customizable_themes:
        theme_patch_multi_path = path.makedirs(specific_path, theme_package, "multi")
        theme_patch_single_path = path.makedirs(specific_path, theme_package, "single")

        for icon in icons.get_missing(theme_package):
            dest = os.path.join(theme_patch_multi_path, icon + ".png")

            if not os.path.exists(dest):
                for filename in multi_files:
                    if filename.startswith(icon):
                        shutil.copy(
                            os.path.join(src_multi, filename),
                            theme_patch_multi_path
                        )

                for filename in single_files:
                    if filename.startswith(icon):
                        shutil.copy(
                            os.path.join(src_single, filename),
                            theme_patch_single_path
                        )

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


def _extract_general():
    log("Extracting general icons")

    try:
        general_path = path.overlay_patches_general_path()

        path.makedirs(general_path, "multi")
        path.makedirs(general_path, "single")

        with zipfile.ZipFile(path.installed_package_path(), "r") as z:
            for m in z.namelist():
                if m.startswith("icons/single") or m.startswith("icons/multi"):
                    _, color, name = m.split("/")
                    with open(os.path.join(general_path, color, name), "wb+") as f:
                        f.write(z.read(m))

    except Exception as error:
        log("Error during extract")
        dump(error)


def _copy_general():
    log("Copying general icons")

    package_path = path.package_icons_path()

    if os.path.exists(package_path):
        general_path = path.overlay_patches_general_path()

        src_multi = os.path.join(package_path, "multi")
        src_single = os.path.join(package_path, "single")

        dest_multi = os.path.join(general_path, "multi")
        dest_single = os.path.join(general_path, "single")

        try:
            shutil.copytree(src_multi, dest_multi)
            shutil.copytree(src_single, dest_single)
        except Exception as error:
            log("Error during copy")
            dump(error)
    else:
        _extract_general()


def _copy_specific():
    log("Checking theme specific icons")

    customizable_themes = themes.get_customizable(themes.get_installed())
    general_path = path.overlay_patches_general_path()
    specific_path = path.overlay_patches_specific_path()

    src_multi = os.path.join(general_path, "multi")
    src_single = os.path.join(general_path, "single")

    multi_files = os.listdir(src_multi)
    single_files = os.listdir(src_single)

    try:
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

    except Exception as error:
        log("Error during copy")
        dump(error)
    finally:
        sublime.run_command("afi_check_aliases")
        sublime.run_command("afi_patch_themes")


def provide():
    if settings.is_package_archive():
        _extract_general()
    else:
        _copy_general()

    _copy_specific()


def init():
    log("Initializing icons")

    if not os.path.exists(path.overlay_path()):
        sublime.set_timeout_async(provide, 0)
    else:
        sublime.set_timeout_async(_copy_specific, 0)
        dump("All the necessary icons are provided")

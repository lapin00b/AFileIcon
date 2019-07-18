import os
import sublime

from .. import settings


def makedirs(*args):
    absolute_path = os.path.join(*args)
    os.makedirs(absolute_path, exist_ok=True)
    return absolute_path


def installed_package_path():
    return os.path.join(
        sublime.installed_packages_path(), settings.PACKAGE_ARCH)


def package_icons_path():
    return os.path.join(
        sublime.packages_path(), settings.PACKAGE_NAME, "icons")


def overlay_path():
    return os.path.join(sublime.packages_path(), settings.OVERLAY_ROOT)


def overlay_cache_path():
    return os.path.join(sublime.cache_path(), settings.OVERLAY_ROOT)


def overlay_aliases_path():
    return os.path.join(
        sublime.packages_path(), settings.OVERLAY_ROOT, "aliases")


def overlay_patches_path():
    return os.path.join(
        sublime.packages_path(), settings.OVERLAY_ROOT, "patches")


def overlay_patches_general_path():
    return os.path.join(
        sublime.packages_path(), settings.OVERLAY_ROOT, "patches", "general")


def overlay_patches_specific_path():
    return os.path.join(
        sublime.packages_path(), settings.OVERLAY_ROOT, "patches", "specific")

import os
import sublime

PACKAGE_NAME, *_ = __package__.split(".", 1)
PACKAGE_MAIN = "plugin"
PACKAGE_ARCH = PACKAGE_NAME + ".sublime-package"

OVERLAY_ROOT = "{0} {1} {0}".format("zzz", PACKAGE_NAME)


def makedirs(*args):
    absolute_path = os.path.join(*args)
    os.makedirs(absolute_path, exist_ok=True)
    return absolute_path


def installed_package_path():
    return os.path.join(sublime.installed_packages_path(), PACKAGE_ARCH)


def package_icons_path():
    return os.path.join(sublime.packages_path(), PACKAGE_NAME, "icons")


def package_preferences_path():
    return os.path.join(sublime.packages_path(), PACKAGE_NAME, "preferences")


def overlay_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT)


def overlay_cache_path():
    return os.path.join(sublime.cache_path(), OVERLAY_ROOT)


def overlay_aliases_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "aliases")


def overlay_patches_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "patches")


def overlay_patches_general_path():
    return os.path.join(
        sublime.packages_path(), OVERLAY_ROOT, "patches", "general")


def overlay_patches_specific_path():
    return os.path.join(
        sublime.packages_path(), OVERLAY_ROOT, "patches", "specific")

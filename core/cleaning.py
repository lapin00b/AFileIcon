import shutil

import sublime

from . import settings

from .utils import path
from .utils.logging import log, dump, message


def clean_all():
    message("Cleaning up")

    def handler(function, path, excinfo):
        if handler.success:
            handler.success = False
            log("Error during cleaning")
        dump(path)

    handler.success = True

    shutil.rmtree(path.overlay_cache_path(), onerror=handler)
    shutil.rmtree(path.overlay_path(), onerror=handler)

    if handler.success:
        message("Cleaned up successfully")

    return handler.success


def revert():
    prefs = sublime.load_settings("Preferences.sublime-settings")
    ignored = prefs.get("ignored_packages", [])
    if path.OVERLAY_ROOT not in ignored:
        prefs.set("ignored_packages", ignored + [path.OVERLAY_ROOT])

    settings.clear_listener()

    try:
        clean_all()
    except Exception as error:
        dump(error)

    try:
        settings.add_listener()
    finally:
        prefs.set("ignored_packages", ignored)

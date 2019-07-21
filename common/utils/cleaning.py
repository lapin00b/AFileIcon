import shutil

import sublime
import sublime_plugin

from . import path

from .logging import log, dump, message
from .reloader import reload_plugin


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
    if clean_all():
        reload_plugin()


class AfiRevertCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(revert)

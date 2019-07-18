import os
import shutil

import sublime
import sublime_plugin

from . import path

from .logging import log, dump, message


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


def clean_theme_patches():
    log("Cleaning patches")

    success = True

    for dirname, _, files in os.walk(path.overlay_path()):
        for f in files:
            if f.endswith(".sublime-theme"):
                try:
                    os.remove(os.path.join(dirname, f))
                except Exception as error:
                    if success:
                        success = False
                        log("Error during cleaning")
                    dump(error)
    if success:
        log("Cleaned up successfully")
        sublime.run_command("afi_patch_themes")


def revert():
    if clean_all():
        sublime.run_command("afi_reload")


class AfiCleanCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(clean_theme_patches)


class AfiRevertCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(revert)

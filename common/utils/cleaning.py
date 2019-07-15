import os
import shutil

import sublime
import sublime_plugin

from . import path

from .logging import log, dump, message


def clean_all():
    message("Cleaning up")

    success = True

    def _on_rmtree_error(function, path, excinfo):
        if success:
            success = False
            log("Error during cleaning")
        dump(error)

    shutil.rmtree(path.overlay_cache_path(), onerror=_on_rmtree_error)
    shutil.rmtree(path.overlay_path(), onerror=_on_rmtree_error)

    if success:
        message("Cleaned up successfully")

    return success


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

import sublime
import sublime_plugin

if int(sublime.version()) >= 3114:

    def reload_modules():
        import imp
        import importlib
        import sys

        modules_load_order = [
            ".core.utils.colors",
            ".core.utils.logging",
            ".core.utils.path",
            ".core.utils.overlay",
            ".core.icons",
            ".core.themes",
            ".core.aliases",
            ".core.settings",
            ".core.cleaning"
        ]
        importlib.invalidate_caches()
        for module in modules_load_order:
            mod = sys.modules.get(__package__ + module)
            if mod:
                imp.reload(mod)

    # Note: Must be called before importing the core package in order to
    #       properly update all module references before usage!
    reload_modules()

    from .core.settings import add_listener, clear_listener
    from .core.cleaning import clean_all, revert
    from .core.utils.logging import log, dump

    def plugin_loaded():
        sublime.set_timeout_async(add_listener)

    def plugin_unloaded():
        is_upgrading = False
        was_removed = False

        clear_listener()

        try:
            from package_control import events
        except ImportError as error:
            log("It seems like you don't have Package Control installed")
            dump(error)
        else:
            is_upgrading = events.pre_upgrade(__package__)
            was_removed = events.remove(__package__)
        finally:
            if is_upgrading or was_removed:
                clean_all()

    class AfiRevertCommand(sublime_plugin.ApplicationCommand):
        def run(self):
            sublime.set_timeout_async(revert)

else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")

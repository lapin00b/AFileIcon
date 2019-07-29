import sublime

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

    from .core.cleaning import AfiRevertCommand, clean_all
    from .core.settings import add_listener, clear_listener
    from .core.utils.overlay import disable_overlay, enable_overlay

    def plugin_loaded():
        def plugin_loaded_async():
            add_listener()
            enable_overlay()
        sublime.set_timeout_async(plugin_loaded_async)

    def plugin_unloaded():
        is_upgrading = False
        was_removed = False

        clear_listener()

        try:
            from package_control import events
        except ImportError as error:
            pass
        else:
            is_upgrading = events.pre_upgrade(__package__)
            was_removed = events.remove(__package__)
        finally:
            if is_upgrading or was_removed:
                disable_overlay()
                try:
                    clean_all()
                finally:
                    if was_removed:
                        enable_overlay()
else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")

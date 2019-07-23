import sublime
import sublime_plugin

if int(sublime.version()) >= 3114:
    from .core.settings import add_listener, clear_listener
    from .core.cleaning import clean_all, revert
    from .core.utils.logging import log, dump
    from .core.utils.reloader import reload_plugin

    def plugin_loaded():
        was_upgraded = False

        try:
            from package_control import events
        except ImportError as error:
            log("It seems like you don't have Package Control installed")
            dump(error)
        else:
            was_upgraded = events.post_upgrade(__package__)
        finally:
            if was_upgraded:
                sublime.set_timeout_async(reload_plugin, 5000)
            else:
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

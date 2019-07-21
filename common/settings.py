import colorsys
import os
import re
import sublime

from .vendor import webcolors
from .utils.logging import log, dump, message
from .utils.path import PACKAGE_NAME

PACKAGE_SETTINGS_FILE = "A File Icon.sublime-settings"
SUBLIME_SETTINGS_FILE = "Preferences.sublime-settings"
PKGCTRL_SETTINGS_FILE = "Package Control.sublime-settings"

_current_settings = {}
_hsl_pattern = re.compile(r'hsl\(\s*(\d+),\s*(\d+)%,\s*(\d+)%\s*\)')
_uuid = "9ebcce78-4cac-4089-8bd7-d551c634b052"


def _package_settings_keys():
    try:
        return _package_settings_keys.cache
    except AttributeError:
        _package_settings_keys.cache = {
            key for key in sublime.decode_value(sublime.load_resource(
                "Packages/{0}/.sublime/{1}"
                .format(PACKAGE_NAME, PACKAGE_SETTINGS_FILE)
            )).keys() if key not in ("dev_mode", "dev_trace")
        }
        return _package_settings_keys.cache


def _merge(*settings):
    result = {}
    for dictionary in settings:
        result.update(dictionary)
    return result


def _parse_hsl_color(color):
    h, s, l = _hsl_pattern.match(color).groups()
    r, g, b = colorsys.hls_to_rgb(int(h) / 360, int(l) / 100, int(s) / 100)
    return [round(255 * r), round(255 * g), round(255 *b)]


def _get_colors(package_settings):
    colors = {}
    color_options = [
        key for key in _package_settings_keys() if key.startswith("color")
    ]

    if package_settings.get("color"):
        for opt in color_options:
            color = package_settings.get(opt)
            if isinstance(color, list):
                # color: [255, 255, 255]
                try:
                    colors[opt] = [int(color[0]), int(color[1]), int(color[2])]
                    continue
                except:
                    pass

            else:
                # color: hsl(360, 100%, 100%)
                try:
                    colors[opt] = _parse_hsl_color(color)
                    continue
                except:
                    pass

                # color: "white" or "#fff"
                try:
                    colors[opt] = webcolors.html5_parse_legacy_color(color)
                    continue
                except:
                    pass

            colors[opt] = []

    return colors


def _on_aliases_change():
    log("Aliases settings changed")
    sublime.run_command("afi_check_aliases")


def _on_icons_change():
    log("Icons settings changed")
    sublime.run_command("afi_patch_themes", {"overwrite": True})


def _on_force_mode_change():
    log("Force mode settings changed")
    sublime.run_command("afi_patch_themes")


def _on_change():
    is_aliases_changed = False
    is_icons_changed = False
    is_force_mode_changed = False

    global _current_settings
    real_settings = {}

    package_settings = package()

    for key in _package_settings_keys():
        real_settings[key] = package_settings.get(key)

        if real_settings[key] != _current_settings[key]:
            if key.startswith("aliases"):
                is_aliases_changed = True
            elif key.startswith("force_mode"):
                is_force_mode_changed = True
            else:
                is_icons_changed = True

    if is_aliases_changed:
        _on_aliases_change()

    if is_icons_changed:
        _on_icons_change()
    elif is_force_mode_changed:
        _on_force_mode_change()

    if is_aliases_changed or is_force_mode_changed or is_icons_changed:
        _current_settings = real_settings


def _update():
    global _current_settings

    for key in _package_settings_keys():
        _current_settings[key] = package().get(key)


def subltxt():
    try:
        return subltxt.cache
    except AttributeError:
        subltxt.cache = sublime.load_settings(SUBLIME_SETTINGS_FILE)
        return subltxt.cache


def pkgctrl():
    try:
        return pkgctrl.cache
    except AttributeError:
        pkgctrl.cache = sublime.load_settings(PKGCTRL_SETTINGS_FILE)
        return pkgctrl.cache


def package():
    try:
        return package.cache
    except AttributeError:
        package.cache = sublime.load_settings(PACKAGE_SETTINGS_FILE)
        return package.cache


def add_listener():
    package().add_on_change(_uuid, _on_change)


def clear_listener():
    package().clear_on_change(_uuid)


def icons():
    log("Getting settings of the icons")

    package_settings = package()

    s = _get_colors(package_settings)
    s["opacity"] = package_settings.get("opacity")
    s["opacity_on_hover"] = package_settings.get("opacity_on_hover")
    s["opacity_on_select"] = package_settings.get("opacity_on_select")
    s["size"] = package_settings.get("size")
    s["row_padding"] = package_settings.get("row_padding")
    dump(s)

    return s


def init():
    log("Initializing settings")
    _update()

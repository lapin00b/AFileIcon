import os
import json

from textwrap import dedent

import sublime
import sublime_plugin

from .common.utils import path
from .common.utils.logging import log, dump


def create_preferences(icons):
    log("Initializing preferences")

    template = dedent("""
        <?xml version="1.0" encoding="UTF-8"?>
        <plist version="1.0">
          <dict>
            <key>scope</key>
            <string>{scope}</string>
            <key>settings</key>
            <dict>
              <key>icon</key>
              <string>{name}</string>
            </dict>
          </dict>
        </plist>
        """).lstrip()

    success = True

    for name, data in icons.items():
        try:
            scopes = {
                syntax["scope"]
                for syntaxes in ("aliases", "syntaxes")
                for syntax in data.get(syntaxes, [])
            }
            if scopes:
                with open(os.path.join(
                        path.package_preferences_path(),
                        name + ".tmPreferences"),
                        "w") as out:
                    out.write(template.format(
                        name=name, scope=", ".join(sorted(scopes))))
        except Exception as error:
            if success:
                success = False
                log("Error during copy")
            dump(error)


class AfiBuildPreferencesCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        create_preferences(
            json.loads(sublime.load_resource(path.icons_json_path())))

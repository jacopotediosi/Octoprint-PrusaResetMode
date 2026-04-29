# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from flask import jsonify
from octoprint import __version__ as octoprint_version

# OctoPrint <2.0.0 uses "Send: " as log prefix
# OctoPrint >=2.0.0 uses ">>> " as log prefix
try:
    _OCTOPRINT_MAJOR = int(octoprint_version.split(".", 1)[0])
except (ValueError, AttributeError):
    _OCTOPRINT_MAJOR = 1
_SEND_LOG_PREFIX = ">>> " if _OCTOPRINT_MAJOR >= 2 else "Send: "


class PrusaResetModePlugin(
    octoprint.plugin.AssetPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SimpleApiPlugin
):
    def get_assets(self):
        return {"js": ["js/PrusaResetMode.js"], "css": ["css/PrusaResetMode.css"], "less": ["less/PrusaResetMode.less"]}

    def is_template_autoescaped(self):
        return True

    def get_api_commands(self):
        return dict(sendSemicolonCommand=["semicolonCommand"])

    def on_api_command(self, command, data):
        if command == "sendSemicolonCommand":
            semicolonCommand = data["semicolonCommand"]

            if not self._printer.is_ready():
                return jsonify({"error": "Printer is not ready"}), 503

            if semicolonCommand not in [";C32u2_FWV", ";C32u2_SNR", ";C32u2_RMD", ";C32u2_RME", ";C2560_RES"]:
                return jsonify({"error": "Semicolon command not allowed"}), 403

            transport = self._printer.get_transport()
            if transport is None:
                return jsonify(
                    {
                        "error": "Printer transport not available, please check you are connected to your Prusa via a serial connection"
                    }
                ), 503

            transport.write(semicolonCommand.encode() + b"\n")
            self._printer.log_lines(_SEND_LOG_PREFIX + semicolonCommand)
            return jsonify({"success": True}), 200

    def is_api_adminonly(self):
        return True

    def is_api_protected(self):
        return True

    def get_update_information(self):
        return {
            "PrusaResetMode": {
                "displayName": "PrusaResetMode Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "current": self._plugin_version,
                "user": "jacopotediosi",
                "repo": "OctoPrint-PrusaResetMode",
                "pip": "https://github.com/jacopotediosi/OctoPrint-PrusaResetMode/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Prusa Reset Mode"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = PrusaResetModePlugin()
__plugin_hooks__ = {"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information}

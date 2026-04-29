# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from flask import jsonify
from octoprint.util import comm as comm


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

            comm.MachineCom._do_send_without_checksum(self._printer._comm, semicolonCommand.encode())

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

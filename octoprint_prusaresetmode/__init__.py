# coding=utf-8
from __future__ import absolute_import

from flask import jsonify, request, make_response
from werkzeug.exceptions import BadRequest

from octoprint.util import comm as comm

from octoprint.server.util import has_permissions
from octoprint.access.permissions import Permissions

import octoprint.plugin


class PrusaResetModePlugin(octoprint.plugin.AssetPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SimpleApiPlugin):
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/PrusaResetMode.js"],
            "css": ["css/PrusaResetMode.css"],
            "less": ["less/PrusaResetMode.less"]
        }

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "PrusaResetMode": {
                "displayName": "PrusaResetMode Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jacopotediosi",
                "repo": "OctoPrint-PrusaResetMode",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jacopotediosi/OctoPrint-PrusaResetMode/archive/{target_version}.zip",
            }
        }

    def get_api_commands(self):
        return dict(
            sendSemicolonCommand=["semicolonCommand"]
        )

    def on_api_command(self, command, data):
        if command == "sendSemicolonCommand":
            semicolonCommand = data["semicolonCommand"]

            if not self._printer.is_ready():
                return jsonify({"error": "Printer is not ready"}), 503

            if semicolonCommand not in [';C32u2_FWV', ';C32u2_SNR', ';C32u2_RMD', ';C32u2_RME', ';C2560_RES']:
                return jsonify({"error": "Semicolon command not allowed"}), 403

            comm.MachineCom._do_send_without_checksum(
                self._printer._comm, semicolonCommand.encode())

            return jsonify({"success": True}), 200

    def is_api_adminonly(self):
        return True


__plugin_name__ = "Prusa Reset Mode"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrusaResetModePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

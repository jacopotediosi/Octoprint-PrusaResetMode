/*
 * View model for OctoPrint-PrusaResetMode
 *
 * Author: Jacopo Tediosi
 * License: AGPLv3
 */

/* global $, ko, _, OctoPrint, OCTOPRINT_VIEWMODELS, PNotify */
/* eslint camelcase: "off" */

$(function () {
  function PrusaResetModeViewModel (parameters) {
    const self = this

    self.loginState = parameters[0]
    self.settings = parameters[1]
    self.access = parameters[2]

    self.pluginIdentifier = 'PrusaResetMode'

    self.isReady = ko.observable(undefined)

    self.fromCurrentData = function (data) {
      self._processStateData(data.state)
    }

    self.fromHistoryData = function (data) {
      self._processStateData(data.state)
    }

    self._processStateData = function (data) {
      self.isReady(data.flags.ready)
    }

    self.sendSemicolonCommand = function (semicolonCommand) {
      OctoPrint.simpleApiCommand(self.pluginIdentifier, 'sendSemicolonCommand', { semicolonCommand })
        .done(function (response) {
          // eslint-disable-next-line no-new
          new PNotify({
            title: _.escape(self.pluginName),
            text: 'Semicolon command sent successfully.\r\nPlease check Terminal for outputs.',
            type: 'success'
          })
        })
        .fail(function (response) {
          // eslint-disable-next-line no-new
          new PNotify({
            title: _.escape(self.pluginName),
            text: 'Error sending semicolon command!',
            type: 'error'
          })
        })
    }
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: PrusaResetModeViewModel,
    // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
    dependencies: ['loginStateViewModel', 'settingsViewModel', 'accessViewModel'],
    // Elements to bind to, e.g. #settings_plugin_PrusaResetMode, #tab_plugin_PrusaResetMode, ...
    elements: ['#tab_plugin_PrusaResetMode']
  })
})

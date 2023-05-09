# SPDX-License-Identifier: Apache-2.0

from omni.kit.window.preferences import PreferenceBuilder
from omni.kit.widget.settings.settings_widget import SettingType
import omni.ui as ui

from . import constants as c

class SaveReminderPreferences(PreferenceBuilder):
    def __init__(self):
        super().__init__("Reminders")

    def build(self):
        with ui.VStack(height=0, spacing=5):
            with self.add_frame("Save Reminder"):
                with ui.VStack():
                    # TODO: Is "min" a valid kwarg?
                    self.create_setting_widget(
                        "Enable Save Reminder", c.SAVE_ENABLED_SETTING, SettingType.BOOL, min=0
                    )
                    self.create_setting_widget(
                        "Save Reminder Interval (seconds)", c.SAVE_INTERVAL_SETTING, SettingType.INT, min=0
                    )
                    self.create_setting_widget(
                        "Save Reminder Message", c.SAVE_MESSAGE_SETTING, SettingType.STRING, min=0
                    )
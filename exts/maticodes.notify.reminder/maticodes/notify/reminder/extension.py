# SPDX-License-Identifier: Apache-2.0

import asyncio

import carb
import carb.settings
import omni.ext
import omni.kit.app
import omni.kit.notification_manager as nm
import omni.kit.window.preferences
import omni.usd

from . import constants as c
from .preferences import SaveReminderPreferences


class MaticodesNotifyReminderExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[maticodes.notify.reminder] maticodes notify reminder startup")
        self.settings = carb.settings.get_settings()
        self.settings.set_default(c.SAVE_ENABLED_SETTING, True)
        self.settings.set_default(c.SAVE_INTERVAL_SETTING, c.DEFAULT_SAVE_INTERVAL)
        self.settings.set_default(c.SAVE_MESSAGE_SETTING, c.DEFAULT_SAVE_MESSAGE)
        self._preferences_page = omni.kit.window.preferences.register_page(SaveReminderPreferences())
        self.bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self.save_fired_sub = self.bus.create_subscription_to_push_by_type(c.SAVE_REMINDER_FIRED, self.on_save_reminder)
        asyncio.ensure_future(self.reminder_timer())

    def on_save_reminder(self, e: carb.events.IEvent):
        if self.settings.get_as_bool(c.SAVE_ENABLED_SETTING):
            message = self.settings.get(c.SAVE_MESSAGE_SETTING)
            ok_button = nm.NotificationButtonInfo("SAVE", on_complete=self.do_save)
            cancel_button = nm.NotificationButtonInfo("CANCEL", on_complete=None)
            notification = nm.post_notification(
                message, hide_after_timeout=False, duration=0,
                status=nm.NotificationStatus.WARNING, button_infos=[ok_button, cancel_button])
            asyncio.ensure_future(self.reminder_timer())

    def do_save(self):
        def save_finished(arg1, arg2, saved_files):
            if not saved_files:
                carb.log_error("No files saved! Are you working in an untitled stage?")
            else:
                carb.log_info(f"Saved the files: {saved_files}")
        omni.usd.get_context().save_stage_with_callback(save_finished)

    async def reminder_timer(self):
        await asyncio.sleep(self.settings.get(c.SAVE_INTERVAL_SETTING))
        if hasattr(self, "bus"):
            self.bus.push(c.SAVE_REMINDER_FIRED)

    def on_shutdown(self):
        print("[maticodes.notify.reminder] maticodes notify reminder shutdown")
        self.save_fired_sub = None
        omni.kit.window.preferences.unregister_page(self._preferences_page)
        self._preferences_page = None

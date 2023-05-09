# SPDX-License-Identifier: Apache-2.0

import carb

SAVE_REMINDER_FIRED = carb.events.type_from_string("maticodes.notify.reminder.SAVE_REMINDER_FIRED")
SAVE_INTERVAL_SETTING = "/persistent/exts/maticodes.notify.reminder/save/interval"
SAVE_ENABLED_SETTING = "/persistent/exts/maticodes.notify.reminder/save/enabled"
SAVE_MESSAGE_SETTING = "/persistent/exts/maticodes.notify.reminder/save/message"

DEFAULT_SAVE_INTERVAL = 600
DEFAULT_SAVE_MESSAGE = "Hey! Don't forget to save!"

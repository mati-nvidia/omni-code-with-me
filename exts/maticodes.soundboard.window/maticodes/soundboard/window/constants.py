# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import carb

REORDER_EVENT = carb.events.type_from_string("maticodes.soundboard.window.BUTTONS_REORDERED")
SOUNDS_CHANGED_EVENT = carb.events.type_from_string("maticodes.soundboard.window.SOUNDS_CHANGED")

DATA_DIR = Path("${omni_data}/exts/maticodes.soundboard.window")
USER_CONFIG_PATH = DATA_DIR / "user.config"
GUTTER_WIDTH = 24
EDIT_BAR_HEIGHT = 110

DEFAULT_BUTTON_COLOR = (0.15, 0.15, 0.15)

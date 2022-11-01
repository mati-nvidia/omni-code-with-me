# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import carb

REORDER_EVENT = carb.events.type_from_string("maticodes.soundboard.BUTTONS_REORDERED")

DATA_DIR = Path("${omni_data}/exts/maticodes.soundboard")
USER_CONFIG_PATH = DATA_DIR / "user.config"
GUTTER_WIDTH = 32
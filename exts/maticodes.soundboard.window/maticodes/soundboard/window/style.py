# SPDX-License-Identifier: Apache-2.0

import omni.ui as ui

slot_style = {
    "ColorWidget": {
        "margin_height": 5
    },
    "Rectangle::edit_bar": {
        "background_color": ui.color(.04),
        "border_radius": 7
    }
}

def get_button_style(color):
    return {
        "": {
            "background_color": ui.color(*[c * 0.5 for c in color]),
            "background_gradient_color": ui.color(*color)
        },
        ":hovered": {
            "background_color": ui.color(*[c * 0.75 for c in color]),
            "background_gradient_color": ui.color(*[c * 1.1 for c in color]),
        },
    }
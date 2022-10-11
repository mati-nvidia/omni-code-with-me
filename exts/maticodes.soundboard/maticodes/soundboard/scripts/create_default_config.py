import json
from pathlib import Path

config_path = Path(__file__).parent.parent.parent.parent / "data" / "default_config.json"

sounds = {
    "Applause": {
        "uri": "data/sounds/applause.wav"
    },
    "Door Bell": {
        "uri": "data/sounds/door_bell.wav"
    },
    "Door Bell": {
        "uri": "data/sounds/door_bell.wav"
    },
    "Crowd Laughing": {
        "uri": "data/sounds/laugh_crowd.mp3"
    },
    "Crowd Sarcastic Laughing": {
        "uri": "data/sounds/laugh_crowd_sarcastic.wav"
    },
    "Level Complete": {
        "uri": "data/sounds/level_complete.wav"
    },
    "Ooooh Yeah": {
        "uri": "data/sounds/oh_yeah.wav"
    },
    "Pew Pew": {
        "uri": "data/sounds/pew_pew.wav"
    },
    "Phone Ringing 1": {
        "uri": "data/sounds/phone_ring_analog.wav"
    },
    "Phone Ringing 2": {
        "uri": "data/sounds/phone_ringing_digital.wav"
    },
    "Rooster Crowing": {
        "uri": "data/sounds/rooster_crowing.wav"
    },
    "Thank you": {
        "uri": "data/sounds/thank_you.wav"
    },
    "Timer": {
        "uri": "data/sounds/timer.wav"
    },
    "Woohoo": {
        "uri": "data/sounds/woohoo.wav"
    },
    "Yes Scream": {
        "uri": "data/sounds/yes_scream.wav"
    },
}

config = {
    "active_sounds": [key for key in sounds],
    "sounds_repo": sounds
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=4)
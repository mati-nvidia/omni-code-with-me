## TODO
- Make a button play a sound
- Create a JSON and read from it for the default config.
- Create multiple buttons from config
- Create button size setting
- Allow user sounds
    - Copy files to data dir
- Merge user config with default config
- Allow removing buttons
- Allow adding buttons from sounds palette
- Allow button reordering
- Allow custom colors
- Edit mode vs perform mode

```
{
    "active_sounds": ["Sound 1", "Sound 2"],
    "sounds_repo": {
        "Sound 1": {
            # default config uses token paths
            # user config uses absolute paths
            "uri": "/some/file/path.wav"
            "color": [1.0, 1.0, 1.0]
        },
        ...
    }
}
```

```
class ConfigManager:
    resolved_config = {}

    @staticmethod
    def load_config():
        pass
    


```

```
class SoundSlot:

```

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
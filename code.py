print("Starting")

import board
import time

time.sleep(3)

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.layers import Layers as _Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.extensions.RGB import RGB
from midi import Midi


# KEYTBOARD SETUP
keyboard = KMKKeyboard()
encoders = EncoderHandler()
tapdance = TapDance()
tapdance.tap_time = 250
keyboard.modules = [encoders, tapdance]

# SWITCH MATRIX
keyboard.col_pins = (board.D3, board.D4, board.D5, board.D6)
keyboard.row_pins = (board.D7, board.D8, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ENCODERS
encoders.pins = ((board.A2, board.A1, board.A0, False), (board.SCK, board.MISO, board.MOSI, False),)

# EXTENSIONS
rgb_ext = RGB(pixel_pin = board.D10, num_pixels=4, hue_default=150)
midi_ext = Midi()
keyboard.extensions.append(rgb_ext)
keyboard.extensions.append(midi_ext)
keyboard.debug_enabled = False


# class Layers(_Layers):
#    last_top_layer = 0
#    hues = (4, 20, 69)
#
#    def after_hid_send(keyboard):
#        if keyboard.active_layers[0] != self.last_top_layer:
#            self.last_top_layer = keyboard.active_layers[0]
#            rgb_ext.set_hsv_fill(self.hues[self.last_top_layer], 255, 255)

layers = _Layers()
keyboard.modules.append(layers)

# MACROS BOTTOM ROW
GMAIL = simple_key_sequence([KC.LWIN(KC.R), KC.MACRO_SLEEP_MS(250), send_string('firefox www.gmail.com'), KC.ENTER])
YTTV = simple_key_sequence([KC.LWIN(KC.R), KC.MACRO_SLEEP_MS(250), send_string('firefox https://tv.youtube.com'), KC.ENTER])
YOUTUBE = simple_key_sequence([KC.LWIN(KC.R), KC.MACRO_SLEEP_MS(250), send_string('firefox www.youtube.com'), KC.ENTER])
REDDIT = simple_key_sequence([KC.LWIN(KC.R), KC.MACRO_SLEEP_MS(250), send_string('firefox https://old.reddit.com'), KC.ENTER])

# MACROS MIDDLE ROW
PREVIOUS_TRACK = KC.MPRV
PLAY_PAUSE = KC.MPLY
NEXT_TRACK = KC.MNXT
NICE = simple_key_sequence([KC.LCTRL(KC.F14)])


# MACROS TOP ROW
VOICEMEETER_RESTART = simple_key_sequence([KC.LCTRL(KC.F13)])
MUTE_DISCORD = simple_key_sequence([KC.LALT(KC.M)])
DEAFEN_DISCORD = simple_key_sequence([KC.LALT(KC.D)])
LOCK = simple_key_sequence([KC.LWIN(KC.L)])

CUT_THAT = simple_key_sequence([KC.LCTRL(KC.F15)])
NICE_SHOT = simple_key_sequence([KC.LCTRL(KC.F16)])
BAD_SHOT = simple_key_sequence([KC.LCTRL(KC.F17)])
TOWEL = simple_key_sequence([KC.LCTRL(KC.F18)])

_______ = KC.TRNS
xxxxxxx = KC.NO

# LAYER SWITCHING TAP DANCE
TD_LYRS = KC.TD(LOCK, KC.MO(1), KC.TO(3), KC.TO(2))
MIDI_OUT = KC.TD(KC.MIDI(71), xxxxxxx, xxxxxxx, KC.TO(0))
SOUND_BOARD_OUT = KC.TD(NICE_SHOT, xxxxxxx, xxxxxxx, KC.TO(0))

# array of default MIDI notes
# midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]

# KEYMAPS

keyboard.keymap = [
    # MACROS
    [
        VOICEMEETER_RESTART,   MUTE_DISCORD,     DEAFEN_DISCORD,    TD_LYRS,
        PREVIOUS_TRACK,    PLAY_PAUSE,          NEXT_TRACK,    NICE,
        GMAIL,    YTTV,       YOUTUBE,     REDDIT,
    ],
    # RGB CTL
    [
        xxxxxxx,    xxxxxxx,            xxxxxxx,                xxxxxxx,
        xxxxxxx,    KC.RGB_MODE_SWIRL,  KC.RGB_MODE_KNIGHT,     KC.RGB_MODE_BREATHE_RAINBOW,
        xxxxxxx,    KC.RGB_MODE_PLAIN,  KC.RGB_MODE_BREATHE,    KC.RGB_MODE_RAINBOW,
    ],
    # Sound Board
    [
        VOICEMEETER_RESTART, NICE, CUT_THAT, SOUND_BOARD_OUT,
        BAD_SHOT, TOWEL,  xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx,
    ],
    # MIDI
    [
        KC.MIDI(68),    KC.MIDI(69),      KC.MIDI(70),       MIDI_OUT,
        KC.MIDI(64),    KC.MIDI(65),      KC.MIDI(66),       KC.MIDI(67),
        KC.MIDI(60),    KC.MIDI(61),      KC.MIDI(62),       KC.MIDI(63),
    ],
]

encoders.map = [    ((KC.VOLU, KC.VOLD, KC.MUTE),           (KC.RGB_VAI,    KC.RGB_VAD,     KC.RGB_TOG)),   # MACROS
                    ((KC.RGB_ANI, KC.RGB_AND, xxxxxxx),     (KC.RGB_HUI,    KC.RGB_HUD,     _______   )),   # RGB CTL
                    ((KC.VOLU, KC.VOLD, KC.MUTE),           (KC.RGB_VAI,    KC.RGB_VAD,     KC.RGB_TOG)),   # MIDI
               ]


if __name__ == '__main__':
    keyboard.go()

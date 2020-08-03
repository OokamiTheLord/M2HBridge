import rtmidi

# from HUI import HUI_display_AA
import Logic
import time

midi_out = rtmidi.MidiOut()
midi_in = rtmidi.MidiIn()

midi_out.open_port(1    )
midi_out.open
midi_in.open_port(8)
midi_in.ignore_types(sysex=False)

# HUI_display_AA(midi_out)
# Logic.initiate_connection(midi_in, midi_out)
# for i in range(8):
#     Logic.send_fader(midi_out, i, 0x7f, 0x7f)

import consts

# for i in range(16):
#     midi_out.send_message([0xB0 + i, 0x7A, 0x00])
# for i in range(8):
#     midi_out.send_message(consts.hdr + [0x00, 0x20, i, 1] + consts.end)
# for i in range(8):
#     midi_out.send_message(consts.hdr + [0x00, 0x20, i, 1] + consts.end)

midi_out.send_message([0xE0, 0x7F, 0x3F])

print("now")
time.sleep(1)

# Logic.end_connection(midi_out)

# midi_out.send_message([0xE0, 0x00, 0x00])

midi_out.close_port()
midi_in.close_port()

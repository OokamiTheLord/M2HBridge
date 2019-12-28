import rtmidi

# from HUI import HUI_display_AA
import Logic
import time

midi_out = rtmidi.MidiOut()
midi_in = rtmidi.MidiIn()

midi_out.open_port(4)
midi_in.open_port(4)
midi_in.ignore_types(sysex=False)

# HUI_display_AA()
Logic.initiate_connection(midi_in, midi_out)
for i in range(8):
    Logic.send_fader(midi_out, i, 0x7f, 0x7f)

print("now")
time.sleep(1)

Logic.end_connection(midi_out)


midi_out.close_port()
midi_in.close_port()

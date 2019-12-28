import rtmidi

# from HUI import HUI_display_AA
import Logic
import time

midiout = rtmidi.MidiOut()
midiin = rtmidi.MidiIn()

midiout.open_port(4)
midiin.open_port(4)
midiin.ignore_types(sysex=False)

# HUI_display_AA()
Logic.initiate_connection(midiin, midiout)
for i in range(8):
    Logic.send_fader(midiout, i, 0x7f, 0x7f)

print("now")
time.sleep(1)

Logic.end_connection(midiout)


midiout.close_port()
midiin.close_port()

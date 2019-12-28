import consts
from main import midiout

hdr = consts.hdr + [5, 0]
end = consts.end

def HUI_display_AA():
    for i in range(0, 0xff):
        table = hdr + [0x10, 0x08, 0x41, 0x41, 0x41, 0x41] + end
        midiout.send_message(table)
import consts
from main import midi_out

hdr = consts.hdr + [5, 0]
end = consts.end


# noinspection PyPep8Naming
def HUI_display_AA():
    for i in range(0, 0xff):
        table = hdr + [0x10, 0x08, 0x41, 0x41, 0x41, 0x41] + end
        midi_out.send_message(table)

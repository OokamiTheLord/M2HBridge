import consts
import exceptions
import enum
import common

import time

hdr = consts.hdr + [0x10]
_hdr_len = len(hdr)
end = consts.end

_device_query = hdr + [0] + end
_go_offline = hdr + [0x0f, 0x7f] + end


# TODO: Improve - this is naive implementation for now.
#  Other midi messages should be filtered as they would disrupt communication, waiting times should be implemented etc.
def initiate_connection(midi_input, midi_output):
    """
    
    :param midi_input: open midi input
    :type midi_input: rtmidi.MidiIn
    :param midi_output: open midi output
    :type midi_output: rtmidi.MidiOut
    """

    class MessageType(enum.IntEnum):
        host_connection_query = 1
        host_connection_reply = 2
        host_connection_confirmation = 3
        host_connection_error = 4

    message_type_pos = _hdr_len
    serial_pos = _hdr_len + 1
    serial_len = 7
    challenge_response_pos = serial_pos + serial_len
    challenge_response_len = 4

    midi_output.send_message(_device_query)
    time.sleep(0.5)
    midi_response = midi_input.get_message()
    if midi_response is None:
        raise exceptions.InitializationFailure("No response")
    midi_response, _ = midi_response

    if midi_response[message_type_pos] != MessageType.host_connection_query:
        try:
            message_name = MessageType(midi_response[message_type_pos]).name
        except ValueError:
            message_name = "unexpected value '{}'".format(midi_response[message_type_pos])
        raise exceptions.InitializationFailure("host_connection_query message type expected. Got {} instead".format(
            message_name))

    serial = midi_response[serial_pos:serial_pos+serial_len]
    challenge = midi_response[challenge_response_pos:challenge_response_pos+challenge_response_len]
    response = challenge_to_response(challenge)

    host_connection_reply = hdr + [MessageType.host_connection_reply.value] + serial + response + end
    midi_output.send_message(host_connection_reply)
    time.sleep(0.5)
    midi_response, _ = midi_input.get_message()

    if midi_response[message_type_pos] != MessageType.host_connection_confirmation:
        try:
            message_name = MessageType(midi_response[message_type_pos]).name
        except ValueError:
            message_name = "unexpected value '{}'".format(midi_response[message_type_pos])
        raise exceptions.InitializationFailure(
            "host_connection_confirmation message type expected. Got {} instead".format(
                message_name))
    if midi_response[serial_pos:serial_pos + serial_len] != serial:
        raise exceptions.InitializationFailure("Received unexpected message from {}".format(
            common.string_from_hex(midi_response[serial_pos:serial_pos + serial_len])))


def challenge_to_response(challenge):
    """

    :param challenge:
    :type challenge: list
    :return:
    """

    r1 = 0x7f & (challenge[0] + (challenge[1] ^ 0xa) - challenge[3])
    r2 = 0x7f & ((challenge[2] >> 4) ^ (challenge[1] + challenge[3]))
    r3 = 0x7f & (challenge[3] - (challenge[2] << 2) ^ (challenge[0] | challenge[1]))
    r4 = 0x7f & (challenge[1] - challenge[2] + (0xf0 ^ (challenge[3] << 4)))

    return [r1, r2, r3, r4]


def end_connection(midi_output):
    """

    :param midi_output:
    :type midi_output: rtmidi.MidiOut
    :return:
    """
    midi_output.send_message(_go_offline)


# TODO: Consider creating class accepting two values for higher and lower, integer, percent etc. to be used in functions
#   as this which operates on 7bit values
def send_fader(midi_output, fader_id, fader_position_higher, fader_position_lower):
    """

    :param fader_position_lower:
    :param fader_position_higher:
    :param midi_output:
    :type midi_output: rtmidi.MidiOut
    :param fader_id:
    :return:
    """
    if fader_id not in range(0, 9):
        raise ValueError("fader_id must be in range 0-7 (or 8 for master)")
    # if fader_position not in range (0, 16383):
        # raise ValueError("fader_position must be in range 0-65535")

    # format Ei, ll, hh
    # i - fader id - 0 to 7 - 8 for master
    # ll - lower 8 bits
    set_fader_message = [0xE0 + fader_id, fader_position_lower, fader_position_higher]
    midi_output.send_message(set_fader_message)

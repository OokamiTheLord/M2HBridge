def string_from_hex(hex_table, separator=''):
    return ''.join('{:02X}{}'.format(x, separator) for x in hex_table)
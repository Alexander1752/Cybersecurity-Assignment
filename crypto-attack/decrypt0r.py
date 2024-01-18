#!/usr/bin/env python3

def str_to_number(text):
    """ Encodes a text to a long number representation (big endian). """
    return int.from_bytes(text, 'big')

def number_to_str(num):
    """ Decodes a text to a long number representation (big endian). """
    num = int(num)
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big').decode('ASCII')

if __name__ == "__main__":
    with open("server_resp.txt", "r") as f:
        flag_times_2 = str.encode(f.readline()[2:-2], 'latin1').decode('unicode_escape').encode('latin1')

    flag_num = str_to_number(flag_times_2) // 2

    print("Flag:", number_to_str(flag_num))


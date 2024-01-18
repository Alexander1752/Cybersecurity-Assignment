#!/usr/bin/env python3

import base64
import json
import gmpy2


def str_to_number(text):
    """ Encodes a text to a long number representation (big endian). """
    return int.from_bytes(text.encode("ASCII"), 'big')

def number_to_str(num):
    """ Decodes a text to a long number representation (big endian). """
    num = int(num)
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big').decode('ASCII')

def encrypt(pub_k, msg_num):
    """ We only managed to steal this function... """
    cipher_num = gmpy2.powmod(msg_num, pub_k["e"], pub_k["n"])
    # note: gmpy's to_binary uses a custom format (little endian + special GMPY header)!
    cipher_b64 = base64.b64encode(gmpy2.to_binary(cipher_num))
    return cipher_b64

if __name__ == "__main__":
    pub_k = {"e": 226459, "n": 19249914891372821195233755397377435273038294603898400682321457416516743608555399418788390614025577717150345656989288758208583263221486414464587008738007848201869249814099855537086399281879881122953632013709647142739648627977745178990393728951142064722779797941130653594465798241167513655575893477156598855283930906157456942713374127778581133248749382757251830450226582503077382192408166322868228174240981448806507657819509875133438193376218584011769107555828031428087996774521615937536855728018424392787619310593686535507391837309413522616292594176620411361899174342184890122043011951714546663249567975925690622543079}
    # generate a message

    message = "SpeishFlag{E8KYG115DK1f2JSYDz4KutSax1SUQa9G}" # actual flag of the challenge

    # note: encrypt requires a number
    msg_num = str_to_number(message)
    # test the reverse
    print("Message:", number_to_str(msg_num))
    # encrypt the message
    cipher = encrypt(pub_k, msg_num)
    print("Ciphertext:", cipher)

    # encode the message to the server's format

    out = {"flag":str(cipher)[2:-1]}

    r = json.dumps(out)
    with open("my_msg.txt", "wb") as f:
        f.write(base64.b64encode(bytes(r, 'ascii')) + b'\x0a' * 3)

    import subprocess
    subprocess.Popen("cat my_msg.txt | nc 141.85.228.32 11007", shell=True)

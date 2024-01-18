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
    return cipher_num

if __name__ == "__main__":
    with open("message.txt", "r") as f:
        b64decoded = base64.b64decode(f.readline())
        file_dict = json.loads(b64decoded)
        flag = file_dict["flag"]
    
    pub_k = {"e": 226459, "n": 19249914891372821195233755397377435273038294603898400682321457416516743608555399418788390614025577717150345656989288758208583263221486414464587008738007848201869249814099855537086399281879881122953632013709647142739648627977745178990393728951142064722779797941130653594465798241167513655575893477156598855283930906157456942713374127778581133248749382757251830450226582503077382192408166322868228174240981448806507657819509875133438193376218584011769107555828031428087996774521615937536855728018424392787619310593686535507391837309413522616292594176620411361899174342184890122043011951714546663249567975925690622543079}

    """ We multiply the encrypted flag with the number 2 also encrypted, we get (2*flag) encrypted """
    flag_times_2_enc =\
        base64.b64encode(gmpy2.to_binary( # revert all the unpacking we've done on the encrypted flag, but now on the modified value
            gmpy2.powmod( # used to compute (2*flag) mod n by using 1 as the exponent
                gmpy2.from_binary(base64.b64decode(str.encode(flag, encoding='ascii'))) # unpack gmpy2.mpz value
                * encrypt(pub_k, gmpy2.mpz(2)), # encrypt the value 2
                1, # the exponent is 1
                pub_k["n"])))
    
    r = dict()
    r["flag"] = str(flag_times_2_enc)[2:-1]

    r = json.dumps(r)
    with open("salted_msg.txt", "wb") as f:
        f.write(base64.b64encode(bytes(r, 'ascii')) + b'\x0a' * 3)

    """
    Send the composite encrypted flag to the server to decrypt it for us.
    Due to the number 2 being used as a "salt", server will show the decrypted value,
    as this is no longer the flag it expects
    """
    import subprocess
    subprocess.Popen("cat salted_msg.txt | nc 141.85.228.32 11007 | grep \"b'\" > server_resp.txt", shell=True)
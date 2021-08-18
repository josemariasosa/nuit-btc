#!/usr/bin/env python3
# coding=utf-8

import re
import hashlib
import hmac

from crypto.ecdsa.secp256k1 import P, N, G

HARDENED_INDEX = (2 ** 32) // 2
REGEX_DERIVATION_PATH = re.compile("^m(/[0-9]+['hH]?)*$")
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def _generate_public_key(private_key: bytes) -> bytes:
    point = int.from_bytes(private_key, 'big') * G
    return point.sec(compressed=True)


def _derive_private_child(privkey: bytes, chaincode: bytes,
                          index: int, hard: bool=True) -> tuple[bytes, bytes]:
    if hard:
        msg = b"\x00" + privkey + index.to_bytes(4, "big")
    else:
        pubkey = _generate_public_key(privkey)
        msg = pubkey + index.to_bytes(4, "big")

    h = hmac.new(key=chaincode, msg=msg, digestmod=hashlib.sha512).digest()
    L256 = h[:32]
    R256 = h[32:]

    child_privkey = (int.from_bytes(L256, 'big')
                    + int.from_bytes(privkey, 'big')) % N
    return child_privkey.to_bytes(32, 'big'), R256


def _pubkey_to_fingerprint(pubkey):
    rip = hashlib.new("ripemd160")
    rip.update(hashlib.sha256(pubkey).digest())
    return rip.digest()[:4]


# Refactored code segments from <https://github.com/keis/base58>
def _b58encode_extended_key(v: bytes) -> str:
    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8

    string = ""
    while acc:
        acc, idx = divmod(acc, 58)
        string = BASE58_ALPHABET[idx : idx + 1] + string
    return string


def _b58decode_extened_key(s: str) -> bytes:
    """ Decodes the base58-encoded string s into bytes (xprv have 82 bytes) """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * 58

    return decoded.to_bytes(82, byteorder='big')
#!/usr/bin/env python3
# coding=utf-8

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# Refactored code segments from <https://github.com/keis/base58>
def _encode_base58(v: bytes) -> str:
    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8

    string = ""
    while acc:
        acc, idx = divmod(acc, 58)
        string = BASE58_ALPHABET[idx : idx + 1] + string
    return string


def _decode_base58(s: str, length: int) -> bytes:
    """ Decodes the base58-encoded string s into bytes  """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * 58

    return decoded.to_bytes(length, byteorder='big')

#!/usr/bin/env python3
# coding=utf-8

import re
import hashlib
import hmac

from dataclasses import dataclass


from crypto.ecdsa.secp256k1 import P, G, S256Point
# from crypto.helper import b58encode_extended_key, b58decode_extened_key

from keys.derivation.extended import ExtendedKeys

HARDENED_INDEX = (2 ** 32) // 2
REGEX_DERIVATION_PATH = re.compile("^m(/[0-9]+['hH]?)*$")


# def _derive_hardened_private_child(privkey, chaincode, index):
#     """A.k.a CKDpriv, in bip-0032, but the hardened way
#     :param privkey: The parent's private key, as bytes
#     :param chaincode: The parent's chaincode, as bytes
#     :param index: The index of the node to derive, as int
#     :return: (child_privatekey, child_chaincode)
#     """
#     # assert isinstance(privkey, bytes) and isinstance(chaincode, bytes)
#     # assert index & HARDENED_INDEX
#     # payload is the I from the BIP. Index is 32 bits unsigned int, BE.

#     """
#     I = HMAC-SHA512(Key = cpar, Data = 0x00 || ser256(kpar) || ser32(i)).
#     (Note: The 0x00 pads the private key to make it 33 bytes long.)
#     """


#     I = hmac.new(
#         chaincode, b"\x00" + privkey + index.to_bytes(4, "big"), hashlib.sha512
#     ).digest()

#     L256 = I[:32]
#     R256 = I[32:]

#     child_privkey = (int.from_bytes(L256, 'big') + int.from_bytes(privkey, 'big')) % P

#     return child_privkey.to_bytes(32, 'big'), R256


# class InvalidDerivationPath(Exception):
#     """Invalid format for derivation path."""


@dataclass
class KeyChain:
    """Class to keep track of the parent and child keys."""
    privkey: bytes
    pubkey: bytes
    chaincode: bytes
    fingerprint: bytes = None # parent's pubkey fingerprint
    depth: int = 0
    index: int = 0
    testnet: bool = False
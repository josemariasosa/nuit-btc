#!/usr/bin/env python3
# coding=utf-8

import hashlib
import hmac

# from crypto.ecdsa.secp256k1 import G
# from keys.helper import b58encode_extended_key, b58decode_extened_key

from keys.derivation.extended import ExtendedKeys

class ChildKeyDerivation:
    """docstring for ChildKeyDerivation"""
    def __init__(self, extended_keys: ExtendedKeys):
        if m:
            mkey = ExtendedKeys.parse_extended_private_key(m)
            self.master_private_key = mkey.master_private_key
            self.master_public_key = mkey.master_public_key
            self.master_chain_code = mkey.chain_code
            print('master_private_key:', mkey.master_private_key)
            print('master_public_key:', mkey.master_public_key)
            print('chain_code:', mkey.chain_code)
            exit()

    @classmethod
    def parse_extended_private_key(xprv)

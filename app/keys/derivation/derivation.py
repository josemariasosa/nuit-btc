#!/usr/bin/env python3
# coding=utf-8

import hashlib
import hmac

from crypto.ecdsa.secp256k1 import G, S256Point
# from crypto.helper import b58encode_extended_key, b58decode_extened_key

from keys.derivation.extended import ExtendedKeys

HARDENED_INDEX = (2 ** 32) // 2

class InvalidDerivationPath(Exception):
    """Invalid format for derivation path."""

class ChildKeyDerivation:
    def __init__(self, extended_keys: ExtendedKeys):
        self.m = extended_keys.master_private_key
        self.M = extended_keys.master_public_key
        self.chain_code = extended_keys.chain_code
        self.testnet = extended_keys.testnet

    def __str__(self):
        return (
            f'master_private_key: {self.master_private_key}\n' +
            f'master_public_key: {self.master_public_key}\n' +
            f'master_chain_code: {self.master_chain_code}\n' +
            f'testnet: {self.testnet}'
        )

    def generate_public_key(self, private_key: bytes) -> bytes:
        point = int.from_bytes(private_key, 'big') * G
        return point.sec(compressed=True)

    def derive_from_path(self, path='m/44h/0h/0h/0/0'):
        """BIP 44: m / purpose' / coin type' / account' / receving / index"""
        steps = path.split('/')
        if steps.pop(0) != 'm':
            raise InvalidDerivationPath()

        parent = {
            'public_key': self.M,
            'private_key': self.m,
            'chain_code': self.chain_code
        }

        child = {}

        for step in steps:
            ix = 0
            hard = False
            if step.endswith('h') or step.endswith('\''):
                hard = True
                ix += HARDENED_INDEX
                step = step[:-1]

            if step.isdigit():
                ix += int(step)
            else:
                raise InvalidDerivationPath()

            seed = hmac.new(key=parent.get('chain_code'),
                            msg=parent.get('public_key')+ix.to_bytes(4, 'big'),
                            digestmod=hashlib.sha512).digest()

            left = seed[:32]
            right = seed[32:]

            left_int = int.from_bytes(left, 'big')
            private_key_int = int.from_bytes(parent.get('private_key'), 'big')

            # Scalar Addition
            child_private_key = (left_int + private_key_int).to_bytes(33, 'big')

            child.update({
                'private_key': child_private_key,
                'public_key': self.generate_public_key(child_private_key),
                'chain_code': right
            })

            from pprint import pprint
            pprint(child)
            exit()




            left_point = left_int * G
            public_key_point = S256Point.parse(parent.get('public_key'))


            # if hard:


            print(left_point)
            print("left_point")

            print(public_key_point)
            print("public_key_point")
            exit()

            child = {
                'public_key': self.M,
                'private_key': self.m,
                'chain_code': self.chain_code                
            }





            print(ix)
            exit()


        print(steps)




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


def _derive_hardened_private_child(privkey, chaincode, index):
    """A.k.a CKDpriv, in bip-0032, but the hardened way
    :param privkey: The parent's private key, as bytes
    :param chaincode: The parent's chaincode, as bytes
    :param index: The index of the node to derive, as int
    :return: (child_privatekey, child_chaincode)
    """
    # assert isinstance(privkey, bytes) and isinstance(chaincode, bytes)
    # assert index & HARDENED_INDEX
    # payload is the I from the BIP. Index is 32 bits unsigned int, BE.

    """
    I = HMAC-SHA512(Key = cpar, Data = 0x00 || ser256(kpar) || ser32(i)).
    (Note: The 0x00 pads the private key to make it 33 bytes long.)
    """


    I = hmac.new(
        chaincode, b"\x00" + privkey + index.to_bytes(4, "big"), hashlib.sha512
    ).digest()

    L256 = I[:32]
    R256 = I[32:]

    child_privkey = (int.from_bytes(L256, 'big') + int.from_bytes(privkey, 'big')) % P

    return child_privkey.to_bytes(32, 'big'), R256


class InvalidDerivationPath(Exception):
    """Invalid format for derivation path."""


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

    @staticmethod
    def _parse_str_path_as_index_list(path: str) -> list[int]:
        if not REGEX_DERIVATION_PATH.match(path):
            raise InvalidDerivationPath(f'{path}')

        steps = path.split('/')
        steps.pop(0)

        index_list = []
        for step in steps:
            if step[-1] in ["'", "h", "H"]:
                index_list.append(int(step[:-1]) + HARDENED_INDEX)
            else:
                index_list.append(int(step))

        return index_list

    def derive_from_path(self, path: str = "m/0'/0h/0h/0/0"):
        """BIP 44: m / purpose' / coin type' / account' / receving / index
            examples: 'm/44h/0h/0h/0/0'
                      "m/44'/0'/3'/1/46"
        """
        steps = self._parse_str_path_as_index_list(path)

        parent = KeyChain(privkey=self.m,
                          pubkey=self.M,
                          chaincode=self.chain_code,
                          testnet=self.testnet)

        assert parent.privkey is not None

        for relative_depth, index in enumerate(steps):
            if index >= HARDENED_INDEX:
                privkey, chaincode = _derive_hardened_private_child(
                    parent.privkey, parent.chaincode, index
                )

                print('parent.privkey', parent.privkey)
                print('child.privkey', privkey)

            exit()

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
            pprint("child")
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




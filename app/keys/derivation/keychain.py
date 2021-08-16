#!/usr/bin/env python3
# coding=utf-8

import re
import hashlib
import hmac

from enum import Enum, auto

from dataclasses import dataclass


from crypto.ecdsa.secp256k1 import P, G, S256Point, PrivateKey
from crypto.helper import b58encode_extended_key, b58decode_extened_key

from keys.derivation.extended import ExtendedKeys

HARDENED_INDEX = (2 ** 32) // 2
REGEX_DERIVATION_PATH = re.compile("^m(/[0-9]+['hH]?)*$")

class Network(Enum):
    MAINNET = auto()
    TESTNET = auto()

class KeyType(Enum):
    PRIVATE = auto()
    PUBLIC = auto()


ENCODING_PREFIX = {
    Network.MAINNET: {
        KeyType.PRIVATE: b'\x04\x88\xAD\xE4',
        KeyType.PUBLIC: b'\x04\x88\xB2\x1E',
    },
    Network.TESTNET: {
        KeyType.PRIVATE: b'\x04\x35\x83\x94',
        KeyType.PUBLIC: b'\x04\x35\x87\xCF',
    },
}


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


class NotValidMasterPrivateKey(Exception):
    """Not a valid Private Key for mainnet nor testnet."""


class ImpossibleToGenerateExtendedKeys(Exception):
    """Not enough information to generate extended keys."""


def _generate_public_key(private_key: bytes) -> bytes:
    point = int.from_bytes(private_key, 'big') * G
    return point.sec(compressed=True)

def _assert_checksum(xkey: bytes, checksum: bytes) -> None:
    # Double hash using SHA256
    hashed_xkey = hashlib.sha256(xkey).digest()
    hashed_xkey = hashlib.sha256(hashed_xkey).digest()

    if checksum != hashed_xkey[:4]:
        raise NotValidMasterPrivateKey('Invalid checksum.')

def _parse_version(version: bytes) -> tuple[str, str]:
    for network in list(Network):
        for key in list(KeyType):
            if ENCODING_PREFIX[network][key] == version:
                return network, key
    raise NotValidMasterPrivateKey('Invalid version.')

@dataclass
class KeyChain:
    """Class to keep track of the parent and child keys."""
    chaincode: bytes
    privkey: bytes = None
    pubkey: bytes = None
    fingerprint: bytes = None # parent's pubkey fingerprint
    depth: int = 0
    index: int = 0
    testnet: bool = False

    @classmethod
    def from_seed(cls, seed: str = '0c0d0e0f', testnet=False):
        bytes_seed = bytes.fromhex(seed)
        h = hmac.new(key=b"Bitcoin seed", msg=bytes_seed,
                     digestmod=hashlib.sha512).digest()
        privkey = h[:32]
        pubkey = _generate_public_key(privkey)
        chaincode = h[32:]
        return KeyChain(chaincode=chaincode,
                        privkey=privkey,
                        pubkey=pubkey,
                        testnet=testnet)

    @classmethod
    def from_xkey(cls, xkey: str):
        xkey = b58decode_extened_key(xkey)

        checksum = xkey[-4:]
        xkey = xkey[:-4]
        _assert_checksum(xkey, checksum)

        version = xkey[:4]
        xkey = xkey[4:]
        network, key_type = _parse_version(version)

        depth = xkey[:1]
        xkey = xkey[1:]

        fingerprint = xkey[:4] if xkey[:4] != b'\x00' * 4 else None
        xkey = xkey[4:]

        index = xkey[:4]
        xkey = xkey[4:]

        chaincode = xkey[:32]
        xkey = xkey[32:]

        if key_type == KeyType.PRIVATE:
            if xkey[:1] != b'\x00':
                raise NotValidMasterPrivateKey('Invalid private key.')
            privkey = xkey[1:]
            pubkey = _generate_public_key(privkey)

        else:
            assert key_type == KeyType.PUBLIC
            pubkey = xkey
            privkey = None

        return KeyChain(chaincode=chaincode,
                        privkey=privkey,
                        pubkey=pubkey,
                        fingerprint=fingerprint,
                        depth=depth,
                        index=index,
                        testnet=True if network == Network.TESTNET else False)

    def serialization(self, key_type: KeyType) -> str:
        network = Network.TESTNET if self.testnet else Network.MAINNET
        version = ENCODING_PREFIX[network][key_type]
        depth = self.depth.to_bytes(1, 'big')
        fingerprint = b'\x00' * 4 if self.fingerprint is None else fingerprint
        index = self.index.to_bytes(4, 'big')

        if key_type == KeyType.PRIVATE:
            if self.privkey is None:
                raise ImpossibleToGenerateExtendedKeys()
            key = b'\x00' + self.privkey

        else:
            assert key_type == KeyType.PUBLIC
            key = self.pubkey

        xkey = version + depth + fingerprint + index + self.chaincode + key

        # Double hash using SHA256
        hashed_xkey = hashlib.sha256(xkey).digest()
        hashed_xkey = hashlib.sha256(hashed_xkey).digest()

        # Append 4 bytes of checksum
        xkey += hashed_xkey[:4]

        # Return base58
        return b58encode_extended_key(xkey)

    @property
    def xprv(self) -> str:
        return self.serialization(KeyType.PRIVATE)

    @property
    def xpub(self) -> str:
        return self.serialization(KeyType.PUBLIC)



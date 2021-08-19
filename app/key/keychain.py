#!/usr/bin/env python3
# coding=utf-8

import hashlib
import hmac

from enum import Enum, auto
from dataclasses import dataclass

from key.utils import (
    HARDENED_INDEX,
    REGEX_DERIVATION_PATH,
    _b58encode_extended_key,
    _b58decode_extened_key,
    _generate_public_key,
    _derive_private_child,
    _derive_public_child,
    _pubkey_to_fingerprint
)

class InvalidDerivationPath(Exception):
    """Invalid format for derivation path."""


class NotValidMasterPrivateKey(Exception):
    """Not a valid Private Key for mainnet nor testnet."""


class ImpossibleToGenerateExtendedKeys(Exception):
    """Not enough information to generate extended keys."""


class ImpossibleToDeriveKeys(Exception):
    """Not enough information to derive keys."""


class Network(Enum):
    MAINNET = auto()
    TESTNET = auto()

class KeyType(Enum):
    PRIVATE = auto()
    PUBLIC = auto()


ENCODING_PREFIX = {
    Network.MAINNET: {
        KeyType.PRIVATE: b'\x04\x88\xAD\xE4',
        KeyType.PUBLIC: b'\x04\x88\xB2\x1E'
    },
    Network.TESTNET: {
        KeyType.PRIVATE: b'\x04\x35\x83\x94',
        KeyType.PUBLIC: b'\x04\x35\x87\xCF'
    },
}

ZERO = b'\x00'


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

    def __str__(self):
        chaincode = self.chaincode[:4]
        privkey = self.privkey[:4] if self.privkey else None
        pubkey = self.pubkey[:4] if self.pubkey else None
        return ' '.join([
            f'KeyChain(chaincode={chaincode}, privkey={privkey},',
            f'pubkey={pubkey}, fingerprint={self.fingerprint},',
            f'depth={self.depth}, index={self.index},',
            f'testnet={self.testnet})'
        ])

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
        xkey = _b58decode_extened_key(xkey)

        checksum = xkey[-4:]
        xkey = xkey[:-4]
        _assert_checksum(xkey, checksum)

        version = xkey[:4]
        xkey = xkey[4:]
        network, key_type = _parse_version(version)

        depth = int.from_bytes(xkey[:1], 'big')
        xkey = xkey[1:]

        fingerprint = xkey[:4] if xkey[:4] != ZERO * 4 else None
        xkey = xkey[4:]

        index = int.from_bytes(xkey[:4], 'big')
        xkey = xkey[4:]

        chaincode = xkey[:32]
        xkey = xkey[32:]

        if key_type == KeyType.PRIVATE:
            if xkey[:1] != ZERO:
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
        fingerprint = self.fingerprint if self.fingerprint else ZERO * 4
        index = self.index.to_bytes(4, 'big')

        if key_type == KeyType.PRIVATE:
            if self.privkey is None:
                raise ImpossibleToGenerateExtendedKeys('Privkey is required.')
            key = ZERO + self.privkey

        else:
            assert key_type == KeyType.PUBLIC
            if self.pubkey:
                key = self.pubkey
            elif self.privkey:
                key = _generate_public_key(privkey)
            else:
                raise ImpossibleToGenerateExtendedKeys('Privkey is required.')

        xkey = version + depth + fingerprint + index + self.chaincode + key

        # Double hash using SHA256
        hashed_xkey = hashlib.sha256(xkey).digest()
        hashed_xkey = hashlib.sha256(hashed_xkey).digest()

        # Append 4 bytes of checksum
        xkey += hashed_xkey[:4]

        # Return base58
        return _b58encode_extended_key(xkey)

    @property
    def xprv(self) -> str:
        return self.serialization(KeyType.PRIVATE)

    @property
    def xpub(self) -> str:
        return self.serialization(KeyType.PUBLIC)

    def _get_child_using_privkey(self, steps):
        for _, index in enumerate(steps):
            _privkey = self.privkey if _ == 0 else privkey
            _chaincode = self.chaincode if _ == 0 else chaincode
            if index >= HARDENED_INDEX:
                assert self.privkey is not None
                privkey, chaincode = _derive_private_child(
                    _privkey, _chaincode, index, hard=True
                )
            else:
                privkey, chaincode = _derive_private_child(
                    _privkey, _chaincode, index, hard=False
                )

        pubkey = _generate_public_key(privkey)
        parent_pubkey = _generate_public_key(_privkey)
        child = KeyChain(chaincode=chaincode,
                         privkey=privkey,
                         pubkey=pubkey,
                         fingerprint=_pubkey_to_fingerprint(parent_pubkey),
                         depth=self.depth+len(steps),
                         index=steps[-1],
                         testnet=self.testnet)
        return child

    def _get_child_using_pubkey(self, steps):
        for _, index in enumerate(steps):
            _pubkey = self.pubkey if _ == 0 else pubkey
            _chaincode = self.chaincode if _ == 0 else chaincode
            if index >= HARDENED_INDEX:
                raise ImpossibleToDeriveKeys('Privkey is required.')
            else:
                pubkey, chaincode = _derive_public_child(
                    _pubkey, _chaincode, index
                )

        child = KeyChain(chaincode=chaincode,
                         privkey=None,
                         pubkey=pubkey,
                         fingerprint=_pubkey_to_fingerprint(_pubkey),
                         depth=self.depth+len(steps),
                         index=steps[-1],
                         testnet=self.testnet)
        return child

    def derive_child_from_path(self, path: str):
        steps = _parse_str_path_as_index_list(path)
        if len(steps) > 0:
            if self.privkey:
                child = self._get_child_using_privkey(steps)
            elif self.pubkey:
                child = self._get_child_using_pubkey(steps)
            else:
                raise ImpossibleToDeriveKeys('Pubkey is required.')
        else:
            child = self

        return child

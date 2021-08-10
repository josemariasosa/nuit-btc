#!/usr/bin/env python3
# coding=utf-8

import hashlib
import hmac

from crypto.ecdsa.secp256k1 import G
from crypto.helper import b58encode_extended_key, b58decode_extened_key


class NotValidMasterPrivateKey(Exception):
    """Not a valid Private Key for mainnet nor testnet."""


class ImpossibleToGenerateExtendedKeys(Exception):
    """Not enough information to generate extended keys."""


class ExtendedKeys:
    """docstring for ExtendedKeys"""
    def __init__(self, seed: str = None, testnet: bool = False, **kwargs):
        if bool(seed):
            self.seed = bytes.fromhex(seed)
            self.master_private_key, self.chain_code = self.compute_split_hash(self.seed)
        else:
            self.master_private_key = kwargs.get('master_private_key')
            self.chain_code = kwargs.get('chain_code')
            if not (bool(self.master_private_key) and bool(self.chain_code)):
                raise ImpossibleToGenerateExtendedKeys(
                    """A seed in hex or (chain code and master private key) \
                    must be provided to generate extended keys."""
                )

        self.testnet = testnet
        self.master_public_key = self.generate_public_key(self.master_private_key)

    def generate_public_key(self, private_key: bytes) -> bytes:
        point = int.from_bytes(private_key, 'big') * G
        return point.sec(compressed=True)

    @staticmethod
    def compute_split_hash(seed: bytes) -> tuple[bytes, bytes]:
        # Compute HMAC-SHA512 of seed
        seed = hmac.new(key=b"Bitcoin seed", msg=seed, digestmod=hashlib.sha512).digest()
        return (
            seed[:32], # Master key
            seed[32:]  # Chain code
        )

    def extended_private_serialization(self) -> str:
        # Serialization format can be found at: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
        xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
        if self.testnet:
            xprv = b"\x04\x35\x83\x94"  # Version for private testnet
        xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xprv += self.chain_code
        xprv += b"\x00" + self.master_private_key

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        # Append 4 bytes of checksum
        xprv += hashed_xprv[:4]

        # Return base58
        return b58encode_extended_key(xprv)

    def extended_public_serialization(self) -> str:
        xpub = b"\x04\x88\xb2\x1e"  # Version for private mainnet
        if self.testnet:
            xpub = b"\x04\x35\x87\xcf"  # Version for private testnet
        xpub += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xpub += self.chain_code
        xpub = xpub + self.master_public_key

        # Double hash using SHA256
        hashed_xpub = hashlib.sha256(xpub).digest()
        hashed_xpub = hashlib.sha256(hashed_xpub).digest()

        # Append 4 bytes of checksum
        xpub += hashed_xpub[:4]

        # Return base58
        return b58encode_extended_key(xpub)

    @property
    def xprv(self) -> str:
        return self.extended_private_serialization()

    @property
    def xpub(self) -> str:
        return self.extended_public_serialization()

    @classmethod
    def parse_extended_private_key(cls, xprv: str):
        xprv = b58decode_extened_key(xprv)

        checksum = xprv[-4:]
        xprv = xprv[:-4]

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        if checksum != hashed_xprv[:4]:
            raise NotValidMasterPrivateKey('Invalid checksum.')

        version = xprv[:4]
        xprv = xprv[4:]
        if version == b"\x04\x88\xad\xe4":
            testnet = False
        elif version == b"\x04\x35\x83\x94":
            testnet = True
        else:
            raise NotValidMasterPrivateKey('Invalid version.')

        depth = xprv[:1]
        xprv = xprv[1:]

        parent_fingerprint = xprv[:4]
        xprv = xprv[4:]

        child_number = xprv[:4]
        xprv = xprv[4:]

        if depth + parent_fingerprint + child_number != b"\x00" * 9:
            raise NotValidMasterPrivateKey('Invalid depth, parent fingerprint or child number.')

        chain_code = xprv[:32]
        xprv = xprv[32:]

        private_key_prepend = xprv[:1]
        xprv = xprv[1:]

        if private_key_prepend != b'\x00':
            raise NotValidMasterPrivateKey('Invalid private key.')

        private_key = xprv[:32]

        return cls(testnet=testnet,
                   master_private_key=private_key,
                   chain_code=chain_code)
    
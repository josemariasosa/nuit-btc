#!/usr/bin/env python3
# coding=utf-8

import os
import hashlib
import secrets
import unicodedata

from key.utils import _normalize_string

PBKDF2_ROUNDS = 2048
FAIR_DICE = ['1', '2', '3', '4', '5', '6']


class Mnemonic():
    """Generar una llave privada maestra."""
    def __init__(self, language: str, number_of_words: int = 12):
        self.language = language
        self.wordlist = self.import_words_for_language()
        if number_of_words not in [12, 15, 18, 21, 24]:
            raise ValueError(
                'El número permitido de palabras mnemónicas (BIP39) debe ser [12, 15, 18, 21, 24]'
            )
        self.number_of_words = number_of_words

    @staticmethod
    def _get_directory() -> str:
        return os.path.join(os.path.dirname(__file__), "wordlist")

    def import_words_for_language(self):
        with open(self._get_directory()+'/'+self.language+'.txt', 'r') as f:
            words = f.read().split('\n')
        return words

    @staticmethod
    def capture_dice_rolls() -> str:
        r = ''
        i = 0
        print("""
            -> Inserta el resultado del lanzamiento [1-6].
            -> Únicamente valores entre 1 y 6 están permitidos.
            -> Capturar al menos 99 lanzamientos.
            -> Para terminar capture cualquier valor no permitido.
        """)
        while True:
            i += 1
            n = input(f'Resultado del lanzamiento ({i}): ')
            if n in FAIR_DICE:
                r += n
            else:
                return r

    @staticmethod
    def simulate_dice_rolls(rolls: int = 200) -> str:
        r = ''
        for i in range(rolls):
            r += secrets.choice(FAIR_DICE)
        return r

    @staticmethod
    def get_entropy_length(number_of_words: int) -> int:
        """La fórmula proviene de despejar la longitud de entropía en BIP39."""
        return int((352 * number_of_words) / 33) # (1 byte = 8 bits)

    @staticmethod
    def bits_to_bytearray(entropy: str) -> bytearray:
        h = hex(int(entropy, 2))[2:]
        if len(h) % 2 != 0:
            h = '0' + h
        return bytearray.fromhex(h)

    def generate_entropy(self, manually: bool = False) -> str:
        """Generar entropía lanzando n veces un dado."""
        r = self.capture_dice_rolls() if manually else self.simulate_dice_rolls()

        if len(r) < 99:
            print(f'WARNING: Input is only {2.585 * len(r)} bits of entropy\n')

        br = r.encode()
        if self.number_of_words == 24:
            h = hashlib.sha256(br).digest()
        else:
            entropy_length = self.get_entropy_length(self.number_of_words)
            h = hashlib.shake_256(br).digest(entropy_length // 8)

        entropy = bin(int.from_bytes(h, 'big'))[2:].zfill(len(h) * 8)
        return entropy

    def generate_checksum(self, entropy: str) -> str:
        """Entropy is in Binary but must be converted into bytearray."""
        b = self.bits_to_bytearray(entropy)
        h = hashlib.sha256(b).digest()
        checksum_length = len(entropy) // 32
        checksum_bits = bin(int.from_bytes(h, 'big'))[2:].zfill(256)
        checksum = checksum_bits[:checksum_length]
        return str(checksum)

    def to_mnemonic(self, full: str) -> str:
        result = []
        for i in range(len(full) // 11):
            idx = int(full[i * 11 : (i + 1) * 11], 2)
            result.append(self.wordlist[idx])
        result = ' '.join(result)
        return result

    def is_valid_mnemonic(self, mnemonic: str) -> bool:
        bin_list = []
        words = mnemonic.split(' ')
        if len(words) not in [12, 15, 18, 21, 24]:
            return False

        for word in words:
            if word in self.wordlist:
                idx = self.wordlist.index(word)
                bidx = bin(idx)[2:].zfill(11)
                bin_list.append(bidx)
            else:
                return False

        bbin = ''.join(bin_list)
        entropy_length = self.get_entropy_length(len(words))
        entropy = bbin[:entropy_length]
        checksum = bbin[entropy_length:]

        if self.generate_checksum(entropy) == checksum:
            return True
        return False

    @classmethod
    def to_seed(cls, mnemonic: str, passphrase: str = '') -> str:
        mnemonic = _normalize_string(mnemonic, form='NFKD')
        passphrase = _normalize_string(passphrase, form='NFKD')
        passphrase = 'mnemonic' + passphrase
        mnemonic_bytes = mnemonic.encode('utf-8')
        passphrase_bytes = passphrase.encode('utf-8')
        stretched = hashlib.pbkdf2_hmac(
            "sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS
        ).hex().zfill(128)
        return stretched

    def generate_user_keys(self, manually: bool = False,
                           passphrase: str = '') -> dict[str, str]:
        entropy = self.generate_entropy(manually)
        checksum = self.generate_checksum(entropy)

        full = entropy + checksum
        mnemonic = self.to_mnemonic(full)
        seed = self.to_seed(mnemonic, passphrase)

        return {
            'entropy': entropy,
            'mnemonic': mnemonic,
            'passphrase': passphrase,
            'seed': seed
        }

#!/usr/bin/env python3
# coding=utf-8

"""
https://learnmeabitcoin.com/technical/mnemonic#generate-entropy

https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

CS = ENT / 32
MS = (ENT + CS) / 11

|  ENT  | CS | ENT+CS |  MS  |
+-------+----+--------+------+
|  128  |  4 |   132  |  12  |
|  160  |  5 |   165  |  15  |
|  192  |  6 |   198  |  18  |
|  224  |  7 |   231  |  21  |
|  256  |  8 |   264  |  24  |
"""

import os
import hashlib
import secrets

FAIR_DICE = ['1', '2', '3', '4', '5', '6']


class Mnemonic():
    """Generar una llave privada maestra."""
    def __init__(self, language: str, number_of_words: int = 12):
        self.language = language
        self.wordlist = self.import_words_for_language()
        if number_of_words not in [12, 15, 18, 21, 24]:
            raise ValueError(
                "El número permitido de palabras mnemónicas (BIP39) debe ser [12, 15, 18, 21, 24]"
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
        return int((352 * number_of_words) / (33 * 8)) # (1 byte = 8 bits)

    @staticmethod
    def bits_to_bytearray(entropy: str) -> bytearray:
        return bytearray.fromhex(hex(int(entropy, 2))[2:])

    def generate_entropy(self, manually: bool = False) -> str:
        """Generar entropía lanzando n veces un dado."""
        r = self.capture_dice_rolls() if manually else self.simulate_dice_rolls()

        if len(r) < 99:
            print(f'WARNING: Input is only {2.585 * len(r)} bits of entropy\n')

        br = r.encode()
        entropy_length = self.get_entropy_length(self.number_of_words)
        h = hashlib.shake_256(br).digest(entropy_length)
        entropy = bin(int.from_bytes(h, byteorder="big"))[2:].zfill(len(h) * 8)
        return entropy

    def generate_checksum(self, entropy: str) -> str:
        """Entropy is in Binary but must be converted into bytearray."""
        b = self.bits_to_bytearray(entropy)
        h = hashlib.sha256(b).digest()
        checksum_length = len(entropy) // 32
        checksum_bits = bin(int.from_bytes(h, byteorder="big"))[2:].zfill(256)
        checksum = checksum_bits[:checksum_length]
        return str(checksum)

    def to_mnemonic(self, full: str) -> str:
        result = []
        for i in range(len(full) // 11):
            idx = int(full[i * 11 : (i + 1) * 11], 2)
            result.append(self.wordlist[idx])
        result = ' '.join(result)
        return result

    def generate_user_keys(self) -> dict[str, str]:
        entropy = self.generate_entropy(manually=False)
        checksum = self.generate_checksum(entropy)

        full = entropy + checksum
        mnemonic = self.to_mnemonic(full)


        print('entropy:', entropy)
        print('mnemonic:', mnemonic)
        # mnemonic = self.to_mnemonic(entropy)





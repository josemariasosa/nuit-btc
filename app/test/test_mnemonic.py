#!/usr/bin/env python3
# coding=utf-8

import unittest

from keys.mnemonic.mnemonic import Mnemonic

class MnemonicTest(unittest.TestCase):
    """Test para la generación de palabras mnemónicas y las llaves maestras."""
    def setUp(self):
        self.m12 = Mnemonic(language='english', number_of_words=12)
        self.m15 = Mnemonic(language='english', number_of_words=15)
        self.m18 = Mnemonic(language='english', number_of_words=18)
        self.m21 = Mnemonic(language='english', number_of_words=21)
        self.m24 = Mnemonic(language='english', number_of_words=24)

        self.entropy12 = '10111111000111001001101101010100000101101110001100111001011100011111111100111000111011000111100000001110010010111000010100100000'
        self.entropy15 = '0010011000000011010011101101110011010000100001110111101001101111001100001010110011011110011000000111100011100100111100000000111111100010000001010011001001100011'
        self.entropy18 = '101010111010001001010100110000011011000110110101111100101001111011100001100110100110000011001111010010111001011110100101100100001100110011111000000000110111101000000101110000001111111001010001'
        self.entropy21 = '00100011111001110101101101011101100010110010101111110011010010100110000001000001110010100000010010110010001100101010111100110011111000010011010011111010001100111100111110010011000011100110010110111101011010010000001001001010'
        self.entropy24 = '1010000010001110100001000100101110101010001001100100011011001100100000110001100011001101100000010101110000001000000111100110001100010010101011010101111010111010010001111001010000000101100111001001010010010010000110000100001101110001111000001010100110010010'

    def test_binary_entropy_size_from_number_of_words(self):
        entropy12 = self.m12.generate_entropy(manually=False)
        entropy15 = self.m15.generate_entropy(manually=False)
        entropy18 = self.m18.generate_entropy(manually=False)
        entropy21 = self.m21.generate_entropy(manually=False)
        entropy24 = self.m24.generate_entropy(manually=False)

        self.assertEqual(len(entropy12), 128, 'incorrect entropy size')
        self.assertEqual(len(entropy15), 160, 'incorrect entropy size')
        self.assertEqual(len(entropy18), 192, 'incorrect entropy size')
        self.assertEqual(len(entropy21), 224, 'incorrect entropy size')
        self.assertEqual(len(entropy24), 256, 'incorrect entropy size')

    def test_incorrect_number_of_words(self):
        self.assertRaises(ValueError, Mnemonic, language='english', number_of_words=11)

    def test_checksum_from_binary_entropy(self):
        checksum12 = self.m12.generate_checksum(self.entropy12)
        checksum15 = self.m15.generate_checksum(self.entropy15)
        checksum18 = self.m18.generate_checksum(self.entropy18)
        checksum21 = self.m21.generate_checksum(self.entropy21)
        checksum24 = self.m24.generate_checksum(self.entropy24)

        self.assertEqual(checksum12, '0100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum15, '11111', 'incorrect checksum for given entropy')
        self.assertEqual(checksum18, '111100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum21, '1101100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum24, '10010101', 'incorrect checksum for given entropy')

    def test_mnemonic_words_from_entropy(self):
        full12 = self.entropy12 + self.m12.generate_checksum(self.entropy12)
        full15 = self.entropy15 + self.m15.generate_checksum(self.entropy15)
        full18 = self.entropy18 + self.m18.generate_checksum(self.entropy18)
        full21 = self.entropy21 + self.m21.generate_checksum(self.entropy21)
        full24 = self.entropy24 + self.m24.generate_checksum(self.entropy24)

        mnemonic12 = self.m12.to_mnemonic(full12)
        mnemonic15 = self.m15.to_mnemonic(full15)
        mnemonic18 = self.m18.to_mnemonic(full18)
        mnemonic21 = self.m21.to_mnemonic(full21)
        mnemonic24 = self.m24.to_mnemonic(full24)

        self.assertEqual(mnemonic12, 'sample tooth steak column crime rib woman budget job inch throw dog', 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic15, 'champion bounce rescue patient jeans daring section orange gather shrimp despair cabin cake odor morning', 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic18, 'produce bargain corn gloom game exhaust major equal soon frequent truly canoe sort accuse trend retreat wrestle moon', 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic21, 'catalog depart student bind sand pioneer library deer again muscle profit guitar battle laptop song venue attack combine fog afraid pulse', 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic24, 'party injury base february good green arrest boost life theory always shiver client quantum trouble verb airport tool cause correct damage utility play famous', 'incorrect mnemonic words for given entropy + checksum')

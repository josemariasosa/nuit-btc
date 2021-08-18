#!/usr/bin/env python3
# coding=utf-8

import unittest

from key.mnemonic import Mnemonic

class MnemonicTest(unittest.TestCase):
    """Test para la generación de palabras mnemónicas y semilla."""
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
        self.entropy12a = '00001110110110100001000111001110001101001011000110100000001010011000001100100010111000110101110100100111110101000010101011000101'

        self.mnemonic12 = 'sample tooth steak column crime rib woman budget job inch throw dog'
        self.mnemonic15 = 'champion bounce rescue patient jeans daring section orange gather shrimp despair cabin cake odor morning'
        self.mnemonic18 = 'produce bargain corn gloom game exhaust major equal soon frequent truly canoe sort accuse trend retreat wrestle moon'
        self.mnemonic21 = 'catalog depart student bind sand pioneer library deer again muscle profit guitar battle laptop song venue attack combine fog afraid pulse'
        self.mnemonic24 = 'party injury base february good green arrest boost life theory always shiver client quantum trouble verb airport tool cause correct damage utility play famous'
        self.mnemonic12a = 'attract spatial inform harvest borrow below arrive fragile frog dirt apple medal'

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
        checksum12a = self.m12.generate_checksum(self.entropy12a)

        self.assertEqual(checksum12, '0100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum15, '11111', 'incorrect checksum for given entropy')
        self.assertEqual(checksum18, '111100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum21, '1101100', 'incorrect checksum for given entropy')
        self.assertEqual(checksum24, '10010101', 'incorrect checksum for given entropy')
        self.assertEqual(checksum12a, '0010', 'incorrect checksum for given entropy')

    def test_mnemonic_words_from_entropy(self):
        full12 = self.entropy12 + self.m12.generate_checksum(self.entropy12)
        full15 = self.entropy15 + self.m15.generate_checksum(self.entropy15)
        full18 = self.entropy18 + self.m18.generate_checksum(self.entropy18)
        full21 = self.entropy21 + self.m21.generate_checksum(self.entropy21)
        full24 = self.entropy24 + self.m24.generate_checksum(self.entropy24)
        full12a = self.entropy12a + self.m12.generate_checksum(self.entropy12a)

        mnemonic12 = self.m12.to_mnemonic(full12)
        mnemonic15 = self.m15.to_mnemonic(full15)
        mnemonic18 = self.m18.to_mnemonic(full18)
        mnemonic21 = self.m21.to_mnemonic(full21)
        mnemonic24 = self.m24.to_mnemonic(full24)
        mnemonic12a = self.m12.to_mnemonic(full12a)

        self.assertEqual(mnemonic12, self.mnemonic12, 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic15, self.mnemonic15, 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic18, self.mnemonic18, 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic21, self.mnemonic21, 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic24, self.mnemonic24, 'incorrect mnemonic words for given entropy + checksum')
        self.assertEqual(mnemonic12a, self.mnemonic12a, 'incorrect mnemonic words for given entropy + checksum')

    def test_the_seed_from_entroy(self):
        full12 = self.entropy12 + self.m12.generate_checksum(self.entropy12)
        full15 = self.entropy15 + self.m15.generate_checksum(self.entropy15)
        full18 = self.entropy18 + self.m18.generate_checksum(self.entropy18)
        full21 = self.entropy21 + self.m21.generate_checksum(self.entropy21)
        full24 = self.entropy24 + self.m24.generate_checksum(self.entropy24)
        full12a = self.entropy12a + self.m12.generate_checksum(self.entropy12a)

        mnemonic12 = self.m12.to_mnemonic(full12)
        mnemonic15 = self.m15.to_mnemonic(full15)
        mnemonic18 = self.m18.to_mnemonic(full18)
        mnemonic21 = self.m21.to_mnemonic(full21)
        mnemonic24 = self.m24.to_mnemonic(full24)
        mnemonic12a = self.m12.to_mnemonic(full12a)

        seed12 = self.m12.to_seed(mnemonic12)
        seed15 = self.m15.to_seed(mnemonic15)
        seed18 = self.m18.to_seed(mnemonic18)
        seed21 = self.m21.to_seed(mnemonic21)
        seed24 = self.m24.to_seed(mnemonic24)
        seed12a = self.m12.to_seed(mnemonic12a)

        self.assertEqual(seed12, '1e64005ec6246b473c7af8f59b39f1a98b493ac02a2757c7902a4f2265e4d6cb2697d1858d35cda6a404e3c1d4d46733aa8129d2c4c9b2d917faba88a77df488', 'incorrect seed for entropy')
        self.assertEqual(seed15, '1554792361ccecb40b9993e086304a6d1c00552fecda3d165f81e73b2fb017327d92d0b1b3dd8026a5d62dac570ca80c9e0811ab2ded64f51e5fde4345269c91', 'incorrect seed for entropy')
        self.assertEqual(seed18, 'c4849f37e3b4ddb8d45f901be33351038254167d60e54d683db9dd05e11d5a23ffa4620de2ea8430bdebe0c29b1aa2fb2b4834fba06de591903b951dae52a858', 'incorrect seed for entropy')
        self.assertEqual(seed21, '2b75e13a7e30c69d21d5e285040252c8a8ff1d1196ae6f44f08c59710c59ce4b2cfb84dd574e3d5dca86466e754a684ba31b4fefc8b8911f4021f8944072e759', 'incorrect seed for entropy')
        self.assertEqual(seed24, '7322a9ac96ce852a14ebd062cb5887fbb4f0aa55b7b2b8fabf7abf9d66c4a191d4fbb0b370fa9ee82209df9dfcf076b0b9eba6011dfef364e0f1addc1a659f5d', 'incorrect seed for entropy')
        self.assertEqual(seed12a, 'e2df9f8f91244f2b59e11ee922ea91c6b69d590f04bb2caf898a1fef11912ddd28688dd1b8a4e1d2a25544bf6eecdaf0aa5ea4edc655ef4b8c92ca12cca9384d', 'incorrect seed for entropy')

    def test_the_seed_from_mnemonic_with_passphrase(self):
        seed12 = self.m12.to_seed(self.mnemonic12, 'impact age real prosper moon stable')
        seed15 = self.m15.to_seed(self.mnemonic15, 'impact age real prosper moon stable')
        seed18 = self.m18.to_seed(self.mnemonic18, 'impact age real prosper moon stable')
        seed21 = self.m21.to_seed(self.mnemonic21, 'impact age real prosper moon stable')
        seed24 = self.m24.to_seed(self.mnemonic24, 'impact age real prosper moon stable')
        seed12a = self.m12.to_seed(self.mnemonic12a, 'impact age real prosper moon stable')

        self.assertEqual(seed12, '94005ed50d277cb353d9faf62edec15c3ff734bfbe374b60049724c097df5b7af247c9804ed99faa3173f4ea7ffd84c315dcf3a411d523aaeac977075e54aaa7', 'incorrect seed for entropy + passphrase')
        self.assertEqual(seed15, 'b6c42de13381a667373233e115196da21ae513e9407105bdee71e15d5b93996c824520afdbaad88a8975865c9214532401244feac364cf375a5bdd8f44a1ec4b', 'incorrect seed for entropy + passphrase')
        self.assertEqual(seed18, '87f5d688a72bdc8c7a88da9006a02bd860c59d9acb8a5b5359dc89c2b03a4783a8d29e4e9168ffc7fdc374b4477d052acb41dcc1fc3e8d2a47fa15091c21dfbc', 'incorrect seed for entropy + passphrase')
        self.assertEqual(seed21, 'da02641c6c6361bf9789e2578f03d930cf86970c3e76e031c7c1790d6459753e057c2b38b595547067dedb44ba5ec0d760180ab1c91771951b4e8b4ae16aa010', 'incorrect seed for entropy + passphrase')
        self.assertEqual(seed24, '90de6cddce732dce530079b85a0ee682f4af922402c661f8f3bba5dc1a5617e0b808169af32f639c6d3b9028702d80d4580fb37cbffc1923eb9f7dbe383e9da5', 'incorrect seed for entropy + passphrase')
        self.assertEqual(seed12a, '84b78500f9af9a3e8974b7f61fa4635906bd91f70e247340ebe7236d6be3b7fb4ab2b61b860dfa167e39d8449af4dff1cc9e4b9cb6bd6ed872f62304b0abf1e1', 'incorrect seed for entropy + passphrase')

    def test_is_valid_mnemonic(self):
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic12))
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic15))
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic18))
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic21))
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic24))
        self.assertTrue(self.m12.is_valid_mnemonic(self.mnemonic12a))

    def test_is_not_valid_mnemonic(self):
        self.assertFalse(self.m12.is_valid_mnemonic('impact age real prosper moon stable'))
        self.assertFalse(self.m12.is_valid_mnemonic('not mnemonic words column crime rib woman budget job inch throw dog'))
        self.assertFalse(self.m12.is_valid_mnemonic('attract spatial inform below borrow arrive fragile frog dirt apple medal harvest'))
        self.assertFalse(self.m12.is_valid_mnemonic('depart catalog student bind sand pioneer library deer again muscle profit guitar battle laptop song venue attack combine fog afraid pulse'))
        self.assertFalse(self.m12.is_valid_mnemonic(''))
        self.assertFalse(self.m12.is_valid_mnemonic('post earn hope'))

#!/usr/bin/env python3
# coding=utf-8

import unittest

from keys.derivation.extended import ExtendedKeys, NotValidMasterPrivateKey

class ExtendedKeysTest(unittest.TestCase):
    """Test para la generación la llave maestra."""
    def setUp(self):
        # Test vectors from https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#test-vectors
        self.seed1 = '000102030405060708090a0b0c0d0e0f'
        self.xpub1 = 'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8'
        self.xprv1 = 'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi'

        self.seed2 = 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542'
        self.xpub2 = 'xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB'
        self.xprv2 = 'xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U'

        self.seed3 = '4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be'
        self.xpub3 = 'xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13'
        self.xprv3 = 'xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6'

        self.seed4 = '3ddd5602285899a946114506157c7997e5444528f3003f6134712147db19b678'
        self.xpub4 = 'xpub661MyMwAqRbcGczjuMoRm6dXaLDEhW1u34gKenbeYqAix21mdUKJyuyu5F1rzYGVxyL6tmgBUAEPrEz92mBXjByMRiJdba9wpnN37RLLAXa'
        self.xprv4 = 'xprv9s21ZrQH143K48vGoLGRPxgo2JNkJ3J3fqkirQC2zVdk5Dgd5w14S7fRDyHH4dWNHUgkvsvNDCkvAwcSHNAQwhwgNMgZhLtQC63zxwhQmRv'

    def test_extended_keys_from_seed(self):
        ek1 = ExtendedKeys(self.seed1)
        ek2 = ExtendedKeys(self.seed2)
        ek3 = ExtendedKeys(self.seed3)
        ek4 = ExtendedKeys(self.seed4)

        self.assertEqual(ek1.xprv, self.xprv1, 'incorrect extended key')
        self.assertEqual(ek1.xpub, self.xpub1, 'incorrect extended key')

        self.assertEqual(ek2.xprv, self.xprv2, 'incorrect extended key')
        self.assertEqual(ek2.xpub, self.xpub2, 'incorrect extended key')

        self.assertEqual(ek3.xprv, self.xprv3, 'incorrect extended key')
        self.assertEqual(ek3.xpub, self.xpub3, 'incorrect extended key')

        self.assertEqual(ek4.xprv, self.xprv4, 'incorrect extended key')
        self.assertEqual(ek4.xpub, self.xpub4, 'incorrect extended key')

    def test_xpub_from_parsed_xprv(self):
        txpub1 = ExtendedKeys.parse_extended_private_key(self.xprv1).xpub
        txpub2 = ExtendedKeys.parse_extended_private_key(self.xprv2).xpub
        txpub3 = ExtendedKeys.parse_extended_private_key(self.xprv3).xpub
        txpub4 = ExtendedKeys.parse_extended_private_key(self.xprv4).xpub

        self.assertEqual(txpub1, self.xpub1, 'incorrect public key')
        self.assertEqual(txpub2, self.xpub2, 'incorrect public key')
        self.assertEqual(txpub3, self.xpub3, 'incorrect public key')
        self.assertEqual(txpub4, self.xpub4, 'incorrect public key')

    def test_invalid_xprv_for_parser(self):
        invalid_xprv1 = 'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHT'
        invalid_xprv2 = 'zprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U'

        self.assertRaises(NotValidMasterPrivateKey, ExtendedKeys.parse_extended_private_key, xprv=invalid_xprv1)
        self.assertRaises(NotValidMasterPrivateKey, ExtendedKeys.parse_extended_private_key, xprv=invalid_xprv2)

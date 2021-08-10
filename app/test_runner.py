#!/usr/bin/env python3
# coding=utf-8

print('Test Runner 🐈-₿ Wallet')

import unittest
from test.test_mnemonic import MnemonicTest
from test.test_ecdsa import (
    FieldElementTest,
    PointTest,
    ECCTest,
    SignatureTest,
    S256Test,
    PrivateKeyTest
)
from test.test_derivation import ExtendedKeysTest

mnemonic_tests = [
    'test_binary_entropy_size_from_number_of_words',
    'test_incorrect_number_of_words',
    'test_checksum_from_binary_entropy',
    'test_mnemonic_words_from_entropy',
    'test_the_seed_from_entroy',
    'test_the_seed_from_mnemonic_with_passphrase',
    'test_is_valid_mnemonic',
    'test_is_not_valid_mnemonic'
]

field_element_tests = [
    'test_ne',
    'test_add',
    'test_sub',
    'test_mul',
    'test_rmul',
    'test_pow',
    'test_div'
]

point_tests = [
    'test_ne',
    'test_on_curve',
    'test_add0',
    'test_add1',
    'test_add2'
]

ecc_tests = [
    'test_on_curve',
    'test_add',
    'test_rmul'
]

signature_tests = [
    'test_der'
]

s256_tests = [
    'test_order',
    'test_pubpoint',
    'test_verify',
    'test_sec',
    'test_address'
]

private_key_tests = [
    'test_sign',
    'test_wif'
]

extended_keys_tests = [
    'test_extended_keys_from_seed',
    'test_xpub_from_parsed_xprv',
    'test_invalid_xprv_for_parser'
]


def suite():
    suite = unittest.TestSuite()

    for test in mnemonic_tests:
        suite.addTest(MnemonicTest(test))

    for test in field_element_tests:
        suite.addTest(FieldElementTest(test))

    for test in point_tests:
        suite.addTest(PointTest(test))

    for test in ecc_tests:
        suite.addTest(ECCTest(test))

    for test in signature_tests:
        suite.addTest(SignatureTest(test))

    for test in s256_tests:
        suite.addTest(S256Test(test))

    for test in private_key_tests:
        suite.addTest(PrivateKeyTest(test))

    for test in extended_keys_tests:
        suite.addTest(ExtendedKeysTest(test))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

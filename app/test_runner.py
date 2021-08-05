#!/usr/bin/env python3
# coding=utf-8

print('Test Runner 🐈-₿ Wallet')

import unittest
from test.test_mnemonic import MnemonicTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(MnemonicTest('test_binary_entropy_size_from_number_of_words'))
    suite.addTest(MnemonicTest('test_incorrect_number_of_words'))
    suite.addTest(MnemonicTest('test_checksum_from_binary_entropy'))
    suite.addTest(MnemonicTest('test_mnemonic_words_from_entropy'))
    suite.addTest(MnemonicTest('test_the_seed_from_entroy'))
    suite.addTest(MnemonicTest('test_the_seed_from_mnemonic_with_passphrase'))
    suite.addTest(MnemonicTest('test_is_valid_mnemonic'))
    suite.addTest(MnemonicTest('test_is_not_valid_mnemonic'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

#!/usr/bin/env python3
# coding=utf-8

print('Test Runner 🐈-₿')

import unittest

from test.test_mnemonic import MnemonicTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(MnemonicTest('test_binary_entropy_size_from_number_of_words'))
    suite.addTest(MnemonicTest('test_incorrect_number_of_words'))
    suite.addTest(MnemonicTest('test_checksum_from_binary_entropy'))
    suite.addTest(MnemonicTest('test_mnemonic_words_from_entropy'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

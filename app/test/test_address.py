#!/usr/bin/env python3
# coding=utf-8

import unittest

from key.keychain import KeyChain
from key.mnemonic import Mnemonic

class AddressTest(unittest.TestCase):
    def setUp(self):
        self.test_vectors = [
            {
                'mnemonic': 'asthma unfold shoot water noodle govern employ gun sea able morning hip rifle ocean fork',
                'paths': [
                    {
                        'path': "m/44'/0'/0'/0/0",
                        'address': '1GLniMuHfGFWS6uKc7mzYcr3bUsbyesGiB',
                        'pubkey': '0222d35a90e17d0a243232aedaf3a269c1b8dbc3e64a619dece6a40ad59805a2cb',
                        'privkey_wif': 'KzvcTrgKMA5JFqBYtCt16f2BJrihUm3HswBecfv6dmoVjd8fgguo'
                    },
                    {
                        'path': "m/44'/0'/0'/0/17",
                        'address': '1AQPGrqLSee4SLWJ2MEbZsMEmPqqLQKnzr',
                        'pubkey': '02cb476926ec03375b4ef20a57a9e821eedd518466bf7e85ef131bf5e229211b46',
                        'privkey_wif': 'L3qUJDQv7A3h6RKyuXj9CQQKrxf5W6hYVDxPVr4kjtqVCJtDPZbY'
                    }
                ]
            },
            {
                'mnemonic': 'toddler unlock cereal reopen cause cargo symptom victory mother master stand update bench orbit field',
                'paths': [
                    {
                        'path': "m/44'/0'/0'/0/9",
                        'address': '1JEcBkTeLYydecfkpKpTeAdQdpZjcHC1Yt',
                        'pubkey': '025f24c35e6e16ce30910dd7d7015a14bc4c628989980b2164ecb8360022f8d027',
                        'privkey_wif': 'KxG8z3eU6iEnZRjtgfem52y2PGRrcUjCpQGXiyfvmkHxQWi8fo1S'
                    },
                    {
                        'path': "m/44'/0'/0'/0/15",
                        'address': '12Rh74uqfLq2cwDz9ZeDsB3HKdTBGvyFgd',
                        'pubkey': '038479bac32cc6a98994c5d2fc120f8d22b01bd055c962b54363ae6bc843cad5d3',
                        'privkey_wif': 'Kz7WWHiZcixrBwz8YnYjFUiNjduXUBjAB6KzdvrJrf7Hn6UY6Rnt'
                    }
                ]
            }
        ]

    def test_address_pubkey_privkey(self):
        for vector in self.test_vectors:
            seed = Mnemonic.to_seed(vector['mnemonic'])
            master = KeyChain.from_seed(seed)
            for path in vector['paths']:
                child = master.derive_child_from_path(path['path'])
                self.assertEqual(child.address, path['address'], 'Incorrect address.')
                self.assertEqual(child.pubkey.hex(), path['pubkey'], 'Incorrect pubkey.')
                self.assertEqual(child.privkey_wif, path['privkey_wif'], 'Incorrect privkey_wif.')

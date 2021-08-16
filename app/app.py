#!/usr/bin/env python3
# coding=utf-8

from keys.mnemonic.mnemonic import Mnemonic
from keys.derivation.extended import ExtendedKeys
from keys.derivation.derivation import ChildKeyDerivation
from keys.derivation.keychain import KeyChain

def main():
    m = Mnemonic("english", 12)
    # print(m.generate_user_keys())

    # mnemonic = 'weekend breeze child puppy detail assault input wish bubble junior mention destroy'
    # seed = m.to_seed(mnemonic)

    seed = '000102030405060708090a0b0c0d0e0f'
    # ek = ExtendedKeys(seed)
    # # # xpriv = ek.master_private_key
    # # # xpub = ek.master_public_key

    # # print("xpub")
    # # print(ek.xpub)
    # # print("xprv")
    # # print(ek.xprv)
    # # exit()

    # # ek = ExtendedKeys.parse_extended_private_key('xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi')
    # # print("parsed-xpub")
    # # print(ek.xpub)
    # # print("parsed-xprv")
    # # print(ek.xprv)

    # ckd = ChildKeyDerivation(ek)
    # ckd.derive_from_path()
    # # print(ckd)

    master_keys = KeyChain.from_seed(seed)
    # master_keys = KeyChain.from_xkey('xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8')

    print(master_keys.xpub)


if __name__ == '__main__':
    main()
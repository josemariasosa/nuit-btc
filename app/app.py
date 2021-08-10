#!/usr/bin/env python3
# coding=utf-8

from keys.mnemonic.mnemonic import Mnemonic
from keys.derivation.extended import ExtendedKeys
from keys.derivation.derivation import ChildKeyDerivation

def main():
    m = Mnemonic("english", 12)
    # print(m.generate_user_keys())

    mnemonic = 'weekend breeze child puppy detail assault input wish bubble junior mention destroy'
    seed = m.to_seed(mnemonic)

    # seed = '000102030405060708090a0b0c0d0e0f'
    # ek = ExtendedKeys(seed)
    # # xpriv = ek.master_private_key
    # # xpub = ek.master_public_key

    # print("xpub")
    # print(ek.xpub)
    # print("xprv")
    # print(ek.xprv)
    # exit()

    ek = ExtendedKeys.parse_extended_private_key('xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi')
    # print("parsed-xpub")
    # print(ek.xpub)
    # print("parsed-xprv")
    # print(ek.xprv)

    ckd = ChildKeyDerivation(ek)
    ckd.derive_from_path()
    # print(ckd)


if __name__ == '__main__':
    main()
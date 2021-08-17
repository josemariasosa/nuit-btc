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
    # seed = 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542'
    path = 'm/0H/1/0H/7'

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path(path)

    print('child.xprv', child.xprv)
    print('child.xpub', child.xpub)



if __name__ == '__main__':
    main()
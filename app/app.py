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
    path = 'm/0H/1'

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path(path)

    print(child.xprv)
    print('xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs')
    print('****')
    print(child.xpub)
    print('xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ')
    print('\n\n\n')

    seed = '3ddd5602285899a946114506157c7997e5444528f3003f6134712147db19b678'
    path = 'm/0H/1H'

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path(path)

    print(child.xprv)
    print('xprv9xJocDuwtYCMNAo3Zw76WENQeAS6WGXQ55RCy7tDJ8oALr4FWkuVoHJeHVAcAqiZLE7Je3vZJHxspZdFHfnBEjHqU5hG1Jaj32dVoS6XLT1')
    print('****')
    print(child.xpub)
    print('xpub6BJA1jSqiukeaesWfxe6sNK9CCGaujFFSJLomWHprUL9DePQ4JDkM5d88n49sMGJxrhpjazuXYWdMf17C9T5XnxkopaeS7jGk1GyyVziaMt')


if __name__ == '__main__':
    main()
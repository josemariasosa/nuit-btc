#!/usr/bin/env python3
# coding=utf-8

from key.mnemonic import Mnemonic
from key.keychain import KeyChain

def main():
    # m = Mnemonic("english", 12)
    # print(m.generate_user_keys())

    # mnemonic = 'weekend breeze child puppy detail assault input wish bubble junior mention destroy'
    # seed = m.to_seed(mnemonic)

    seed = '000102030405060708090a0b0c0d0e0f'
    # # seed = 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542'
    path1 = 'm/0H/1'
    path2 = 'm/0H/1/4/14'
    path3 = 'm/4/14'

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path(path1)
    child_result_1 = master.derive_child_from_path(path2)

    master2 = KeyChain.from_xkey(child.xpub)
    child_result_2 = master2.derive_child_from_path(path3)

    print(child_result_1.xpub)
    print(child_result_2.xpub)


    # print(child.xprv)
    # print('xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs')
    # print('****')
    # print(child.xpub)
    # print('xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ')
    # # print('\n\n\n')

    # xpub = 'xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ'
    # path = 'm/0/1'
    # master_pub = KeyChain.from_xkey(xpub)

    # k = master_pub.derive_child_from_path(path)
    # print(k)



if __name__ == '__main__':
    main()
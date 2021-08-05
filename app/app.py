#!/usr/bin/env python3
# coding=utf-8

from keys.mnemonic.mnemonic import Mnemonic

def main():
    m = Mnemonic("english", 12)
    # print(m.generate_user_keys())

    print(m.is_valid_mnemonic("casual taxi shove crew rebel empower size enroll dynamic neck imitate clay clerk motion borrow select around web race when laundry length name okay"))


if __name__ == '__main__':
    main()
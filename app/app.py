#!/usr/bin/env python3
# coding=utf-8

from keys.mnemonic.mnemonic import Mnemonic

def main():
    m = Mnemonic("english", 12)
    print(m.generate_user_keys())


if __name__ == '__main__':
    main()
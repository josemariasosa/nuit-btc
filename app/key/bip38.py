#!/usr/bin/env python3
# coding=utf-8

# 'BIP38: Passphrase-protected privkey 🔐'

from key.mnemonic import Mnemonic
from key.keychain import KeyChain
from key.utils import _normalize_string

from crypto.base58 import _encode_base58

# from crypto.aes256 import AESCipher


import pyaes


def bip38():


    ## bip38
    mnemonic = 'sample tooth steak column crime rib woman budget job inch throw dog'
    seed = Mnemonic.to_seed(mnemonic)

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path("m/44'/0'/0'/0/0")

    import hashlib

    # step 1
    privkey = child.privkey
    address = child.address
    addresshash = hashlib.sha256(hashlib.sha256(address.encode()).digest()).digest()

    #step 2
    passphrase = 'la nuit es belle'
    password = _normalize_string(passphrase, 'NFC').encode()

    salt = addresshash[:4]
    n=16384
    r=8
    p=8
    length=64

    derived = hashlib.scrypt(password, salt=salt, n=n, r=r, p=p, maxmem=0, dklen=64)
    derivedhalf1 = derived[:32]
    derivedhalf2 = derived[32:]

    aes = pyaes.AESModeOfOperationCTR(derivedhalf2)
    def xor(var, key):
        return bytes(a ^ b for a, b in zip(var, key))
    # step 3
    var = privkey[:16]
    key = derivedhalf1[:16]
    raw = xor(var, key)
    encryptedhalf1 = aes.encrypt(raw)

    # step 4
    var = privkey[16:]
    key = derivedhalf1[16:]
    raw = xor(var, key)
    encryptedhalf2 = aes.encrypt(raw)


    result = b'0x01'+b'0x42'+b'0x00' + salt + encryptedhalf1 + encryptedhalf2
    result = _encode_base58(result)


    print('address:', address)
    print(result)
    exit()

    "m/44'/0'/0'/0/0"
    "1N8NpkKX3y5qHMfMoCavcxRb9xALEKAyY7"
    "0411768df11424d9aab77fc6e8370cbcdda5eb843a2763d9e7dc5bb008cc869d34348140e8fc4f0e6c42f03913db9c4bb02e5e391c46f8c4d6e4bffb330b513aae"
    "6PRUbJKc2g5xfXH8nWmbnzKLsmaKPMLdEqvb85giJwcmxjw2JDUeskuSwb"
    # Do AES256Encrypt(block = bitcoinprivkey[0...15] xor derivedhalf1[0...15], key = derivedhalf2), call the 16-byte result encryptedhalf1


    print('addresshash:', addresshash)
    print('passphrase:', passphrase)
    print('derivedhalf1:', derivedhalf1)
    print('derivedhalf2:', derivedhalf2)
    exit()



# plaintext = "Text may be any length you wish, no padding is required"
# ciphertext = aes.encrypt(plaintext)

# # '''\xb6\x99\x10=\xa4\x96\x88\xd1\x89\x1co\xe6\x1d\xef;\x11\x03\xe3\xee
# #    \xa9V?wY\xbfe\xcdO\xe3\xdf\x9dV\x19\xe5\x8dk\x9fh\xb87>\xdb\xa3\xd6
# #    \x86\xf4\xbd\xb0\x97\xf1\t\x02\xe9 \xed'''
# print repr(ciphertext)

# # The counter mode of operation maintains state, so decryption requires
# # a new instance be created
# aes = pyaes.AESModeOfOperationCTR(key)
# decrypted = aes.decrypt(ciphertext)



# from crypto.base58 import _encode_base58




# Range in base58check encoding for non-EC-multiplied keys without compression (prefix 6PR):
# Minimum value: 6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi (based on 01 42 C0 plus thirty-six 00's)
# Maximum value: 6PRWdmoT1ZursVcr5NiD14p5bHrKVGPG7yeEoEeRb8FVaqYSHnZTLEbYsU (based on 01 42 C0 plus thirty-six FF's)
# Range in base58check encoding for non-EC-multiplied keys with compression (prefix 6PY):
# Minimum value: 6PYJxKpVnkXUsnZAfD2B5ZsZafJYNp4ezQQeCjs39494qUUXLnXijLx6LG (based on 01 42 E0 plus thirty-six 00's)
# Maximum value: 6PYXg5tGnLYdXDRZiAqXbeYxwDoTBNthbi3d61mqBxPpwZQezJTvQHsCnk (based on 01 42 E0 plus thirty-six FF's)
# Range in base58check encoding for EC-multiplied keys without compression (prefix 6Pf):
# Minimum value: 6PfKzduKZXAFXWMtJ19Vg9cSvbFg4va6U8p2VWzSjtHQCCLk3JSBpUvfpf (based on 01 43 00 plus thirty-six 00's)
# Maximum value: 6PfYiPy6Z7BQAwEHLxxrCEHrH9kasVQ95ST1NnuEnnYAJHGsgpNPQ9dTHc (based on 01 43 00 plus thirty-six FF's)
# Range in base58check encoding for EC-multiplied keys with compression (prefix 6Pn):
# Minimum value: 6PnM2wz9LHo2BEAbvoGpGjMLGXCom35XwsDQnJ7rLiRjYvCxjpLenmoBsR (based on 01 43 20 plus thirty-six 00's)
# Maximum value: 6PnZki3vKspApf2zym6Anp2jd5hiZbuaZArPfa2ePcgVf196PLGrQNyVUh (based on 01 43 20 plus thirty-six FF's)
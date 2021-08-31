#!/usr/bin/env python3
# coding=utf-8

from key.mnemonic import Mnemonic
from key.keychain import KeyChain
from key.utils import _normalize_string


def bip38():


    ## bip38
    mnemonic = 'sample tooth steak column crime rib woman budget job inch throw dog'
    seed = Mnemonic.to_seed(mnemonic)

    master = KeyChain.from_seed(seed)
    child = master.derive_child_from_path("m/44'/0'/0'/0/0")

    import hashlib

    # step 1
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

    # step 3


    print('address:', address)
    print('addresshash:', addresshash)
    print('passphrase:', passphrase)
    print('derivedhalf1:', derivedhalf1)
    print('derivedhalf2:', derivedhalf2)
    exit()




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
#!/usr/bin/env python3
# coding=utf-8

import unittest

from keys.derivation.keychain import KeyChain, NotValidMasterPrivateKey

class ExtendedKeysTest(unittest.TestCase):
    """Test para la generación la llave maestra."""
    def setUp(self):
        # Test vectors from https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#test-vectors

        # TEST VECTOR 1
        self.seed1 = '000102030405060708090a0b0c0d0e0f'
        self.xpub1 = 'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8'
        self.xprv1 = 'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi'
        
        self.path11 = 'm/0H'
        self.xpub11 = 'xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw'
        self.xprv11 = 'xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7'

        self.path12 = 'm/0H/1'
        self.xpub12 = 'xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ'
        self.xprv12 = 'xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs'

        self.path13 = 'm/0H/1/2H'
        self.xpub13 = 'xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5'
        self.xprv13 = 'xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM'

        self.path14 = 'm/0H/1/2H/2'
        self.xpub14 = 'xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV'
        self.xprv14 = 'xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334'

        self.path15 = 'm/0H/1/2H/2/1000000000'
        self.xpub15 = 'xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy'
        self.xprv15 = 'xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76'

        # TEST VECTOR 2
        self.seed2 = 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542'
        self.xpub2 = 'xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB'
        self.xprv2 = 'xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U'

        self.path21 = 'm/0'
        self.xpub21 = 'xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH'
        self.xprv21 = 'xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt'

        self.path22 = 'm/0/2147483647H'
        self.xpub22 = 'xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a'
        self.xprv22 = 'xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9'

        self.path23 = 'm/0/2147483647H/1'
        self.xpub23 = 'xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon'
        self.xprv23 = 'xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef'

        self.path24 = 'm/0/2147483647H/1/2147483646H'
        self.xpub24 = 'xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL'
        self.xprv24 = 'xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc'

        self.path25 = 'm/0/2147483647H/1/2147483646H/2'
        self.xpub25 = 'xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt'
        self.xprv25 = 'xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j'

        # TEST VECTOR 3
        self.seed3 = '4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be'
        self.xpub3 = 'xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13'
        self.xprv3 = 'xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6'

        self.path31 = 'm/0H'
        self.xpub31 = 'xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y'
        self.xprv31 = 'xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L'

        # TEST VECTOR 4
        self.seed4 = '3ddd5602285899a946114506157c7997e5444528f3003f6134712147db19b678'
        self.xpub4 = 'xpub661MyMwAqRbcGczjuMoRm6dXaLDEhW1u34gKenbeYqAix21mdUKJyuyu5F1rzYGVxyL6tmgBUAEPrEz92mBXjByMRiJdba9wpnN37RLLAXa'
        self.xprv4 = 'xprv9s21ZrQH143K48vGoLGRPxgo2JNkJ3J3fqkirQC2zVdk5Dgd5w14S7fRDyHH4dWNHUgkvsvNDCkvAwcSHNAQwhwgNMgZhLtQC63zxwhQmRv'

        self.path41 = 'm/0H'
        self.xpub41 = 'xpub69AUMk3qDBi3uW1sXgjCmVjJ2G6WQoYSnNHyzkmdCHEhSZ4tBok37xfFEqHd2AddP56Tqp4o56AePAgCjYdvpW2PU2jbUPFKsav5ut6Ch1m'
        self.xprv41 = 'xprv9vB7xEWwNp9kh1wQRfCCQMnZUEG21LpbR9NPCNN1dwhiZkjjeGRnaALmPXCX7SgjFTiCTT6bXes17boXtjq3xLpcDjzEuGLQBM5ohqkao9G'

        self.path42 = 'm/0H/1H'
        self.xpub42 = 'xpub6BJA1jSqiukeaesWfxe6sNK9CCGaujFFSJLomWHprUL9DePQ4JDkM5d88n49sMGJxrhpjazuXYWdMf17C9T5XnxkopaeS7jGk1GyyVziaMt'
        self.xprv42 = 'xprv9xJocDuwtYCMNAo3Zw76WENQeAS6WGXQ55RCy7tDJ8oALr4FWkuVoHJeHVAcAqiZLE7Je3vZJHxspZdFHfnBEjHqU5hG1Jaj32dVoS6XLT1'
        
        self.m1 = KeyChain.from_seed(self.seed1)
        self.m2 = KeyChain.from_seed(self.seed2)
        self.m3 = KeyChain.from_seed(self.seed3)
        self.m4 = KeyChain.from_seed(self.seed4)

    def test_extended_master_keys_from_seed(self):
        self.assertEqual(self.m1.xprv, self.xprv1, 'incorrect extended key')
        self.assertEqual(self.m1.xpub, self.xpub1, 'incorrect extended key')

        self.assertEqual(self.m2.xprv, self.xprv2, 'incorrect extended key')
        self.assertEqual(self.m2.xpub, self.xpub2, 'incorrect extended key')

        self.assertEqual(self.m3.xprv, self.xprv3, 'incorrect extended key')
        self.assertEqual(self.m3.xpub, self.xpub3, 'incorrect extended key')

        self.assertEqual(self.m4.xprv, self.xprv4, 'incorrect extended key')
        self.assertEqual(self.m4.xpub, self.xpub4, 'incorrect extended key')

    def test_xpub_from_parsed_xprv(self):
        txpub1 = KeyChain.from_xkey(self.xprv1).xpub
        txpub2 = KeyChain.from_xkey(self.xprv2).xpub
        txpub3 = KeyChain.from_xkey(self.xprv3).xpub
        txpub4 = KeyChain.from_xkey(self.xprv4).xpub

        self.assertEqual(txpub1, self.xpub1, 'incorrect public key')
        self.assertEqual(txpub2, self.xpub2, 'incorrect public key')
        self.assertEqual(txpub3, self.xpub3, 'incorrect public key')
        self.assertEqual(txpub4, self.xpub4, 'incorrect public key')

    def test_invalid_xprv_for_parser(self):
        invalid_xprv1 = 'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHT'
        invalid_xprv2 = 'zprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U'
        invalid_xprv3 = 'xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e'

        self.assertRaises(NotValidMasterPrivateKey, KeyChain.from_xkey, xkey=invalid_xprv1)
        self.assertRaises(NotValidMasterPrivateKey, KeyChain.from_xkey, xkey=invalid_xprv2)
        self.assertRaises(NotValidMasterPrivateKey, KeyChain.from_xkey, xkey=invalid_xprv3)

    def test_child_private_key_derivation(self):
        child11 = self.m1.derive_child_from_path(self.path11)
        child12 = self.m1.derive_child_from_path(self.path12)
        child13 = self.m1.derive_child_from_path(self.path13)
        child14 = self.m1.derive_child_from_path(self.path14)
        child15 = self.m1.derive_child_from_path(self.path15)
        child21 = self.m2.derive_child_from_path(self.path21)
        child22 = self.m2.derive_child_from_path(self.path22)
        child23 = self.m2.derive_child_from_path(self.path23)
        child24 = self.m2.derive_child_from_path(self.path24)
        child25 = self.m2.derive_child_from_path(self.path25)
        child31 = self.m3.derive_child_from_path(self.path31)
        child41 = self.m4.derive_child_from_path(self.path41)
        child42 = self.m4.derive_child_from_path(self.path42)

        self.assertEqual(child11.xpub, self.xpub11, f'incorrect child derivation: {self.path11}, {self.seed1[:5]}')
        self.assertEqual(child11.xprv, self.xprv11, f'incorrect child derivation: {self.path11}, {self.seed1[:5]}')
        self.assertEqual(child12.xpub, self.xpub12, f'incorrect child derivation: {self.path12}, {self.seed1[:5]}')
        self.assertEqual(child12.xprv, self.xprv12, f'incorrect child derivation: {self.path12}, {self.seed1[:5]}')
        self.assertEqual(child13.xpub, self.xpub13, f'incorrect child derivation: {self.path13}, {self.seed1[:5]}')
        self.assertEqual(child13.xprv, self.xprv13, f'incorrect child derivation: {self.path13}, {self.seed1[:5]}')
        self.assertEqual(child14.xpub, self.xpub14, f'incorrect child derivation: {self.path14}, {self.seed1[:5]}')
        self.assertEqual(child14.xprv, self.xprv14, f'incorrect child derivation: {self.path14}, {self.seed1[:5]}')
        self.assertEqual(child15.xpub, self.xpub15, f'incorrect child derivation: {self.path15}, {self.seed1[:5]}')
        self.assertEqual(child15.xprv, self.xprv15, f'incorrect child derivation: {self.path15}, {self.seed1[:5]}')
        self.assertEqual(child21.xpub, self.xpub21, f'incorrect child derivation: {self.path21}, {self.seed2[:5]}')
        self.assertEqual(child21.xprv, self.xprv21, f'incorrect child derivation: {self.path21}, {self.seed2[:5]}')
        self.assertEqual(child22.xpub, self.xpub22, f'incorrect child derivation: {self.path22}, {self.seed2[:5]}')
        self.assertEqual(child22.xprv, self.xprv22, f'incorrect child derivation: {self.path22}, {self.seed2[:5]}')
        self.assertEqual(child23.xpub, self.xpub23, f'incorrect child derivation: {self.path23}, {self.seed2[:5]}')
        self.assertEqual(child23.xprv, self.xprv23, f'incorrect child derivation: {self.path23}, {self.seed2[:5]}')
        self.assertEqual(child24.xpub, self.xpub24, f'incorrect child derivation: {self.path24}, {self.seed2[:5]}')
        self.assertEqual(child24.xprv, self.xprv24, f'incorrect child derivation: {self.path24}, {self.seed2[:5]}')
        self.assertEqual(child25.xpub, self.xpub25, f'incorrect child derivation: {self.path25}, {self.seed2[:5]}')
        self.assertEqual(child25.xprv, self.xprv25, f'incorrect child derivation: {self.path25}, {self.seed2[:5]}')
        self.assertEqual(child31.xpub, self.xpub31, f'incorrect child derivation: {self.path31}, {self.seed3[:5]}')
        self.assertEqual(child31.xprv, self.xprv31, f'incorrect child derivation: {self.path31}, {self.seed3[:5]}')
        self.assertEqual(child41.xpub, self.xpub41, f'incorrect child derivation: {self.path41}, {self.seed4[:5]}')
        self.assertEqual(child41.xprv, self.xprv41, f'incorrect child derivation: {self.path41}, {self.seed4[:5]}')
        self.assertEqual(child42.xpub, self.xpub42, f'incorrect child derivation: {self.path42}, {self.seed4[:5]}')
        self.assertEqual(child42.xprv, self.xprv42, f'incorrect child derivation: {self.path42}, {self.seed4[:5]}')

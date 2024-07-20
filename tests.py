#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import json

from pmtrie import *

key = 'key'
value = 'value'

FRUITS_LIST = [
  { key: 'apple[uid: 58]', value: '🍎' },
  { key: 'apricot[uid: 0]', value: '🤷' },
  { key: 'banana[uid: 218]', value: '🍌' },
  { key: 'blueberry[uid: 0]', value: '🫐' },
  { key: 'cherry[uid: 0]', value: '🍒' },
  { key: 'coconut[uid: 0]', value: '🥥' },
  { key: 'cranberry[uid: 0]', value: '🤷' },
  { key: 'fig[uid: 68267]', value: '🤷' },
  { key: 'grapefruit[uid: 0]', value: '🤷' },
  { key: 'grapes[uid: 0]', value: '🍇' },
  { key: 'guava[uid: 344]', value: '🤷' },
  { key: 'kiwi[uid: 0]', value: '🥝' },
  { key: 'kumquat[uid: 0]', value: '🤷' },
  { key: 'lemon[uid: 0]', value: '🍋' },
  { key: 'lime[uid: 0]', value: '🤷' },
  { key: 'mango[uid: 0]', value: '🥭' },
  { key: 'orange[uid: 0]', value: '🍊' },
  { key: 'papaya[uid: 0]', value: '🤷' },
  { key: 'passionfruit[uid: 0]', value: '🤷' },
  { key: 'peach[uid: 0]', value: '🍑' },
  { key: 'pear[uid: 0]', value: '🍐' },
  { key: 'pineapple[uid: 12577]', value: '🍍' },
  { key: 'plum[uid: 15492]', value: '🤷' },
  { key: 'pomegranate[uid: 0]', value: '🤷' },
  { key: 'raspberry[uid: 0]', value: '🤷' },
  { key: 'strawberry[uid: 2532]', value: '🍓' },
  { key: 'tangerine[uid: 11]', value: '🍊' },
  { key: 'tomato[uid: 83468]', value: '🍅' },
  { key: 'watermelon[uid: 0]', value: '🍉' },
  { key: 'yuzu[uid: 0]', value: '🤷' },
]

FOOBAR_LIST = [
  { key: 'foo', value: '14' },
  { key: 'bar', value: '42' },
]

class TestTrie(unittest.TestCase):

    def test_fruits(self):

        t = PMtrie.FromList(FRUITS_LIST)
        t.inspect()

        computed_value = t.hash.hex()
        target_value   = '4acd78f345a686361df77541b2e0b533f53362e36620a1fdd3a13e0b61a3b078'
        print("root hash:")
        print(f"computed: {computed_value}")
        print(f"target:   {target_value}")
        self.assertEqual(computed_value, target_value)

    def test_duplicate(self):
        with self.assertRaises(Exception) as context:
            t = PMtrie()
            t.insert('aaa', '1')
            t.insert('aaa', '2')

    def test_proof_fruits(self):
        t = PMtrie.FromList(FRUITS_LIST)
        print("root hash:", t.hash.hex())
        for i in range(len(FRUITS_LIST)):
            proof = t.prove(FRUITS_LIST[i]['key'])
            print(f"-proof of {FRUITS_LIST[i]['key']} ({FRUITS_LIST[i]['value']}) {proof.verify().hex()==t.hash.hex()}")
            self.assertEqual(proof.verify().hex(), t.hash.hex())

    def test_simple(self):
        print("test simple trie")

        t = PMtrie.FromList(FOOBAR_LIST)
        self.assertEqual(t.size, 2)

        self.assertEqual(t.hash.hex(), "69509862d51b65b26be6e56d3286d2ff00a0e8091d004721f4d2ce6918325c18")

        self.assertEqual(t.prove(FOOBAR_LIST[0]['key']).verify().hex(), t.hash.hex())
        self.assertEqual(t.prove(FOOBAR_LIST[1]['key']).verify().hex(), t.hash.hex())

        with self.assertRaises(Exception) as context:
            t.prove('ffffff')
        with self.assertRaises(Exception) as context:
            t.prove('foo ')
        with self.assertRaises(Exception) as context:
            t.prove('')

    def test_prove_insertion(self):
        print("test insertion")

        t = PMtrie.FromList(FRUITS_LIST)
        for i in range(len(FRUITS_LIST)):
            proof = t.prove(FRUITS_LIST[i]['key'])
            self.assertEqual(proof.verify().hex(), t.hash.hex())
            t_without = PMtrie.FromList(list(filter(lambda x: x['key'] != FRUITS_LIST[i]['key'], FRUITS_LIST))) 
            self.assertEqual(proof.verify(False).hex(), t_without.hash.hex())

    def test_proof_json(self):
        t = PMtrie.FromList(FRUITS_LIST)
        proof = t.prove(FRUITS_LIST[0]['key'])

        serialized_full = proof.toJSON(full=True)
        self.assertEqual(serialized_full, '{"path": "5ed71f91166242e8477758810ad103aff35313b175b1762b0efe800fa9a126d2", "value": "f09f8d8e", "steps": [{"type": "branch", "skip": 0, "neighbors": "c7bfa4472f3a98ebe0421e8f3f03adf0f7c4340dec65b4b92b1c9f0bed209eb47238ba5d16031b6bace4aee22156f5028b0ca56dc24f7247d6435292e82c039c3490a825d2e8deddf8679ce2f95f7e3a59d9c3e1af4a49b410266d21c9344d6d79519b8cdfbd053e5a86cf28a781debae71638cd77f85aad4b88869373d9dcfd"}, {"type": "leaf", "skip": 0, "neighbor": {"key": "5cddcd30a0a388cf6feb3fd6e112c96e9daf23e3a9c8a334e7044650471aaa9e", "value": "f429821ddf89c9df3c7fbb5aa6fadb6c246d75ceede53173ce59d70dde375d14"}}, {"type": "leaf", "skip": 0, "neighbor": {"key": "5e7ccfedd44c90423b191ecca1eb21dfbac865d561bace8c0f3e94ae7edf4440", "value": "7c3715aba2db74d565a6ce6cc72f20d9cb4652ddb29efe6268be15b105e40911"}}]}')

        serialized = proof.toJSON(full=True)

        proof_deserialized = PMproof.fromJSON(serialized)
        serialized_again = proof_deserialized.toJSON(full=True)
        self.assertEqual(serialized, serialized_again)

        self.assertEqual(proof_deserialized.verify().hex(), t.hash.hex())

        serialized_steps = proof.toJSON()
        self.assertEqual(serialized_steps, '[{"type": "branch", "skip": 0, "neighbors": "c7bfa4472f3a98ebe0421e8f3f03adf0f7c4340dec65b4b92b1c9f0bed209eb47238ba5d16031b6bace4aee22156f5028b0ca56dc24f7247d6435292e82c039c3490a825d2e8deddf8679ce2f95f7e3a59d9c3e1af4a49b410266d21c9344d6d79519b8cdfbd053e5a86cf28a781debae71638cd77f85aad4b88869373d9dcfd"}, {"type": "leaf", "skip": 0, "neighbor": {"key": "5cddcd30a0a388cf6feb3fd6e112c96e9daf23e3a9c8a334e7044650471aaa9e", "value": "f429821ddf89c9df3c7fbb5aa6fadb6c246d75ceede53173ce59d70dde375d14"}}, {"type": "leaf", "skip": 0, "neighbor": {"key": "5e7ccfedd44c90423b191ecca1eb21dfbac865d561bace8c0f3e94ae7edf4440", "value": "7c3715aba2db74d565a6ce6cc72f20d9cb4652ddb29efe6268be15b105e40911"}}]')

    def test_blockchain(self):

        genesis = {
                '532945de0bc268a6b89d445c97f018d1dc5bf2ac4f80bad827dafdc05df71d62': '357dc4014a70c866c01c5c0966b6c0ecebf826c0475877a92491d708d8a2a683',
                '0801de1c443d83b7436c96cc81f325583775f58bd38e43b15b93ab630c78d6b2': '0000077d6412d9d9006bd5abd01191087e7a0b41aa7e4f9b69924eda9b8d564a',
                '506ea47b608de6b67c31d4169b8dda967b889ed218d95b0b419225904cd86db2': '00000fcdcb33f425a1fae31d92a847bdc60d75cf90a132608bf9074e9675d23e',
                '5d383a0925612fb2adcca13c0b12f19b911c8f8fea6585cc81cbb3392374ea07': '000002057bf654592884cdd370317eeec835545c5b4909f15fae751b24b014db',
                '053b168c1854e78f670879fdc0da9b533e1dabead4b370874519ccc8f65ace5a': '00000d1c0cc8af18e5e69d1f43196f528af8b2b08d52467376b657b7232172a3'
                }

        t = PMtrie()
        for k,v in genesis.items():
            t.insert(bytes.fromhex(k), bytes.fromhex(v))
        self.assertEqual(t.hash.hex(), "e93fd5647f4c458e3a339c9700e1f86c66b55e133a768c32612c9f50ccdbf3f5")

        new_blockhash = bytes.fromhex("00038818db9aad8d4d11fb31308c4e20cb3b01e2079697ac95287b8196d4008b")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "e80c5162f4eca0c90213d71b63ceb30eba1d3f08f71a22561588a8e9f0880d0e")

        new_blockhash = bytes.fromhex("0000cd204248afa1b80e293d96f0e600b71b9273e80d7b88a3b8b818270611bc")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "85c7a115102a8cdb6afba047a4fefcf7b25bbed07aee92e6658d894c2b633edd")

        new_blockhash = bytes.fromhex("000fc61c50169ffe40a5e86ca21c557849e999e093d3fd16e142dc62de58e69e")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "88cd10de259ad479964d00261123cd6634b6c16dabcdd9d7154e6e7f9b8388b8")

        new_blockhash = bytes.fromhex("00037ac34b160b38ac5592addd8dd36b804259f26e754affe99ffa39aa2d6369")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "1319b3bab7470c068398af18c7e0da36d5446504d0a9359034f1a31d37dccb79")

        new_blockhash = bytes.fromhex("000367d6b92990ca97ee5484d3dbe1a87e3ff731d0a3555c06d601b3b546a697")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "a9924dfb007673d02d8504229b50f99e49659d79dff36089bc528897c33f7c9f")

        new_blockhash = bytes.fromhex("0003a9cbb12721260be94415443ec1b25f61f4b6c42a9c266da73f2a63279127")
        t.insert(digest(new_blockhash), new_blockhash)
        self.assertEqual(t.hash.hex(), "696d335e97d07e83156e4a59c14f557e45cec43293c36b1d8c8fc636093d65df")


        more_hashes = '''000d0041342a4bffbc7fc1f21a5f42ff554d1a1e663ec27455cddbbc9714aee9
0004ee95d8d590758cacf2f4d1eb4d833fbb706b05ceb11919453fee9c69c178
000112633b8efd53d07960f00812d68e1ecdbbe98c179f13c895fafbca09aefc
00028f1d6cd6e27e78dc024580dc100f7ba2c3f15e34a287c80c2b167e454d86
000c2aff038eb909c325a3b7791ec72b6772bf9effe3ea796f0665d09744eb54
000506ce62c276af014225ab568ffb9dd144b19f6e5c844601640b06c37197e5
000a2a9d2513df0ed6d2c9a795e29cc75f18762695c7aab53837cb727672df67
000d4b5df51e8d06001f538872d601f1636f194d8e16f8f9a1722d1c2dd1f683'''
        for h in more_hashes.split('\n'):
            t.insert_digest(h)

        hashes_and_proofs = [
                ["000898e5a4feaed47d252cbb86c7b3ea45e99df71a202ece8abaa0f362b241b4", "9fd8799f005f584045f438aa6df69fa1c7de7f8ee37625fe47d7a9fbf2431cc2bbd2a4f890fe39cb6284bcd8a5a28014a7da9425264b4c8c600e75911304bc8fc492d91d5f3b51af584001bb4a4426235cbe17c4c1f7f15d7cd01f1983af2b4fb4f26021e39b04d2964c6932e374aead25ca40ff53f9767c650605d1416d0d38b7afb49b45ecd2647eb7ffffd87b9f005820db43c59fc44143d4a6d3f1f6337982e84b567deacf54f24d57343f8d38b4fb3058208f616fb8c63fee1a056b09850bdab87d9b3551bad61e65506218e799e77d7cacffff"],
                ["000eb6f3ba03b7123c08ddc5b6da25df50b8b54526b7770f38c2fc683715435e", "9fd8799f005f5840ef218dde3a1fb872a11f38855212c03c19f0b294673a15e80c0575b2fdd62822ef93e32cdb5c999ecfb77422bd9cfd783380cb14b33145a01f13496f34c8e2b258407843fa1eed1db71ccd3931886edf59e6fd419f11b04317f258c61ba34f107f37a27889f2cf61d36dafb2ada45af6ddf2445df9350310955d67b88d1eec07c19cffffff"],
                ["0007ea60b9b44dac70e378e7325d3522656f4502c1a22f833c141e2451b7e28d", "9fd8799f005f58405daba41ef822123952659f7d3df7bd0f565823fff448996eb92261b323eebbb26284bcd8a5a28014a7da9425264b4c8c600e75911304bc8fc492d91d5f3b51af5840663a8ac21d45237a7f38fd5716caa421e66ed37e13e6717338b48cf7732791ebc18dabde836c090fbb295a2c5eba663979c7262b2d0671638483804cd858ee80ffffd87b9f005820e368883881bf43912ec1de8a820066b265e37ec00ffbe440067b03a97a4be4d6582090d8a10d510e7666f80f5914eb53b9a2628a3017c5e59d2acbeaf68bb506dac9ffff"]
                ]
        
        for h, expected_proof in hashes_and_proofs:
            t.insert_digest(h)
            proof = t.prove_digest(h).toCBOR()
            self.assertEqual(proof, expected_proof) 

    def test_more_proofs(self):
        t = PMtrie()
        with open("proofs.txt", "r") as f:
            for i,line in enumerate(f):
                p = line.strip().split(' ')
                t.insert_digest(p[1])
                proof = t.prove_digest(p[1]).toCBOR()
                self.assertEqual(proof, p[2])

                proof_as_list = t.prove_digest(p[1]).toCBORlist()
                proof = '9f' + ''.join(proof_as_list) + 'ff'
                self.assertEqual(proof, p[2])



if __name__ == '__main__':
    unittest.main()

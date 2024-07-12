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

if __name__ == '__main__':
    unittest.main()

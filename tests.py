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


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from pmtrie import *

class TestTrie(unittest.TestCase):

    def test_fruits(self):
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

if __name__ == '__main__':
    unittest.main()

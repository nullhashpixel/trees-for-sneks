#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @nullhashpixel
# based on: https://github.com/aiken-lang/merkle-patricia-forestry

# WARNING: untested and incomplete implementation

from helpers import *

class PMtrie:
    TYPE_ROOT   = 'root'
    TYPE_BRANCH = 'branch'
    TYPE_LEAF   = 'leaf'

    def __init__(self, prefix='', hash=None):
        self.prefix = prefix
        self.hash   = hash if hash is not None else NULL_HASH
        self.size   = 0
        self.children = None
        self.key      = None
        self.value    = None 

    def get_type(self):
        if self.key is not None and self.value is not None:
            return PMtrie.TYPE_LEAF
        elif self.children is not None:
            return PMtrie.TYPE_BRANCH
        else:
            return PMtrie.TYPE_ROOT

    @staticmethod
    def FromList(l):
        t = PMtrie()
        for d in l:
            t.insert(d['key'], d['value'])
        return t

    @staticmethod
    def ComputeHash(prefix:str, value=None, root=None):

        assert (value is not None and root is None) or (value is None and root is not None)

        if value is not None:
            is_odd = len(prefix) % 2 == 1
            head   = bytes([0x00]) + nibbles(prefix[:1]) if is_odd else bytes([0xFF])
            tail   = bytes.fromhex(prefix[1:] if is_odd else prefix)
            assert len(value) == DIGEST_LENGTH
            return digest(head + tail + value)
        else:
            return digest(nibbles(prefix) + root)


    @staticmethod
    def Leaf(prefix:str, key, value):
        d_hex = hexdigest(encode_string(key))
        assert d_hex.endswith(prefix)

        leaf = PMtrie()
        leaf.hash   = PMtrie.ComputeHash(prefix, value=digest(encode_string(value)))
        leaf.prefix = prefix
        leaf.key    = encode_string(key)
        leaf.value  = encode_string(value)

        return leaf

    @staticmethod
    def Branch(prefix:str, children):
        branch = PMtrie()
        branch.prefix = prefix
        if type(children) is list:
            assert len(children) == 16
            branch.children = children
        elif type(children) is dict:
            branch.children = [children.get(x) for x in range(16)]
        else:
            raise Exception("TypeError")

        branch.size = sum([(1 if x is not None else 0) for x in branch.children])
        assert branch.size > 1

        branch.hash = PMtrie.ComputeHash(prefix, root=merkle_root(branch.children))
        return branch
    
    def replace_with(self, new):
        self.__dict__ = new.__dict__

    def insert(self, key, value):

        if self.get_type() == PMtrie.TYPE_ROOT:
            self.replace_with(PMtrie.Leaf(to_path(key), key, value))

        elif self.get_type() == PMtrie.TYPE_LEAF:
            assert key != self.key
            assert len(self.prefix) > 0

            new_path = to_path(key)[-len(self.prefix):]

            prefix = common_prefix(self.prefix, new_path)

            this_nibble = nibble(self.prefix[len(prefix)])
            new_nibble  = nibble(new_path[len(prefix)])

            assert this_nibble != new_nibble

            leaf_l = PMtrie.Leaf(self.prefix[len(prefix)+1:], self.key, self.value)
            leaf_r = PMtrie.Leaf(new_path[len(prefix)+1:], key, value)

            self.replace_with(PMtrie.Branch(prefix, {this_nibble: leaf_l, new_nibble: leaf_r}))
        else:

            def loop(node, path, parents):
                prefix = common_prefix(node.prefix, path) if len(node.prefix) > 0 else ''
                path   = path[len(prefix):]

                this_nibble = nibble(path[0])
                if len(prefix) < len(node.prefix):
                    new_prefix = node.prefix[len(prefix):]
                    new_nibble = nibble(new_prefix[0])

                    assert new_nibble != this_nibble

                    leaf_l   = PMtrie.Leaf(path[1:], key, value)
                    branch_r = PMtrie.Branch(node.prefix[len(prefix)+1:],  node.children)

                    node.replace_with(PMtrie.Branch(prefix, {this_nibble: leaf_l, new_nibble: branch_r}))
                    return parents

                parents.insert(0, node)

                child = node.children[this_nibble]
                if child is None:
                    node.children[this_nibble] = PMtrie.Leaf(path[1:], key, value)
                    node.hash = PMtrie.ComputeHash(node.prefix, root=merkle_root(node.children))
                    return parents

                if child.get_type() == PMtrie.TYPE_LEAF:
                    child.insert(key, value)
                    node.hash = PMtrie.ComputeHash(node.prefix, root=merkle_root(node.children))
                    return parents
                else:
                    return loop(child, path[1:], parents)

            parents = loop(self, to_path(key), [])
            for p in parents:
                p.size += 1
                if p.get_type() == PMtrie.TYPE_BRANCH:
                    p.hash = PMtrie.ComputeHash(p.prefix, root=merkle_root(p.children))
            return self

    def inspect(self, level=0):
        type_symbol = {PMtrie.TYPE_ROOT: 'R', PMtrie.TYPE_BRANCH: '+', PMtrie.TYPE_LEAF: '>'}
        print(f"{' '*level}[{type_symbol[self.get_type()]}] size={self.size} {self.prefix} {decode_string(self.key)}-->{decode_string(self.value)} {'#'+self.hash.hex() if self.hash is not None else ''}")
        d_level = 4
        if self.get_type() == PMtrie.TYPE_BRANCH:
            for child in self.children:
                if child is not None:
                    child.inspect(level=level+d_level)


if __name__ == '__main__':
    t = PMtrie()
    t.insert('test','hello')
    t.insert('test2','world')
    t.insert('test3','world')
    t.insert('te3','wgdfgorld')
    t.insert('t','d')
    t.inspect()

    print("-"*80)
    t2 = PMtrie()
    t2.insert('apple[uid: 58]', '🍎')
    t2.insert('apricot[uid: 0]', '🤷')
    t2.inspect()
    t2.insert('plum[uid: 15492]', '🤷')
    t2.inspect()


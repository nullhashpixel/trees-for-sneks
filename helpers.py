from hashlib import blake2b

DIGEST_LENGTH = 32
NULL_HASH = bytes([0]*DIGEST_LENGTH)

def common_prefix(a,b):
    i=0
    while i<len(a) and i<len(b) and a[:i] == b[:i]:
        i+=1
    if a[:i] != b[:i]:
        i-=1
    return a[:i]

def nibble(c):
    return int(c,16)

def nibbles(a):
    return bytes([nibble(x) for x in a])

def encode_string(s):
    if type(s) is str:
        return s.encode('utf-8')
    elif type(s) is bytes:
        return s
    else:
        raise Exception("TypeError")

def decode_string(b):
    if type(b) is bytes:
        return b.decode('utf-8')
    elif type(b) is str:
        return b
    elif type(b) is type(None):
        return ''
    else:
        raise Exception("TypeError")

def to_path(s):
    return hexdigest(encode_string(s))

def digest(b):
    return blake2b(b, digest_size=32).digest()

def hexdigest(b):
    return blake2b(b, digest_size=32).hexdigest()

def merkle_root(children, size=16):
    nodes = [(x if type(x) is bytes else x.hash) if x is not None else NULL_HASH for x in children]
    n = len(nodes)
    assert n == size
    if n == 1:
        return nodes[0]
    assert n >= 2 and n % 2 == 0

    while True:
        for i in range(n//2):
            nodes.append(digest(nodes[0]+nodes[1]))
            nodes = nodes[2:]
        n = len(nodes)
        if n < 2:
            break
    return nodes[0]

'Create a working dictionary from scratch'

import time

_hashseed = int(time.time() * 101)

def myhash(s):
    'Deterministic string hash function'
    h = _hashseed
    for c in s:
        h = h * 17 + ord(c)
    return h

class Dict:
    'A custom dict reimplementation using seperate chaining'

    def _get_bucket(self, key):
        i = myhash(key) % self.n
        bucket = self.buckets[i]
        return bucket

    def _find_index_in_bucket(self, key, bucket):
        for i, item in enumerate(bucket):
            if key == item[0]:
                return i
        raise KeyError(key)

    def _resize(self):
        items = self.items()
        self.n = self.n * self.n
        self.buckets = [[] for x in range(self.n)]
        for key,value in items:
            self[key] = value

    def _should_resize(self):
        if len(self)/self.n >= 2/3:
            return True
        return False
        
    def __init__(self):                 # d = Dict()
        self.n = 8
        self.buckets = [[] for i in range(self.n)]

    def __setitem__(self, key, value):  # d[k] = v
        if self._should_resize():
            self._resize()
        if key in self:
            del self[key]
        bucket = self._get_bucket(key)
        bucket.append((key, value))

    def __getitem__(self, key):         # d[k]
        bucket = self._get_bucket(key)
        i = self._find_index_in_bucket(key, bucket)
        return bucket[i][1]

    def __contains__(self, key):        # k in d
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __delitem__(self, key):         # del d[k]
        bucket = self._get_bucket(key)
        i = self._find_index_in_bucket(key, bucket)
        del bucket[i]

    def __iter__(self):
        return iter([(k, self[k]) for k in self.keys()])

    def __len__(self):                  # len(d)
        return sum([len(bucket) for bucket in self.buckets])

    def clear(self):                    # d.clear()
        for bucket in self.buckets:
            bucket.clear()

    def keys(self):
        result = []
        for bucket in self.buckets:
            for key, value in bucket:
                result.append(key)
        return result

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            if not default:
                raise KeyError(key)
            return default

    def update(self, d):
        for k, v in d:
            self[k] = v

    def pop(self, key, default=None):
        try:
            old = {key: self[key]}
            del self[key]
            return old
        except KeyError:
            if not default:
                raise KeyError(key)
            return default

    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return {key: self[key]}

    def items(self):
        return [(key, self[key]) for key in self.keys()]
    
    def __repr__(self):
        pairs = ', '.join([f'{k!r}: {self[k]!r}' for k in self.keys()])
        return '{' + pairs + '}'


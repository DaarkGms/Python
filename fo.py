class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def search(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return (x, i)
            elif x.leaf:
                return None
            else:
                return self.search(k, x.child[i])
        else:
            return self.search(k, self.root)

    def insert(self, k):
        r = self.root
        if len(r.keys) == (2 * self.t) - 1:
            s = BTreeNode()
            self.root = s
            s.child.insert(0, r)
            self._split_child(s, 0)
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(r, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.child[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.child = y.child[t:(2 * t)]
            y.child = y.child[0:(t - 1)]

    def __str__(self):
        r = self.root
        return self._print_recursive(r)

    def _print_recursive(self, x, lvl=0):
        ret = ""
        if x is not None:
            ret += self._print_recursive(x.child[-1], lvl + 1)
            for i in range(len(x.keys)):
                ret += "\t" * lvl + str(x.keys[i]) + "\n"
                ret += self._print_recursive(x.child[i], lvl + 1)
        return ret

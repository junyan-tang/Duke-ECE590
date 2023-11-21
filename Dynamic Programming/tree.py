import functools
import time
import sys
sys.setrecursionlimit(20000)

class TreeNode:
    def __init__(self, val, freq, left, right):
        self.val = val
        self.freq = freq
        self.left = left
        self.right = right
        self.cost = None
        pass

    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.val)
        left = str(self.left) if self.left is not None else '()'
        right = str(self.right) if self.right is not None else '()'
        return '({} {} {})'.format(self.val, left, right)

    def computeCost(self):
        if self.cost is not None:
            return self.cost

        def helper(n, depth):
            if n is None:
                return 0
            return depth * n.freq + helper(n.left, depth + 1) + helper(n.right, depth + 1)

        self.cost = helper(self, 1)
        return self.cost

    pass


# Your code here.
def parse(filename):
    value = []
    freq = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.rstrip('\n')
        v, f = line.split(':')
        value.append(int(v))
        freq.append(int(f))
    return value, freq

def construct_tree(v, freq):
    @functools.cache
    def leastExp(l,r, depth):
        if r < l:
            return None, 0
        if l == r:
            return TreeNode(v[l], freq[l], None, None), depth * freq[l]
        res = float('inf')
        index = -1
        for i in range(l, r + 1):
            left_tree, left_val = leastExp(l, i - 1,  depth + 1)
            right_tree, right_val = leastExp(i + 1, r, depth + 1)
            total = left_val + right_val  + depth * freq[i]
            if total < res:
                res = total
                index = i
        left, _ = leastExp(l, index - 1, depth + 1)
        right, _ = leastExp(index + 1, r, depth + 1)
        node = TreeNode(v[index], freq[index], left, right)
        return node, res
    return leastExp(0, len(v) - 1, 1)


if __name__ == "__main__":
    file_name = sys.argv[1]
    node_val, node_freq = parse(file_name)
    tree, min_exp = construct_tree(node_val, node_freq)
    print(str(tree))
    print(min_exp)
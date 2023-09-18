# coding:utf-8
import bisect
from hashlib import md5

"""
from https://github.com/graphite-project/carbon 
支持hashring和多副本 

扩容
  1 使用2个hashring，双写，读取的时候还是按原来的环读
  2 对所有的key使用新环做rehash，copy数据到应该的节点上
  3 改成新环
  4 删除冗余数据
"""


class ConsistentHashRing:
    def __init__(self, nodes, replica_count=100):
        self.ring = []
        self.nodes = set()
        self.replica_count = replica_count
        for node in nodes:
            self.add_node(node)

    def compute_ring_position(self, key):
        big_hash = md5(str(key).encode("utf-8")).hexdigest()
        small_hash = int(big_hash[:4], 16)
        return small_hash

    def add_node(self, node):
        self.nodes.add(node)
        for i in range(self.replica_count):
            replica_key = "%s:%d" % (node, i)
            position = self.compute_ring_position(replica_key)
            while position in [r[0] for r in self.ring]:
                position = position + 1
            entry = (position, node)
            bisect.insort(self.ring, entry)

    def remove_node(self, node):
        self.nodes.discard(node)
        self.ring = [entry for entry in self.ring if entry[1] != node]

    def get_node(self, key):
        assert self.ring
        node = None
        node_iter = self.get_nodes(key)
        node = node_iter.next()
        node_iter.close()
        return node

    def get_nodes(self, key):
        assert self.ring
        nodes = set()
        position = self.compute_ring_position(key)
        search_entry = (position, None)
        index = bisect.bisect_left(self.ring, search_entry) % len(self.ring)
        last_index = (index - 1) % len(self.ring)
        while len(nodes) < len(self.nodes) and index != last_index:
            next_entry = self.ring[index]
            (position, next_node) = next_entry
            if next_node not in nodes:
                nodes.add(next_node)
                yield next_node
            index = (index + 1) % len(self.ring)


def test_ring_nodes(hashring):
    nodes1 = hashring.get_nodes("name")
    nodes2 = hashring.get_nodes("orangleliu")
    nodes3 = hashring.get_nodes("china")
    print(f"key: name -> {nodes1.__next__()}")
    print(f"key: orangleliu -> {nodes2.__next__()}")
    print(f"key: china -> {nodes3.__next__()}")


def test_ring():
    nodes = ["node1", "node2", "node3"]
    hashring = ConsistentHashRing(nodes=nodes, replica_count=1)
    print(f"round1, nodes: {nodes}")
    test_ring_nodes(hashring)

    print(f"\nround2, nodes: {nodes}")
    hashring.add_node("node4")
    test_ring_nodes(hashring)


if __name__ == '__main__':
    test_ring()

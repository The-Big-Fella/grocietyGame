class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

    def __repr__(self):
        return repr(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Add node at end
    def append(self, node):
        if not isinstance(node, Node):
            node = Node(node)

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.size += 1

    # Add node at beginning
    def prepend(self, node):
        if not isinstance(node, Node):
            node = Node(node)

        node.next = self.head
        self.head = node

        if self.tail is None:
            self.tail = node

        self.size += 1

    # Get by index (0-based)
    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("LinkedList index out of range")

        current = self.head
        for _ in range(index):
            current = current.next

        return current

    def getNext(self):
        if not self.head:
            return None

        node = self.head
        self.head = self.head.next
        return node

    # Make it iterable
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __repr__(self):
        values = []
        cur = self.head
        while cur:
            values.append(repr(cur.value))  # value itself, not the node
            cur = cur.next
        return f"LinkedList([{', '.join(values)}])"

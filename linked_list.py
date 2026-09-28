class Node:
    """One station of the metro line."""

    def __init__(self, name, zone):
        self.name = name      # station name, e.g. "Central Market"
        self.zone = zone      # fare zone: 1, 2 or 3
        self.prev = None      # link to the previous station
        self.next = None      # link to the next station


class DoublyLinkedList:
    """A metro line stored as a doubly linked list."""

    def __init__(self):
        self.head = None      # first station
        self.tail = None      # last station
        self.current = None   # where the train is now
        self.size = 0

    def find(self, name):
        """Return the node with this name (ignoring case) or None."""
        node = self.head
        while node is not None:
            if node.name.lower() == name.lower():
                return node
            node = node.next
        return None

    def add_at_start(self, name, zone):
        """Add a station before the head. Return the node or None if duplicated."""
        if self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        if self.head is None:                 # empty line: node is head and tail
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.next = self.head         # 1. new node points forward to old head
            self.head.prev = new_node         # 2. old head points back to new node
            self.head = new_node              # 3. head becomes the new node
        self.size += 1
        return new_node

    def add_at_end(self, name, zone):
        """Add a station after the tail. Return the node or None if duplicated."""
        if self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        if self.tail is None:                 # empty line: node is head and tail
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail         # 1. new node points back to old tail
            self.tail.next = new_node         # 2. old tail points forward to new node
            self.tail = new_node              # 3. tail becomes the new node
        self.size += 1
        return new_node

    def add_after(self, target_name, name, zone):
        """Insert a station right after target_name. Return node or None."""
        target = self.find(target_name)
        if target is None or self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        new_node.prev = target                # 1. new node looks back at target
        new_node.next = target.next           # 2. new node looks forward at target's old next
        if target.next is not None:
            target.next.prev = new_node       # 3. old next now looks back at new node
        else:
            self.tail = new_node              # target was the last station
        target.next = new_node                # 4. target now looks forward at new node
        self.size += 1
        return new_node

    def remove(self, name):
        """Remove a station. Return True if it existed."""
        node = self.find(name)
        if node is None:
            return False
        if node.prev is not None:
            node.prev.next = node.next        # skip over the removed node going forward
        else:
            self.head = node.next             # removed node was the head
        if node.next is not None:
            node.next.prev = node.prev        # skip over the removed node going backward
        else:
            self.tail = node.prev             # removed node was the tail
        if self.current is node:              # never leave the train on a deleted node
            self.current = node.next if node.next is not None else node.prev
        self.size -= 1
        return True

    def move_next(self):
        """Move the train forward. Return the new current node or None at the end."""
        if self.current is None or self.current.next is None:
            return None
        self.current = self.current.next
        return self.current

    def move_previous(self):
        """Move the train backward. Return the new current node or None at the start."""
        if self.current is None or self.current.prev is None:
            return None
        self.current = self.current.prev
        return self.current

    def go_to(self, name):
        """Place the train at a station. Return True if it exists."""
        node = self.find(name)
        if node is None:
            return False
        self.current = node
        return True

    def reverse(self):
        """Reverse the direction of the whole line by swapping prev and next."""
        node = self.head
        while node is not None:
            node.prev, node.next = node.next, node.prev
            node = node.prev                  # after the swap, the old "next" is now "prev"
        self.head, self.tail = self.tail, self.head

    def node_to_dict(self, node, index):
        """Convert a node into plain data for the frontend."""
        return {
            "name": node.name,
            "zone": node.zone,
            "prev_name": node.prev.name if node.prev is not None else None,
            "next_name": node.next.name if node.next is not None else None,
            "is_current": node is self.current,
            "index": index,
        }

    def to_list_forward(self):
        """Walk head -> tail using next."""
        result = []
        node = self.head
        index = 0
        while node is not None:
            result.append(self.node_to_dict(node, index))
            node = node.next
            index += 1
        return result

    def to_list_backward(self):
        """Walk tail -> head using prev (this proves prev works)."""
        result = []
        node = self.tail
        index = self.size - 1
        while node is not None:
            result.append(self.node_to_dict(node, index))
            node = node.prev
            index -= 1
        return result

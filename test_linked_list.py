"""Tests for the doubly linked list. Run with: python test_linked_list.py"""

from linked_list import DoublyLinkedList


def build_line(names):
    """Create a list with the given station names, in order."""
    line = DoublyLinkedList()
    for name in names:
        line.add_at_end(name, 1)
    return line


def forward_names(line):
    """Return the station names walking head -> tail."""
    names = []
    node = line.head
    while node is not None:
        names.append(node.name)
        node = node.next
    return names


def backward_names(line):
    """Return the station names walking tail -> head (uses prev)."""
    names = []
    node = line.tail
    while node is not None:
        names.append(node.name)
        node = node.prev
    return names


def test_forward_and_backward_order():
    """Several insertions at the end keep the correct order both ways."""
    line = build_line(["A", "B", "C", "D"])
    assert line.size == 4
    assert forward_names(line) == ["A", "B", "C", "D"]
    assert backward_names(line) == ["D", "C", "B", "A"]
    # backward must be exactly the reverse of forward
    assert backward_names(line) == forward_names(line)[::-1]


def test_add_at_start_and_middle():
    """Insertions at the start and in the middle keep size, head and tail."""
    line = DoublyLinkedList()
    line.add_at_end("B", 1)
    line.add_at_end("D", 1)
    line.add_at_start("A", 1)          # A B D
    line.add_after("B", "C", 1)        # A B C D
    assert line.size == 4
    assert line.head.name == "A"
    assert line.tail.name == "D"
    assert forward_names(line) == ["A", "B", "C", "D"]
    # pointers of the inserted middle node
    node_b = line.find("B")
    assert node_b.next.name == "C"
    assert node_b.next.prev.name == "B"


def test_add_after_tail_moves_tail():
    """Adding after the last station must update the tail pointer."""
    line = build_line(["A", "B"])
    line.add_after("B", "C", 1)
    assert line.tail.name == "C"
    assert forward_names(line) == ["A", "B", "C"]


def test_remove_head_tail_and_middle():
    """Removing head, tail and a middle node keeps the list consistent."""
    line = build_line(["A", "B", "C", "D"])
    assert line.remove("A") is True     # remove head
    assert line.head.name == "B"
    assert line.head.prev is None
    assert line.remove("D") is True     # remove tail
    assert line.tail.name == "C"
    assert line.tail.next is None
    assert line.remove("B") is True     # remove middle (only C left)
    assert line.size == 1
    assert line.head is line.tail
    assert forward_names(line) == ["C"]
    assert line.remove("C") is True     # remove last node
    assert line.size == 0
    assert line.head is None and line.tail is None


def test_remove_missing_returns_false():
    """Removing a station that does not exist returns False."""
    line = build_line(["A", "B"])
    assert line.remove("Z") is False
    assert line.size == 2


def test_remove_current_station():
    """The train must never stay on a deleted node."""
    line = build_line(["A", "B", "C"])
    line.go_to("B")
    assert line.remove("B") is True
    assert line.current is not None
    assert line.current.name in ("A", "C")
    assert line.size == 2


def test_move_at_edges_returns_none():
    """Moving beyond head or tail returns None without breaking anything."""
    line = build_line(["A", "B"])
    line.go_to("A")
    assert line.move_previous() is None   # already at head
    assert line.current.name == "A"
    assert line.move_next().name == "B"
    assert line.move_next() is None       # already at tail
    assert line.current.name == "B"


def test_reverse_twice_restores_order():
    """reverse() applied twice must recover the original order."""
    names = ["A", "B", "C", "D", "E"]
    line = build_line(names)
    line.go_to("C")
    line.reverse()
    assert forward_names(line) == ["E", "D", "C", "B", "A"]
    assert line.head.name == "E"
    assert line.tail.name == "A"
    assert line.current.name == "C"       # train stays on the same station
    line.reverse()
    assert forward_names(line) == names
    assert line.head.name == "A"
    assert line.tail.name == "E"


def test_empty_list_operations():
    """No operation on an empty list may raise an error."""
    line = DoublyLinkedList()
    assert line.size == 0
    assert line.head is None and line.tail is None
    assert line.find("A") is None
    assert line.remove("A") is False
    assert line.move_next() is None
    assert line.move_previous() is None
    assert line.go_to("A") is False
    assert line.to_list_forward() == []
    assert line.to_list_backward() == []
    line.reverse()                         # must not crash
    assert line.head is None and line.tail is None


def test_duplicate_names_rejected():
    """A duplicated station name must be rejected (returns None)."""
    line = DoublyLinkedList()
    assert line.add_at_end("Central", 1) is not None
    assert line.add_at_end("Central", 2) is None
    assert line.add_at_start("CENTRAL", 1) is None      # case-insensitive
    assert line.add_after("Central", "central", 1) is None
    assert line.size == 1


def test_add_after_missing_target():
    """add_after with a target that does not exist returns None."""
    line = build_line(["A"])
    assert line.add_after("Z", "B", 1) is None
    assert line.size == 1


def test_single_node_behaviour():
    """A list with one node: head == tail, train on it, safe operations."""
    line = DoublyLinkedList()
    node = line.add_at_end("Solo", 1)
    assert node is line.head and node is line.tail and node is line.current
    assert line.move_next() is None
    assert line.move_previous() is None
    assert line.remove("Solo") is True
    assert line.head is None and line.tail is None and line.current is None
    assert line.size == 0


def test_backward_is_reverse_of_forward():
    """The backward traversal must be exactly the forward traversal reversed."""
    line = build_line(["N1", "N2", "N3", "N4", "N5"])
    forward = [station["name"] for station in line.to_list_forward()]
    backward = [station["name"] for station in line.to_list_backward()]
    assert backward == forward[::-1]


def test_node_to_dict_fields():
    """Every dict returned to the frontend must carry the pointer names."""
    line = build_line(["A", "B", "C"])
    line.go_to("B")
    data = line.to_list_forward()
    assert data[0]["prev_name"] is None       # head has no previous
    assert data[0]["next_name"] == "B"
    assert data[1]["prev_name"] == "A"
    assert data[1]["next_name"] == "C"
    assert data[1]["is_current"] is True
    assert data[2]["next_name"] is None       # tail has no next
    assert data[2]["index"] == 2


if __name__ == "__main__":
    tests = [value for key, value in sorted(globals().items()) if key.startswith("test_")]
    for test in tests:
        test()
    print("All tests passed")

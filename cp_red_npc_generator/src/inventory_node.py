#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from dataclasses import dataclass, field

from item import Item
from utils import left_align


@dataclass
class InventoryNode:
    item: Item = field(default=Item)
    children: List = field(default_factory=list)

    def can_add_child(self, child: Item) -> bool:
        node_capacity: int = self.item.container_capacity
        node_size: int = sum([x.item.size_in_container for x in self.children])
        if node_size + child.size_in_container > node_capacity:
            return False

        if self.item.name not in child.requires_container:
            return False

        return True

    def add_child(self, child: Item):  # -> Optional[InventoryNode]:
        if self.can_add_child(child):
            # new_node = InventoryNode(replace(copy.deepcopy(child), id=str(uuid.uuid4())))
            # new_node = InventoryNode(copy.deepcopy(child))
            new_node = InventoryNode(child.clone())
            self.children.append(new_node)
            return new_node
        else:
            return None

    def get_all_items(self) -> List[Item]:
        items: List[Item] = [self.item]
        for inventory_node in self.children:
            items += inventory_node.get_all_items()

        return items

    def __iter__(self):
        return self._traverse(self)

    def _traverse(self, node):
        yield node
        for child in node.children:
            yield from self._traverse(child)

    def to_string(self, offset: int) -> str:
        if self.item.default_hidden and len(self.children) == 0:
            return ""

        result: str = left_align(f"{self.item.to_string(True)}", offset, "    ")

        if self.item.container_capacity != 0 and self.item.container_capacity < 100:
            result += f" [{sum([x.item.size_in_container for x in self.children])}/{self.item.container_capacity}]"

        result += "\n"

        for child in self.children:
            result += child.to_string(offset + 1)

        return result

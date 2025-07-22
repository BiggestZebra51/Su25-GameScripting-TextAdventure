from __future__ import annotations # For some reason this resolves circular refrences in type hints - https://stackoverflow.com/a/69042351
import Interactables
import Room

# Stores items and handles removing or adding items
class Inventory:
    def __init__(self):
        self.items:dict[str,Interactables.Item] = {}
    
    def item_actions(self) -> list[str]:
        return [str.capitalize(item) for item in self.items]

    def add_item(self, input_item:Interactables.Item):
        item_id = str.lower(input_item.name)
        # If the item exists in the inventory add to it's count
        inv_item = self.items.get(item_id)
        if inv_item is not None:
            inv_item.count += input_item.count
        else:
            # Otherwise append the item element
            self.items[item_id] = input_item

    def remove_item(self, item_id:str, count:int = 1):
        item_id = str.lower(item_id)

        # If the item exists in the inventory add to it's count
        if self.items.get(item_id) is not None:
            self.items[item_id].count -= count

            # if count is less than 1 then remove it from the list
            if self.items[item_id].count < 1:
                self.items.pop(item_id)

    def use_item(self, action):
        action = str.lower(action)

        # Find the item in the list
        item = self.items.get(action)
        if(item is not None):
            # Use the item
            remove = item.use_item()
            # If the item should be removed, then remove it from the list
            if(remove):
                self.items.pop(action)
    
    def display_inventory(self) -> str:
        if(len(self.items) > 0):
            output = "\n".join(["%2i %s" % (item.count, str.capitalize(item.name)) for item in list(self.items.values())])
        else:
            output = "No items"
        return output

class Player:
    def __init__(self, current_room:str):
        self.health = 20
        self.max_health = 20
        self.level = 1
        self.inventory = Inventory()
        self.current_room = current_room

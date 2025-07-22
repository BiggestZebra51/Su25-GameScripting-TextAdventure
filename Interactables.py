from __future__ import annotations # For some reason this resolves circular refrences in type hints - https://stackoverflow.com/a/69042351
import Room
import Player

class Interactable:
    def __init__(self, name: str):
        """
            Name is what the player types to interact with this object, along with what the object is displayed as
        """
        self.name = name
    def __str__(self):
        return str.upper(self.name)
    
    def interact(self, room:Room.Room, player:Player.Player) -> bool:
        """
            This should only be called from the context of a room, if this is an item in an inventory, do use_item() instead

            Input the source room, and the player object

            Output is if the interactable should be removed from the room
        """
        print("Interacted with %s!" % str(self))
        return False

class Item(Interactable):
    def __init__(self, name: str, count: int = 1):
        super().__init__(name)
        self.count = count
        
    def interact(self, room:Room.Room, player:Player.Player) -> bool:
        """
            This should only be called from the context of a room, if this is an item in an inventory, do use_item() instead

            Input the source room, and the player object

            Output is if the interactable should be removed from the room

            ---------------------------------------------------------------
            As an item, this will remove the item from the room and add it to the player inventory
        """
        player.inventory.add_item(self)
        print("Picked up %s" % str.capitalize(self.name))
        return True
    
    def use_item(self) -> bool:
        """
            This should only be called with the context of the inventory, if this is an item in a room, do interact() instead

            Input the player object
            Output is if the interactable should be removed from the inventory
        """
        print("Used item %s!" % str(self))
        return False
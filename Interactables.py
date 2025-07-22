from __future__ import annotations # For some reason this resolves circular refrences in type hints - https://stackoverflow.com/a/69042351
import Room
import Player
import random

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
    
class Note(Item):
    def __init__(self, text:str, count: int = 1):
        super().__init__("paper", count)
        self.text = text
    
    def interact(self, room:Room.Room, player:Player.Player) -> bool:
        """
            This should only be called from the context of a room, if this is an item in an inventory, do use_item() instead

            Input the source room, and the player object

            Output is if the interactable should be removed from the room

            ---------------------------------------------------------------
            As an item, this will remove the item from the room and add it to the player inventory
            As a note, this will also print the text stored on the note        
        """
        super().interact(room, player)
        print("\nYou noticed some text on the paper,\n")
        print(self.text)
        return True


class Enemy(Interactable):
    def __init__(self, name: str, max_damage:int=4, max_exp:int=32, defeated_str:str="You defeated the %s", attack_str="You attack the %s with your sword!"):
        super().__init__(name)
        self.defeated_str = defeated_str
        self.attack_str = attack_str
        self.max_damage = max_damage
        self.max_exp = max_exp

    def interact(self, room:Room.Room, player:Player.Player) -> bool:
        """
            This should only be called from the context of a room, if this is an item in an inventory, do use_item() instead

            Input the source room, and the player object

            Output is if the interactable should be removed from the room

            ---------------------------------------------------------------
            As an enemy it will 'battle' the player and hurt/level up the player
        """
        print(self.attack_str % self.name)

        damage = random.randint(0, self.max_damage)
        experience = random.randint(0, self.max_exp)

        print(self.defeated_str % self.name)
        player.damage(damage)
        player.level_up(experience)

        return True
from __future__ import annotations # For some reason this resolves circular refrences in type hints - https://stackoverflow.com/a/69042351
import Interactables
import Player
# Main room crawler
# All actions in a room are optional, you can leave at any time, but you can't go back
# Rooms are created by a description, list of interactables, and number ids of other rooms to exit to
# eg. list += new Room("This is a description, there is a ROCK and a doorway to the LEFT", [new Item("rock", 1)], {"LEFT": 4})
# A BossRoom type that forces a type of battle on enter

class Room:
    def __init__(self, desc:str, actions:list[Interactables.Interactable], exits:dict[str,str]):
        """
            Room description is reported upon entering a room, actions mentioned in the description should be in all caps to indicate so

            Things is a list of interactables belonging to this room

            Exits is a dictionary of Action to Room id, ex. LEFT might take you to room_4
        """
        
        self.desc = desc
        self.actions:dict[str,Interactables.Interactable] = {str.lower(thing.name): thing for thing in actions}
        self.exits = exits

    def describe(self) -> str:
        return self.desc
    def room_actions(self) -> list[str]:
        return [str.upper(key) for key in self.actions]
    def room_exits(self) -> list[str]:
        return [str.upper(key) for key in self.exits]
    
    def interact(self, player:Player.Player, action:str):
        action = str.lower(action)
        
        thing = self.actions.get(action)

        # Handle action
        if(thing is not None):
            # Action is a thing

            # Interact with the thing, passing the room and the player to it
            remove = thing.interact(self, player)
            # If the thing should be removed, then remove it from the list
            if(remove):
                self.actions.pop(action)
            return True
        else:
            # Action is not found
            return False
        
    def direction(self, player:Player.Player, action:str):
        action = str.lower(action)
        
        room_exit = self.exits.get(action)

        # Handle action
        if(room_exit is not None):
            # Action is an exit
            player.current_room = room_exit
            return True
        else:
            # Action is not found
            return False
from __future__ import annotations # For some reason this resolves circular refrences in type hints - https://stackoverflow.com/a/69042351
import Interactables
import Player
import random


# [InteractStr("You notice %s on the floor", ["rock", "paper"], " and ", "a ", "")]

class ActionStr:
    def __init__(self, string:str, action_ids:list[str], join:str='', prefix:str='', suffix:str=''):
        self.string = string
        self.action_ids = action_ids
        self.join = join
        self.prefix = prefix
        self.suffix = suffix

    def to_str(self, room:Room) -> str|None:
        actions = room.get_actions(self.action_ids)
        if(actions is None):
            return
        
        actions = list(filter(lambda x: not isinstance(x, Interactables.Item) or x.count > 0, actions))
        if(len(actions) == 0):
            return

        separator = self.suffix+self.join+self.prefix
        actions = self.prefix + separator.join([str.upper(action.name) for action in actions]) + self.suffix

        return self.string % actions




# Main room crawler
# All actions in a room are optional, you can leave at any time, but you can't go back
# Rooms are created by a description, list of interactables, and number ids of other rooms to exit to
# eg. list += new Room("This is a description, there is a ROCK and a doorway to the LEFT", [new Item("rock", 1)], {"LEFT": 4})
# A BossRoom type that forces a type of battle on enter

class Room:
    def __init__(self, desc:str|list[str|ActionStr], actions:list[Interactables.Interactable], exits:dict[str,str]):
        """
            Room description is reported upon entering a room, actions mentioned in the description should be in all caps to indicate so

            Things is a list of interactables belonging to this room

            Exits is a dictionary of Action to Room id, ex. LEFT might take you to room_4
        """
        self.desc = desc
        self.actions:dict[str,Interactables.Interactable] = {str.lower(thing.name): thing for thing in actions}
        self.exits = exits

    def describe(self, player:Player.Player|None = None) -> str:
        if(self.desc is str):
            return self.desc
        else:
            output = []

            for text in self.desc:
                if(isinstance(text, ActionStr)):
                    string = text.to_str(self)
                    if(string is not None):
                        output.append(string)
                else:
                    output.append(text)
            return '\n'.join(output)
        
    def room_actions(self) -> list[str]:
        return [str.upper(key) for key in self.actions]
    def room_exits(self) -> list[str]:
        return [str.upper(key) for key in self.exits]
    
    def get_actions(self, ids:list[str]) -> list[Interactables.Interactable]|None:
        # Handle array of actions
        actions:list[Interactables.Interactable] = []
        # Iterate and get each one
        for action_id in ids:
            action = self.actions.get(action_id)
            if (action is not None):
                actions.append(action)
        # Return the actions found
        if(len(actions) != 0):
            return actions
        # If no actions found return None
        return None

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

class BossRoom(Room):
    def __init__(self, desc:str|list[str|ActionStr], actions:list[Interactables.Interactable]):
        super().__init__(desc, actions, {})

    rps_actions = ["paper", "sword", "rock"]
    boss_wins = 0
    player_wins = 0
    required_wins = 3
    room_described = False
    player:Player.Player|None = None
    alt_desc = """----------------------
???? - 99999/99999 HP - LV ???
----------------------
Nothing seems to have changed...
But you feel something different
"""
    boss_win_text = """
You almost don't even realize what happened
You died.
The entity's influence escaped the dungeon and reached the planet's heart
It's over
"""
    player_win_text = """
You won, though you aren't sure how
You also don't know what would have happened if you lost
You feel it would have been much worse than the demon lord you originally came here for
They must have already perished to this entity
It's over
"""

    def describe(self, player:Player.Player|None = None) -> str:
        if(player is not None):
            self.player = player
        if(not self.room_described):
            self.room_described = True
            return super().describe()
        else:
            return self.alt_desc + "\n%i - %i\n" % (self.player_wins, self.boss_wins)

    def room_actions(self) -> list[str]:
        actions = self.get_actions(["sword","rock","paper"])
        if (actions is None):
            return []
        return [str.upper(key.name) for key in actions]
    def get_actions(self, ids:list[str]) -> list[Interactables.Interactable]|None:
            if(self.player is None):
                return None

            # Handle array of actions
            actions:list[Interactables.Interactable] = []
            # Iterate and get each one
            for action_id in ids:
                action = self.player.inventory.items.get(action_id)
                if (action is not None):
                    actions.append(action)
            # Return the actions found
            if(len(actions) != 0):
                return actions
            # If no actions found return None
            return None


    def interact(self, player:Player.Player, action:str):
        action = str.lower(action)
        
        # Handle action
        if(action in self.rps_actions):
            # If it's a sword, or we have rocks/paper to use
            if(action == "sword" or player.inventory.remove_item(action)):
                index = self.rps_actions.index(action)
                boss_index = random.randint(0,2) # 0,1,2
                print("You used %s" % action)
                print("The entity responded with %s" % self.rps_actions[boss_index])
                if(index != boss_index):
                    # Find the winner
                    boss_win = (boss_index == (index + 1)%3)
                    if(boss_win):
                        print("The entity grows stronger")
                        self.boss_wins += 1
                    else:
                        print("You feel the entity's aura lessen")
                        self.player_wins += 1
                else:
                    print("You think about your next move")
                    pass
                print("%i - %i" % (self.player_wins, self.boss_wins))
                pass
            else:
                print("You are out of %s" % action)
            
            if(self.boss_wins >= self.required_wins or self.player_wins >= self.required_wins):
                if(self.boss_wins >= self.required_wins):
                    print(self.boss_win_text)
                else:
                    print(self.player_win_text)
                player.game_over = True

            return True
        else:
            # Action is not found
            return False
    pass
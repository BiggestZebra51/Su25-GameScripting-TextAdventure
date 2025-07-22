import Room
from Player import *
from Interactables import *
# Text adventure
# Minimum 10 prompts
# Decided on Python

# Idea:
#   You are an adventurer diving through a dungeon
#   In every room there are various items and enemies
#   Some of these items are non descript rocks, paper, and scissors
#   The final battle you use these in a best of 3 rock paper scissors battle
#   It is completely optional to grab these items and the boss fight will give you some because you didn't bring any

# Commands:
# ME
#   Human - 20/20 HP - LV 5
#   -----------------------
#   1 Sword
#   5 Rocks
#   3 Paper sheets

# LOOK
#   A description of the room
#   Sometimes there might be a ROCK or some other ITEM
#   and it would be capitalized as a keyword to type for interaction
#   also something like GOBLIN and you could attack the goblin
#

# HELP
#   Lists commands you can use, probably no descriptions <- Scope

# ---------------
# SYSTEMS

# Main room crawler
# All actions in a room are optional, you can leave at any time, but you can't go back
# Rooms are created by a description, list of interactables, and number ids of other rooms to exit to
# eg. list += new Room("This is a description, there is a ROCK and a doorway to the LEFT", [new ROCK()], [new EXIT("LEFT", 4)])
# A BossRoom type that forces a type of battle on enter

# Interactable
#   An implementation of a per room command
#   This can be a monster, item, or other
#   These will be defined as their own classes implementing interactable
#   These will be available commands when in a given room

# Battle class
#   Normal combat against monsters?
#   Somewhat out of scope, if not implemented, 
#   interacting with monsters will result in instant win probably
#   or maybe random chance for how much damage taken and if you level up

# RPSBattle class
#   You use up the rocks and papers you picked up 
#   Your sword also is used but does not break (it's a good sword)
#   In this battle, it reports how many you have of each item
#   You say the item and it will decrement how many you have,
#   and random chance the opponent will pick, the outcome determined by RPS
#   Best of 3 battle 



# Initialize Rooms
# room_id -> room
rooms:dict[str,Room.Room] = {
    "starting_room": Room.Room("Welcome adventurer!\nIn the room you spot a STONE and a PAPER\nYou also notice a door to your LEFT", [Item("stone"),Item("paper"),], {"left": "end_room"}),
    "end_room": Room.Room("Upon entering the room you notice there is no where to go than BACK", [], {"back": "starting_room"})
}


# Initialize Player
player = Player.Player("starting_room")
# Add the sword
player.inventory.add_item(Item("sword"))

running = True
while running:
    # Enter current room and describe it
    room = rooms[player.current_room]
    print(room.describe())

    while True:
        # Wait for user input
        user_action = str.lower(input("> "))
        # Check if the action is global
        #   HELP -> prints this help
        #   ~~USE -> Use an item in the inventory~~
        #   ME -> Prints player information including inventory
        #   LOOK -> Prints room information, the description, interactables, and exits
        #   QUIT -> Close the game
        if(user_action == "help"):
            print("""
Global actions:
    HELP -> prints this help
    ME -> Prints player information including inventory
    LOOK -> Prints room information, the description, interactables, and exits
    QUIT -> Close the game
                """)
        elif(user_action == "me"):
            print("Human - %2i/%2i HP - LV %i" % (player.health, player.max_health, player.level))
            print("-------------------------")
            print(player.inventory.display_inventory())
        elif(user_action == "look"):
            print(room.describe())
            if(len(room.room_actions()) > 0):
                print("-------------------------\nActions:")
                print(" ".join(room.room_actions()))
            if(len(room.room_exits()) > 0):
                print("-------------------------\nDirections:")
                print(" ".join(room.room_exits()))
        elif(user_action == "quit"):
            print("Quitting the game")
            running = False
            break

        # Check if the action exists in the room
        elif(room.direction(player, user_action)):
            # Room found and entering room
            break
        elif(room.interact(player, user_action)):
            # Interacted with thing
            pass
        else:
            print("Unknown action %s!" % user_action)
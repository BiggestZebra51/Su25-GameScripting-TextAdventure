import Room
from Player import *
from Interactables import *

####################################################################################################
# Text Adventure by Jacob Crawford                                                                 #
# In this text adventure you are diving into a dungeron to save the world from a demon lord        #
# Once getting to the boss room you realize the demon lord has been replaced by an unknown entity  #
# You must save the world by defeating this unknown entity in a strange battle                     #
#                                                                                                  #
# The comments after this box are the initial plans for this project                               #
# Other code is in Interactables.py, Player.py, and Room.py                                        #
####################################################################################################




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
    "starting_room": Room.Room(
        [
            "You notice a door in FRONT of you",
            Room.ActionStr("You also spot %s by the door", ["stone", "paper"], " and ", "a ")
        ],
        [Item("stone"),Note("Warning\nDanger beyond this point!\nThis area has been declared as a Dungeon\nTurn back for your safety")],
        {"front": "first_junction","forward": "first_junction"}),
    "first_junction": Room.Room(
        [
            "You notice three doors to your LEFT, RIGHT, and BACK",
            Room.ActionStr("You also see a %s near the LEFT door.", ["skeleton"]),
            Room.ActionStr("There are a couple %ss around the room.", ["rock"]),
        ], 
        [Enemy("skeleton"),Item("rock", 3)],
        {
            "back":"starting_room",
            "left":"left_wing_upper",
            "right":"right_wing_one"}),
    "left_wing_upper": Room.Room(["This room seems fairly empty", "You can go BACK through a passage to the RIGHT"], [], 
                                 {"back":"first_junction", "right":"first_junction"}),
    "right_wing_one": Room.Room(
        [
            Room.ActionStr("There is a pack of %s in the middle of the room", ["goblins"]),
            "You notice exits in FRONT of you and to your LEFT",
            Room.ActionStr("There is %s strewn about the room", ["paper", "trash"], " and ", "some "),
        ], [Enemy("goblins", 8, 128), Item("paper", 4), Item("trash", 6)], 
        {   "front":"right_wing_two","forward":"right_wing_two",
            "left":"first_junction"}),
    "right_wing_two": Room.Room(
        [
            Room.ActionStr("There is a large %s in the corner", ["slime"]),
            "There is a metal door to your LEFT and a passage to your BACK",
            Room.ActionStr("There are also a couple %ss on the ground", ["rock"]),
        ], [Enemy("slime", 2, 128), Item("rock", 3)], {"back":"right_wing_one",
                                         "left":"descend_upper"}),
    "descend_upper": Room.Room(
        [
        "There is a metal door to your right and a ladder DOWN",
        Room.ActionStr("There are also a piece of %s by the ladder", ["paper"]),
        ], [Note("""I'm running out of food
There is a large slime stopping me from going back where I came from
But my instincts are screaming at me to not go further in
I don't know how much time I have left""", 4)], {"right":"right_wing_two",
                                        "down":"descend_lower"}),
    "descend_lower": Room.Room(
        [
            "The air down here feels thick",
            "The doorway in FRONT of you looks unstable",
            "There is a ladder UP along the wall",
            "You get the feeling you will not be able to return if you go FORWARD",
            Room.ActionStr("There is an empty %s on the ground", ["bottle"]),
        ], [Item("bottle")], {"up":"descend_upper",
                "front":"lower_corner","forward":"lower_corner"}),
    "lower_corner": Room.Room(
        [
            "There is a collapsed doorway behind you",
            "There is no going back",
            Room.ActionStr("You see a pack of %s", ["orks"])
        ], [Enemy("orks", max_damage=6, max_exp=256)], {#"back":"descend_lower",
                                       "left":"lower_junction"}),
    "lower_junction": Room.Room(
        [
            "To the RIGHT and LEFT there are some passageways",
            "To your FRONT there is a large imposing door\nYou feel a tingling on your back",
        ], [], {"right":"lower_corner",
                                         "left":"left_wing_lower",
                                         "front":"boss_room"}),
    "left_wing_lower": Room.Room(
        [
            Room.ActionStr("There is.. a %s in the middle of the room?", ["bed"]),
            "You can go BACK to the RIGHT"
        ], [Enemy("bed", 0, 1024, "You woke up and got out of the %s\nYou feel your body has adjusted to the atmosphere down here\nYou can't seem to find the bed anymore", "You decided to rest in the %s")],
        {"back":"lower_junction","right":"lower_junction"}),
    "boss_room": Room.BossRoom(
        ["""Upon entering the room your skin crawls
This- this doesn't make sense, this is not the demon lord- you don't know what this is
You LOOK and see
----------------------
???? - 99999/99999 HP - LV ???
----------------------
You're frozen in fear
You try to go BACK but you can't move

You try to steel yourself
Not just humanity but the world it's self is doomed if you die here
Feeling returns to your hands

You think you can manage to use your SWORD but you aren't sure what that could even accomplish""",
Room.ActionStr("You also have %s", ["rock", "paper"], " and ")], [])
}


# Initialize Player
player = Player.Player("starting_room")
# Add the sword
player.inventory.add_item(Item("sword"))

#### TESTING
#player.current_room = "boss_room"
#player.inventory.add_item(Item("paper", 4))
#player.inventory.add_item(Item("rock", 4))
#### TESTING

print("Welcome adventurer!\nYou are on an important mission to save the world\nAt the bottom of this dungeon you must fight an epic battle against the demon lord\nThe world rests upon your back\n\nUpon entering the dungeon,")
running = True
while running and not player.game_over:
    # Enter current room and describe it
    room = rooms[player.current_room]
    print(room.describe(player))

    while not player.game_over:
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
            print(room.describe(player))
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

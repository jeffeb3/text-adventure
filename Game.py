from Objects import *
from Worlds import *
import time
import sys
import os

def startgame():
    os.system('clear')

    hero = Hero(input("What is the hero's name?\n> "))
    hero.welcome()

    world = createWorld(hero)
    playgame(world)

def playgame(world):

    while True:
        world.describe()
        if world.gameOver:
            sys.exit()
        command = input("> ")
        os.system('clear')

        if command.startswith("help"):
            print("I'm just as clueless as you")
            continue

        if command.startswith("go") and len(command.split()) > 1:
            if world.go(command.split()[1]):
                continue
            else:
                continue

        if command.startswith("inventory"):
            world.showInventory()
            continue

        if command.startswith("quit") or command == 'q':
            print("Ok, bye!")
            sys.exit()

        print("??")

if '__main__' in __name__:
    startgame()

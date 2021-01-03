from Objects import *

class BossRoom(Location):
    def entered(self, hero):
        print("You don't have a weapon. This boss is really mean and he took all your hearts :(")
        hero.health = 0

    def getMapChar(self):
        return '\u2620'

class Kitchen(Location):
    def entered(self, hero):
        print('You found a key! It says, "Boss Key" on it')
        hero.addItem(self.key)

    def getMapChar(self):
        return '🥞️'

def createWorld(hero):

    world = World()
    world.addHero(hero)
    hero.addItem(Item("Tic Tac", 2, "Hard candies that don't fill you up, but do make your breath fresh"))

    lobby = Location("The Lobby", 0, 0,
            "This is where you started. There is a marble floor and three doors\n"
            "The doors are labelled 2, 4, 8.\n"
            "There is an equation on the wall:\n"
            "  10 - 6 = ?\n")
    world.addLocation(lobby)

    hallway = Location("Hallway", 0, 1)
    lobby.lock(hallway)
    hallwayKey = Key("Hallway Door", lobby, hallway, "Boss Key")
    world.addLocation(hallway)

    world.addLocation(BossRoom("a Boss Fight", 0, 2))

    kitchen = Kitchen("Kitchen", 1, 0,
            "There are tasty pancakes here")
    kitchen.key = hallwayKey
    world.addLocation(kitchen)

    world.addLocation(Location("West Room", -1, 0))

    return world


import math
import os

class Location(object):
    '''Basic location object'''
    def __init__(self, name, x, y, description = ""):
        self.name = name
        self.description = description
        self.connections = {}
        self.xy = (x, y)
        self.locks = []
        self.mapChar = ' '

    def shortDescribe(self):
        print("You are in {}.".format(self.name))

    def describe(self):
        print("You are in {}.".format(self.name))
        if self.description:
            print('-'*20)
            print(self.description)

    def lock(self, neighbor):
        self.locks.append(neighbor.xy)

    def getMapChar(self):
        ''' Legend coming later. But this should return a single character for the map'''
        return self.mapChar

    def entered(self, hero):
        pass

class Item(object):
    def __init__(self, name, quantity=1, description="unknown"):
        self.name = name
        self.quantity = quantity
        self.description = description

    def show(self):
        print("{} ({}): {}".format(self.name, self.quantity, self.description))

class Key(Item):
    def __init__(self, name, doorRhs, doorLhs, description="unknown key"):
        Item.__init__(self, name, 1, description)
        self.rhs = doorRhs
        self.lhs = doorLhs

    def unlocks(self, fromLocation, toLocation):
        if self.rhs == fromLocation and self.lhs == toLocation:
            return True
        if self.lhs == fromLocation and self.rhs == toLocation:
            return True
        return False

class Weapon(Item):
    def __init__(self, name, damage, description="unknown weapon"):
        Item.__init__(self, name, 1, description)
        self.damage = damage

class Hero(object):
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.health = 45
        self.lives = 20

    def welcome(self):
        os.system('clear')
        print("Welcome {}.".format(self.name))

    def showInventory(self):
        print("{}'s Inventory:".format(self.name))
        if not self.inventory:
            print("empty")
            return
        for item in self.inventory:
            item.show()

    def showHearts(self):
        numHearts = math.floor(self.health/10)
        partialHearts = self.health % 10 != 0
        print("Health: {}{}".format("\u2665"*numHearts, '\u2661'*(5-numHearts)))

    def addItem(self, item):
        self.inventory.append(item)

    def hasKey(self, fromLocation, toLocation):
        for item in self.inventory:
            if isinstance(item, Key):
                if item.unlocks(fromLocation, toLocation):
                    return True
        return False

class World(object):
    def __init__(self):
        self.locations = {}
        self.heroLocation = None
        self.gameOver = False

    def addLocation(self, location):
        if self.heroLocation is None:
            self.heroLocation = location.xy
        if location.xy in self.locations:
            raise RuntimeError("Duplicate location at {},{}".format(xy[0], xy[1]))
        self.locations[location.xy] = location

    def addHero(self, hero):
        self.hero = hero

    def describe(self):
        print("--------------------")
        self.hero.showHearts()
        print("--------------------")
        self.drawMap()
        self.here().describe()
        if self.hero.health <= 0:
            print("Game over!")
            self.gameOver = True

    def here(self):
        return self.locations[self.heroLocation]

    def drawMap(self):
        xmin = 1e9
        xmax = -1e9
        ymin = 1e9
        ymax = -1e9
        for x,y in self.locations.keys():
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

        # Print header
        mapWidth = (xmax-xmin+1)*3+2
        print(' '*(math.floor(mapWidth/2)-1) + 'map')
        print('-'*mapWidth)
        for y in range(ymax, ymin-1, -1):
            row = ' '
            for x in range(xmin, xmax+1):
                if (x,y) == self.heroLocation:
                    row += '[\u265E]'
                elif (x,y) in self.locations.keys():
                    row += '[' + self.locations[(x,y)].getMapChar() + ']'
                else:
                    row += '   '
            row += ' '
            print(row)
        print('-'*mapWidth)

    def showInventory(self):
        self.hero.showInventory()

    def tryGo(self, xy):
        if xy not in self.locations:
            print("There isn't a door there")
            return False
        if xy in self.here().locks:
            print("The door is locked")
            if self.hero.hasKey(self.here(), self.locations[xy]):
                print("But you have the key!")
            else:
                return False
        self.heroLocation = xy
        self.locations[xy].entered(self.hero)
        return True

    def go(self, command):
        if command == 'north' or command == 'up':
            return self.tryGo((self.heroLocation[0], self.heroLocation[1]+1))
        if command == 'south' or command == 'down':
            return self.tryGo((self.heroLocation[0], self.heroLocation[1]-1))
        if command == 'east' or command == 'right':
            return self.tryGo((self.heroLocation[0]+1, self.heroLocation[1]))
        if command == 'west' or command == 'left':
            return self.tryGo((self.heroLocation[0]-1, self.heroLocation[1]))
        print("Unknown direction")
        return False


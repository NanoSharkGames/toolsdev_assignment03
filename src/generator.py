import random

import maya.cmds as cmds
import generatorui

import room
import corridor


class Generator:

    def __init__(self, genui=None):

        """Constructor"""

        # Get generator UI object
        self.genui = genui

        # The max number of rooms to spawn
        self.roomMax = 10

        # The first room's x and y positions
        self.roomStartX = 0
        self.roomStartY = 0

        # The range of room widths and heights to spawn
        self.roomWidthMin = 1
        self.roomWidthMax = 2
        self.roomHeightMin = 1
        self.roomHeightMax = 2

        # Whether to create branching room paths or not
        self.branching = True

        # The current x and y that the generator is positioned at
        self.curX = 0
        self.curY = 0

        # The generator's current room that is being appended with a corridor
        self.curRoom = None

        # The number of rooms so far in the dungeon
        self.roomCount = 0
        # The number of corridors so far in the dungeon
        self.corridorCount = 0

        # The list of room objects in the dungeon
        self.roomList = []

        # The list of corridor objects in the dungeon
        self.corridorList = []

        # The list of corridor directions
        self.corridorDirections = []
        # The current corridor direction branching from the current room
        self.corridorCurDirection = ''

    def initialize_generation(self):

        # Reset all generator data to create a new dungeon
        self.reset_generator()

        # Retrieve parameters from UI

        self.roomMax = int(self.genui.roomcountle.text())

        self.roomStartX = int(self.genui.roomstartxle.text())
        self.roomStartY = int(self.genui.roomstartyle.text())

        self.roomWidthMin = int(self.genui.roomwidthminle.text())
        self.roomWidthMax = int(self.genui.roomwidthmaxle.text())
        self.roomHeightMin = int(self.genui.roomheightminle.text())
        self.roomHeightMax = int(self.genui.roomheightmaxle.text())

        self.branching = self.genui.branchingchk.isChecked()

        # Set up other needed data for processing

        self.curX = self.roomStartX
        self.curY = self.roomStartY

        # Randomize the new room's width and height
        width = random.randint(self.roomWidthMin, self.roomWidthMax)
        height = random.randint(self.roomHeightMin, self.roomHeightMax)

        # Create first room
        self.create_room(self.curX, self.curY, width, height)

    def create_room(self, roomX, roomY, roomWidth, roomHeight):

        if self.curRoom != None:
            if self.corridorCurDirection == 'NORTH':
                self.curRoom.topOpening = False
            elif self.corridorCurDirection == 'SOUTH':
                self.curRoom.bottomOpening = False
            elif self.corridorCurDirection == 'EAST':
                self.curRoom.rightOpening = False
            elif self.corridorCurDirection == 'WEST':
                self.curRoom.leftOpening = False

        # Create a room object
        _room = room.Room

        # Assign the room object's coordinates and size

        _room.roomX = roomX
        _room.roomY = roomY

        _room.roomWidth = roomWidth
        _room.roomHeight = roomHeight

        # Determine the resource name for the room plane's mesh
        roomName = 'Room' + str(self.roomCount + 1)

        # Assign the room object's mesh plane by creating one
        _room.roomMesh = cmds.polyPlane(w=roomWidth, h=roomHeight, n=roomName)

        # Move the room to its appropriate position in the dungeon
        cmds.move(roomX, 0, roomY, roomName)

        # Add the room object to the list of rooms
        self.roomList.append(_room)

        # Assign this room object as the current room
        self.curRoom = _room

        # Do the same thing as the previous room but in the opposite direction
        if self.corridorCurDirection == 'NORTH':
            self.curRoom.bottomOpening = False
        elif self.corridorCurDirection == 'SOUTH':
            self.curRoom.topOpening = False
        elif self.corridorCurDirection == 'EAST':
            self.curRoom.leftOpening = False
        elif self.corridorCurDirection == 'WEST':
            self.curRoom.rightOpening = False

        self.roomCount += 1

        # If the dungeon can spawn more rooms
        if self.roomCount < self.roomMax:

            # If the dungeon can have branching paths
            if self.branching:

                # Variables are here to not go in an infinite loop
                attempts = 0
                maxAttempts = 10

                # Pick a random room from the room list
                self.curRoom = self.roomList[random.randint(0, len(self.roomList) - 1)]

                # While the current room has NO available openings to spawn a corridor
                while self.all_directions_blocked():

                    attempts += 1

                    # Break out of loop if the attempts have been exceeded
                    if attempts <= maxAttempts:
                        # Assign a new room if attempts have NOT been exceeded
                        self.curRoom = self.roomList[random.randint(0, len(self.roomList) - 1)]
                    else:
                        self.curRoom = None
                        break

            # If a room is available, spawn a corridor and connect with another room
            if self.curRoom is not None:
                self.create_and_connect_rooms()

    def create_and_connect_rooms(self):

        self.corridorDirections.append('NORTH')
        self.corridorDirections.append('SOUTH')
        self.corridorDirections.append('EAST')
        self.corridorDirections.append('WEST')

        corridorCanBePlaced = False

        while not corridorCanBePlaced:

            if len(self.corridorDirections) > 0:
                self.corridorCurDirection = self.corridorDirections[random.randint(0, len(self.corridorDirections) - 1)]
            else:
                break

            if self.corridorCurDirection == 'NORTH':
                if self.curRoom.topOpening:
                    corridorCanBePlaced = True
            elif self.corridorCurDirection == 'SOUTH':
                if self.curRoom.bottomOpening:
                    corridorCanBePlaced = True
            elif self.corridorCurDirection == 'EAST':
                if self.curRoom.rightOpening:
                    corridorCanBePlaced = True
            elif self.corridorCurDirection == 'WEST':
                if self.curRoom.leftOpening:
                    corridorCanBePlaced = True

            self.corridorDirections.remove(self.corridorCurDirection)

        del self.corridorDirections

        if corridorCanBePlaced:

            # Randomize the new room's width and height
            newRoomWidth = random.randint(self.roomWidthMin, self.roomWidthMax)
            newRoomHeight = random.randint(self.roomHeightMin, self.roomHeightMax)

            _corridor = corridor.Corridor()

            _corridor.startingRoom = self.curRoom

            # Determine the resource name for the corridor plane's mesh
            corridorName = 'Corridor' + str(self.corridorCount + 1)

            if self.corridorCurDirection == 'NORTH' or self.corridorCurDirection == 'SOUTH':
                _corridor.corridorMesh = cmds.polyPlane(w=_corridor.corridorWidth, h=_corridor.corridorLength, n=corridorName)
            if self.corridorCurDirection == 'EAST' or self.corridorCurDirection == 'WEST':
                _corridor.corridorMesh = cmds.polyPlane(w=_corridor.corridorLength, h=_corridor.corridorWidth, n=corridorName)

            _corridor.place_corridor(self.curRoom, self.corridorCurDirection)

            if self.corridorCurDirection == 'NORTH':
                self.curY -= self.curRoom.roomHeight / 2 + _corridor.corridorLength + newRoomHeight / 2
            elif self.corridorCurDirection == 'SOUTH':
                self.curY += self.curRoom.roomHeight / 2 + _corridor.corridorLength + newRoomHeight / 2
            elif self.corridorCurDirection == 'EAST':
                self.curX -= self.curRoom.roomWidth / 2 + _corridor.corridorLength + newRoomWidth / 2
            elif self.corridorCurDirection == 'WEST':
                self.curX += self.curRoom.roomWidth / 2 + _corridor.corridorLength + newRoomWidth / 2

    def all_directions_blocked(self):

        blocked = False

        if not self.curRoom.rightOpening and not self.curRoom.leftOpening:
            if not self.curRoom.bottomOpening and not self.curRoom.topOpening:
                blocked = True

        return blocked

    def reset_generator(self):

        for rm in self.roomList:
            cmds.delete(rm)

        del self.roomList[:]

        self.roomCount = 0

        self.curRoom = None

    def reset_attributes(self):

        self.roomMax = 10

        self.roomStartX = 0
        self.roomStartY = 0

        self.roomWidthMin = 1
        self.roomWidthMax = 5

        self.roomHeightMin = 1
        self.roomHeightMax = 5

        self.branching = True
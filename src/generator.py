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
        self.roomStartX = 0.0
        self.roomStartY = 0.0

        # The range of room widths and heights to spawn
        self.roomWidthMin = 1
        self.roomWidthMax = 2
        self.roomHeightMin = 1
        self.roomHeightMax = 2

        # Whether to create branching room paths or not
        self.branching = True

        # The current x and y that the generator is positioned at
        self.curX = 0.0
        self.curY = 0.0

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

        self.roomStartX = float(self.genui.roomstartxle.text())
        self.roomStartY = float(self.genui.roomstartyle.text())

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

        # If there is a room that the generator is located at (a previous room has been created)
        if self.curRoom != None:

            # Close off openings based on corridor direction
            if self.corridorCurDirection == 'NORTH':
                self.curRoom.topOpening = False
            elif self.corridorCurDirection == 'SOUTH':
                self.curRoom.bottomOpening = False
            elif self.corridorCurDirection == 'EAST':
                self.curRoom.rightOpening = False
            elif self.corridorCurDirection == 'WEST':
                self.curRoom.leftOpening = False

        # Create a room object
        _room = room.Room(roomX, roomY)

        # Assign room's width and height
        _room.roomWidth = roomWidth
        _room.roomHeight = roomHeight

        # Determine the resource name for the room plane's mesh
        roomName = 'Room' + str(self.roomCount + 1)

        # Assign the room object's mesh plane by creating one
        _room.roomMesh = cmds.polyPlane(w=roomWidth, h=roomHeight, n=roomName)

        # Move the room to its appropriate position in the dungeon
        cmds.move(roomX, 0.0, roomY, roomName)

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

                # Update current x and y
                self.curX = self.curRoom.roomX
                self.curY = self.curRoom.roomY

                self.create_and_connect_rooms()

    def create_and_connect_rooms(self):

        # Gather all four cardinal directions

        self.corridorDirections.append('NORTH')
        self.corridorDirections.append('SOUTH')
        self.corridorDirections.append('EAST')
        self.corridorDirections.append('WEST')

        """
        Go through all cardinal directions and check where to place corridor
        until an empty opening has been spotted
        """

        corridorCanBePlaced = False

        while not corridorCanBePlaced:

            # Grab a random unexplored direction
            if len(self.corridorDirections) > 0:
                self.corridorCurDirection = self.corridorDirections[random.randint(0, len(self.corridorDirections) - 1)]
            else:
                break

            # Check for an opening in that direction from the current room

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

            # Remove the cardinal direction from the direction list as it has been explored
            self.corridorDirections.remove(self.corridorCurDirection)

        # Clear the corridor direction list for later re-population
        del self.corridorDirections[:]

        if corridorCanBePlaced:

            # Randomize the new room's width and height
            newRoomWidth = random.randint(self.roomWidthMin, self.roomWidthMax)
            newRoomHeight = random.randint(self.roomHeightMin, self.roomHeightMax)

            # Create a new corridor

            _corridor = corridor.Corridor()

            # Assign the current room as the room where the corridor branches from
            _corridor.startingRoom = self.curRoom

            # Determine the resource name for the corridor plane's mesh
            corridorName = 'Corridor' + str(self.corridorCount + 1)

            # Align corridor based on horizontal or vertical orientation
            if self.corridorCurDirection == 'NORTH' or self.corridorCurDirection == 'SOUTH':
                _corridor.corridorMesh = cmds.polyPlane(w=0.5, h=_corridor.corridorLength, n=corridorName)
            if self.corridorCurDirection == 'EAST' or self.corridorCurDirection == 'WEST':
                _corridor.corridorMesh = cmds.polyPlane(w=_corridor.corridorLength, h=0.5, n=corridorName)

            # Translate the corridor to fit perfectly between the current and future room
            _corridor.place_corridor(self.curRoom, self.corridorCurDirection)

            # Add the corridor object to the list of corridors
            self.corridorList.append(_corridor)

            self.corridorCount += 1

            # Reassign current generator x and y coordinates based on current room and new room/corridor
            if self.corridorCurDirection == 'NORTH':
                self.curY -= self.curRoom.roomHeight / 2.0 + _corridor.corridorLength + newRoomHeight / 2.0
            elif self.corridorCurDirection == 'SOUTH':
                self.curY += self.curRoom.roomHeight / 2.0 + _corridor.corridorLength + newRoomHeight / 2.0
            elif self.corridorCurDirection == 'EAST':
                self.curX += self.curRoom.roomWidth / 2.0 + _corridor.corridorLength + newRoomWidth / 2.0
            elif self.corridorCurDirection == 'WEST':
                self.curX -= self.curRoom.roomWidth / 2.0 + _corridor.corridorLength + newRoomWidth / 2.0

            self.create_room(self.curX, self.curY, newRoomWidth, newRoomHeight)

    def all_directions_blocked(self):

        # CHECKS IF A ROOM HAS ALL DIRECTIONS BLOCKED (HAS CORRIDORS CONNECTED)

        blocked = False

        if not self.curRoom.rightOpening and not self.curRoom.leftOpening:
            if not self.curRoom.bottomOpening and not self.curRoom.topOpening:
                blocked = True

        return blocked

    def reset_generator(self):

        # Resets all generator data to generate a new dungeon layout

        for rm in self.roomList:
            cmds.delete(rm.roomMesh)

        for c in self.corridorList:
            cmds.delete(c.corridorMesh)

        del self.roomList[:]
        del self.corridorList[:]

        self.roomCount = 0
        self.corridorCount = 0

        self.curRoom = None

    def reset_attributes(self):

        # Resets all generator data to populate into the Generator UI

        self.roomMax = 10

        self.roomStartX = 0
        self.roomStartY = 0

        self.roomWidthMin = 2
        self.roomWidthMax = 4

        self.roomHeightMin = 2
        self.roomHeightMax = 4

        self.branching = True
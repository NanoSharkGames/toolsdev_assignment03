import maya.cmds as cmds

import room


class Corridor(object):

    def __init__(self):

        self.corridorMesh = None

        self.startingRoom = None

        self.corridorX = 0.0
        self.corridorY = 0.0

        self.corridorWidth = 0.5
        self.corridorLength = 5

    def place_corridor(self, startingRoom, dir):

        if dir == 'NORTH':
            self.corridorX = startingRoom.roomX
            self.corridorY = startingRoom.roomY - startingRoom.roomHeight / 2 - self.corridorLength / 2

        if dir == 'SOUTH':
            self.corridorX = startingRoom.roomX
            self.corridorY = startingRoom.roomY + startingRoom.roomHeight / 2 + self.corridorLength / 2

        if dir == 'EAST':
            self.corridorX = startingRoom.roomX + startingRoom.roomWidth / 2 + self.corridorLength / 2
            self.corridorY = startingRoom.roomY

        if dir == 'WEST':
            self.corridorX = startingRoom.roomX - startingRoom.roomWidth / 2 - self.corridorLength / 2
            self.corridorY = startingRoom.roomY

        # Move the corridor to connect the original and new room
        cmds.move(self.corridorX, 0.0, self.corridorY, self.corridorMesh)
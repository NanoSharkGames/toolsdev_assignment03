class Room:

    def __init__(self, roomX=0, roomY=0):

        self.roomX = roomX
        self.roomY = roomY

        self.roomWidth = 1
        self.roomHeight = 1

        self.roomMesh = ''

        self.rightOpening = True
        self.leftOpening = True
        self.bottomOpening = True
        self.topOpening = True
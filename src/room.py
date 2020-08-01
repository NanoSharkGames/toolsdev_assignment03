class Room(object):

    def __init__(self, roomX=0.0, roomY=0.0):

        self.roomX = roomX
        self.roomY = roomY

        self.roomWidth = 1.0
        self.roomHeight = 1.0

        self.roomMesh = ''

        self.rightOpening = True
        self.leftOpening = True
        self.bottomOpening = True
        self.topOpening = True
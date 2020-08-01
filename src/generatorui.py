import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import generator

def maya_main_window():

    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class GeneratorUI(QtWidgets.QDialog):

    def __init__(self):

        """Constructor"""
        # Passing the object GeneratorUI to super()
        # Makes this line Python 2 and 3 compatible.
        super(GeneratorUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Random Dungeon Generator")
        self.resize(400, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # Create the generator
        self.gen = generator.Generator()

        # Assign this UI as the generator's UI
        self.gen.genui = self

        self.gen.reset_attributes()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        # Reset the generator's attributes on load
        self.gen.reset_attributes()

        """Create widgets for our UI"""

        # Define title widgets

        self.titlelbl = QtWidgets.QLabel("Random Dungeon Generator")
        self.titlelbl.setStyleSheet("font: bold 20px")

        # Define room max widgets

        self.roomcountlbl = QtWidgets.QLabel("Room Count")
        self.roomcountle = QtWidgets.QLineEdit()
        self.roomcountle.setText(str(self.gen.roomMax))

        # Define room start position widgets

        self.roomstartxlbl = QtWidgets.QLabel("Room Start X")
        self.roomstartxle = QtWidgets.QLineEdit()
        self.roomstartxle.setText(str(self.gen.roomStartX))
        self.roomstartylbl = QtWidgets.QLabel("Room Start Y")
        self.roomstartyle = QtWidgets.QLineEdit()
        self.roomstartyle.setText(str(self.gen.roomStartY))

        # Define room dimension widgets

        self.roomwidthminlbl = QtWidgets.QLabel("Room Width")
        self.roomwidthminle = QtWidgets.QLineEdit()
        self.roomwidthminle.setText(str(self.gen.roomWidthMin))
        self.roomwidthmaxlbl = QtWidgets.QLabel("-")
        self.roomwidthmaxle = QtWidgets.QLineEdit()
        self.roomwidthmaxle.setText(str(self.gen.roomWidthMax))

        self.roomheightminlbl = QtWidgets.QLabel("Room Height")
        self.roomheightminle = QtWidgets.QLineEdit()
        self.roomheightminle.setText(str(self.gen.roomHeightMin))
        self.roomheightmaxlbl = QtWidgets.QLabel("-")
        self.roomheightmaxle = QtWidgets.QLineEdit()
        self.roomheightmaxle.setText(str(self.gen.roomHeightMax))

        # Define branching boolean widgets

        self.branchinglbl = QtWidgets.QLabel("Branching?")
        self.branchingchk = QtWidgets.QCheckBox()
        self.branchingchk.setChecked(True)

        # Define button widgets

        self.cancelbtn = QtWidgets.QPushButton("Cancel")
        self.generatebtn = QtWidgets.QPushButton("Generate")

    def create_layouts(self):

        """Initialize labels and fields"""

        # Define room count label-and-field layout

        self.roomcountlayout = QtWidgets.QHBoxLayout()
        self.roomcountlayout.addWidget(self.roomcountlbl)
        self.roomcountlayout.addWidget(self.roomcountle)

        # Start x and y coordinates:

        # Define room Start X label-and-field layout
        self.roomstartxlayout = QtWidgets.QHBoxLayout()
        self.roomstartxlayout.addWidget(self.roomstartxlbl)
        self.roomstartxlayout.addWidget(self.roomstartxle)

        # Define room Start Y label-and-field layout
        self.roomstartylayout = QtWidgets.QHBoxLayout()
        self.roomstartylayout.addWidget(self.roomstartylbl)
        self.roomstartylayout.addWidget(self.roomstartyle)

        # Room width range:

        self.roomwidthlayout = QtWidgets.QHBoxLayout()

        # Define room width min label-and-field layout
        self.roomwidthminlayout = QtWidgets.QHBoxLayout()
        self.roomwidthminlayout.addWidget(self.roomwidthminlbl)
        self.roomwidthminlayout.addWidget(self.roomwidthminle)

        # Define room width max label-and-field layout
        self.roomwidthmaxlayout = QtWidgets.QHBoxLayout()
        self.roomwidthmaxlayout.addWidget(self.roomwidthmaxlbl)
        self.roomwidthmaxlayout.addWidget(self.roomwidthmaxle)

        # Add room width range layouts to room width layout
        self.roomwidthlayout.addLayout(self.roomwidthminlayout)
        self.roomwidthlayout.addLayout(self.roomwidthmaxlayout)

        # Room height range:

        self.roomheightlayout = QtWidgets.QHBoxLayout()

        # Define room height min label-and-field layout
        self.roomheightminlayout = QtWidgets.QHBoxLayout()
        self.roomheightminlayout.addWidget(self.roomheightminlbl)
        self.roomheightminlayout.addWidget(self.roomheightminle)

        # Define room height max label-and-field layout
        self.roomheightmaxlayout = QtWidgets.QHBoxLayout()
        self.roomheightmaxlayout.addWidget(self.roomheightmaxlbl)
        self.roomheightmaxlayout.addWidget(self.roomheightmaxle)

        # Add room height range layouts to room height layout
        self.roomheightlayout.addLayout(self.roomheightminlayout)
        self.roomheightlayout.addLayout(self.roomheightmaxlayout)

        # Define branching label-and-checkbox layout
        self.branchlayout = QtWidgets.QHBoxLayout()
        self.branchlayout.addWidget(self.branchinglbl)
        self.branchlayout.addWidget(self.branchingchk)

        # Define left column layout
        self.leftlayout = QtWidgets.QVBoxLayout()
        self.leftlayout.addLayout(self.roomcountlayout)
        self.leftlayout.addLayout(self.roomstartxlayout)
        self.leftlayout.addLayout(self.roomstartylayout)

        # Define right column layout
        self.rightlayout = QtWidgets.QVBoxLayout()
        self.rightlayout.addLayout(self.roomwidthlayout)
        self.rightlayout.addLayout(self.roomheightlayout)
        self.rightlayout.addLayout(self.branchlayout)

        # Define combined column layout
        self.bodylayout = QtWidgets.QHBoxLayout()
        self.bodylayout.addLayout(self.leftlayout)
        self.bodylayout.addLayout(self.rightlayout)

        # Define button layout
        self.buttonlayout = QtWidgets.QHBoxLayout()
        self.buttonlayout.addWidget(self.cancelbtn)
        self.buttonlayout.addWidget(self.generatebtn)

        # Define main layout
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.mainlayout.addWidget(self.titlelbl)
        self.mainlayout.addLayout(self.bodylayout)
        self.mainlayout.addLayout(self.buttonlayout)

        self.mainlayout.addStretch()

        self.setLayout(self.mainlayout)

    def create_connections(self):

        """Connects to widget signals to slots"""

        self.cancelbtn.clicked.connect(self.cancel)
        self.generatebtn.clicked.connect(self.generate)

    @QtCore.Slot()
    def cancel(self):

        """Quits the dialog"""

        self.close()

    def generate(self):

        """Generates the dungeon"""

        self.gen.initialize_generation()
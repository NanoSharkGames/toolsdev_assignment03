from PySide2 import QtWidgets

import maya.cmds as cmds

class BasicUI(QtWidgets.QDialog):

    """Basic UI Class"""

    def __init__(self):
        super(BasicUI, self).__init__()
        self.setWindowTitle("Basic UI Example")
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.fruit_cmb = QtWidgets.QComboBox()
        self.fruit_cmb.addItems(['apple', 'orange', 'banana'])

    def create_layout(self):
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow("Fruit", self.fruit_cmb)
        self.setLayout(self.layout)

if __name__ == '__main__':
    maya.core.
    app = QtWidgets.QApplication()
    window = BasicUI()
    window.show()
    app.exec_()
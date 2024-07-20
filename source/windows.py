class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.downGrade = 4
        self.isDownGrade = False

    def getGrade(self):
        return self.downGrade

    def getFlag(self):
        return self.isDownGrade

from config import DOWNGRADE_COUNT


class GameWindow:
    def __init__(self):
        self.hwnd: int = 0
        self.isAttaced: bool = False
        self.isDownGrade: bool = False
        self.downgradeCount: int = DOWNGRADE_COUNT

    def set_hwnd(self, hwnd):
        self.hwnd = hwnd

    def is_attached(self, isAttaced):
        self.isAttaced = isAttaced

    def is_downgrade(self, isDowngrade):
        self.isDownGrade = isDowngrade

    def set_downgrade_count(self, downgradeCount):
        self.downgradeCount = downgradeCount

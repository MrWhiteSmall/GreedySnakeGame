class GameTemplate:
    def initMap(self):
        pass
    def initGameParam(self):
        pass
    def initControl(self):
        pass
    def draw(self):
        pass
    def play(self):
        self.initMap()
        self.initGameParam()
        self.initControl()
        self.draw()

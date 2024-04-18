class EdgeStrategy:
    def process(self):
        pass

class EdgeStrategy1(EdgeStrategy):
    def process(self,x,y,width_edge,height_edge):
        # edge规则，撞边上就死
        game_close = False
        if x >= width_edge or x < 0 or y >= height_edge or y < 0:
            game_close = True
        return game_close,x,y
class EdgeStrategy2(EdgeStrategy):
    def process(self,x,y,width_edge,height_edge):
        # edge规则，撞边上就死
        if x >= width_edge or y >= height_edge:
            x %= width_edge
            y %= height_edge
        if x < 0 or y < 0:
            x += width_edge
            y += height_edge
        game_close = False
        return game_close,x,y
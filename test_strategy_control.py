import pygame

# 写一个控制策略的适配器，方便调用
class ControlStrategyAdapter:
    def __init__(self) -> None:
        self.control_strategy1 = ControlStrategy1()
        self.control_strategy2 = ControlStrategy2()
    def process(self,snake_len,event,snake_block,x_change,y_change):
        if snake_len == 1:
            return self.control_strategy1.process(event,snake_block,x_change,y_change)
        else:
            return self.control_strategy2.process(event,snake_block,x_change,y_change)

class ControlStrategy:
    def process(self):
        pass


# 蛇身长度为1时，允许上下，左右垂直变向
class ControlStrategy1(ControlStrategy):
    def process(self,event,snake_block,x_change,y_change):
        if event.key == pygame.K_LEFT:
            x_change = -snake_block
            y_change = 0
        elif event.key == pygame.K_RIGHT:
            x_change = snake_block
            y_change = 0
        elif event.key == pygame.K_UP:
            y_change = -snake_block
            x_change = 0
        elif event.key == pygame.K_DOWN:
            y_change = snake_block
            x_change = 0
        return x_change,y_change
# # 蛇身长度 > 1时，不允许上下，左右垂直变向
class ControlStrategy2(ControlStrategy):
    def process(self,event,snake_block,x_change,y_change):
        if event.key == pygame.K_LEFT:
            # 如果x_change大于0，说明上一个方向是向右，此时禁止向左，所以不变
            # 否则x_change <= 0，说明方向是向上或者向下或者向左，允许向左，所以变
            x_change = x_change if x_change>0 else -snake_block
            y_change = 0
        elif event.key == pygame.K_RIGHT:
            # 如果x_change小于0，说明上一个方向是向坐，此时禁止向右，所以不变
            # 否则x_change >= 0，说明方向是向上或者向下或者向右，允许向右，所以变
            x_change = x_change if x_change<0 else snake_block
            y_change = 0
        elif event.key == pygame.K_UP:
            x_change = 0
            y_change = y_change if y_change>0 else -snake_block
        elif event.key == pygame.K_DOWN:
            x_change = 0
            y_change = y_change if y_change<0 else  snake_block
        return x_change,y_change
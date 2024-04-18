import pygame

# 引入控制策略
from test_strategy_control import ControlStrategyAdapter
# 引入边界策略
from test_strategy_edge import EdgeStrategy1,EdgeStrategy2

class GameConfig:
    def __init__(self) -> None:
        # 设置游戏窗口
        self.window_width = 600
        self.window_height = 400
        self.caption = '贪吃蛇'
        # 定义颜色
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (200,200,200)
        # 游戏模式
        self.game_modes = ['电网恢恢', '循环往复']
        
        # 定义贪吃蛇和速度的大小
        self.snake_block = 10
        self.snake_speed = 15
        self.snake_list = []

        # 每个食物得分
        self.num_food = 3
        self.food_score = 10
        # 总得分
        self.score = 0

        self.button_width, self.button_height = 200, 50
        self.button_margin = 20
        self.button_rects = [
            pygame.Rect((self.window_width - self.button_width) // 2, 
                        (self.window_height - self.button_height * 2 - self.button_margin) // 2, 
                        self.button_width, self.button_height),
            pygame.Rect((self.window_width - self.button_width) // 2, 
                        (self.window_height - self.button_height) // 2, 
                        self.button_width, self.button_height)
        ]

        # 蛇的控制模式
        self.control_strategy_adapter = \
                    ControlStrategyAdapter()
        # 游戏模式
        edge_strategy1 = EdgeStrategy1()
        edge_strategy2 = EdgeStrategy2()
        self.edge_strategies = [edge_strategy1,edge_strategy2]
        self.current_edge_strategy = None
        self.selected_mode = None


import pygame
import random
# 引入游戏模板
from test_template import GameTemplate
# 引入控制策略
from test_strategy_control import ControlStrategyAdapter
# 引入边界策略
from test_strategy_edge import EdgeStrategy1,EdgeStrategy2


class GreedySnakeGame(GameTemplate):
    def __init__(self) -> None:
        super().__init__()
        # 初始化pygame
        pygame.init()

        # 设置游戏窗口
        self.window_width = 600
        self.window_height = 400
        self.caption = '贪吃蛇'
        # 定义颜色
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (200,200,200)
        # 字体
        font_name = pygame.font.match_font('fangsong')  # 获得字体文件
        self.font = pygame.font.Font(font_name, 20)  # 获取font对象（需要字体文件）
        # 游戏模式
        self.game_modes = ['电网恢恢', '循环往复']

        # 定义贪吃蛇和速度的大小
        self.snake_block = 10
        self.snake_speed = 15
        # 每个食物得分
        self.food_score = 10

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
        
    def initMap(self):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.caption)

    def initGameParam(self):
        # 游戏关闭【界面】、游戏结束【退回首页】、强制退出【退回首页】
        self.game_over = False
        self.game_close = False
        self.forced_stop = False

        # 初始化游戏设置
        # 贪吃蛇初始位置
        self.x = self.window_width / 2
        self.y = self.window_height / 2

        # 贪吃蛇初始位置和长度
        self.snake_list = [[self.x,self.y]]
        self.length_of_snake = 1

        # 贪吃蛇移动方向
        self.x_change = 0
        self.y_change = 0
        
        # 蛇的控制模式
        self.control_strategy_adapter = \
                    ControlStrategyAdapter()
        # 游戏模式
        edge_strategy1 = EdgeStrategy1()
        edge_strategy2 = EdgeStrategy2()
        self.edge_strategies = [edge_strategy1,edge_strategy2]
        self.current_edge_strategy = None
        self.selected_mode = None

        # 食物位置
        _,self.food_x,self.food_y = self.generate_food()

        self.score = 0

    def initControl(self):
        self.playing()

    def draw(self):
        pass
    
    # 生成食物
    def generate_food(self):
        game_close = False
        stop_limit_x = self.window_width - self.snake_block
        stop_limit_y = self.window_height - self.snake_block
        interval = self.snake_block
        for _ in range(1000):
            rand_x = random.randrange(0, stop_limit_x)
            food_x = round( rand_x // interval) * interval
            rand_y = random.randrange(0, stop_limit_y)
            food_y = round( rand_y // interval) * interval
            if [food_x,food_y] not in self.snake_list:
                print(f'生成食物，坐标 {food_x},{food_y}')
                return game_close,food_x,food_y
        # 没有可用位置放置食物，游戏结束
        game_close = True
        print('没有可用食物坐标')
        return game_close,-1,-1

    # 绘制按钮
    def draw_buttons(self):
        for i, rect in enumerate(self.button_rects):
            pygame.draw.rect(self.window, 
                             self.gray if rect.collidepoint(pygame.mouse.get_pos()) else self.black, 
                             rect)
            text_surface = self.font.render(self.game_modes[i], 
                                            True, self.white)
            x = rect.centerx - text_surface.get_width() // 2
            y = rect.centery - text_surface.get_height() // 2
            self.window.blit(text_surface, (x,y ))
    # 绘制贪吃蛇
    def draw_snake(self):
        for p in self.snake_list:
            pygame.draw.rect(self.window, self.black, 
                             [p[0], p[1], 
                              self.snake_block, self.snake_block])
    # 绘制食物
    def draw_food(self):
        pygame.draw.rect(self.window, self.red, 
                         [self.food_x, self.food_y, 
                          self.snake_block, self.snake_block])
    
    # 处理游戏关闭-游戏运行
    def handle_game_close(self):
        # 游戏正常结束 or 强制结束
        # 游戏结束时屏幕上显示的文字
        while self.game_close or self.forced_stop:
            self.window.fill(self.white)
            text = self.font.render(f"真厉害！得分{self.score}!Press Q-Quit or C-Play Again", 
                                    True, self.red)
            self.window.blit(text, ((self.window_width-text.get_width()) // 2, 
                                    (self.window_height-text.get_height()) // 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_over = True
                        self.game_close = False
                        self.forced_stop = False
                    if event.key == pygame.K_c:
                        self.initGameParam()
                        self.playing()
    def handle_game_running(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if not self.selected_mode and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    # 检查按钮点击
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_mode = self.game_modes[i]
                            print(f"选择了游戏模式：{self.selected_mode}")
                            self.current_edge_strategy = self.edge_strategies[i]
                            break
                if self.selected_mode and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.forced_stop = True
                    # 蛇身长度=1，允许左右变向，上下变向
                    # 蛇身长度>1，不允许左右变向
                    # 使用策略模式
                    self.x_change,self.y_change = \
                        self.control_strategy_adapter.process(self.length_of_snake,
                                                            event,self.snake_block,
                                                            self.x_change,self.y_change)
    # 处理蛇的移动，食物的生成
    def handle_snake_move(self):
        self.x += self.x_change
        self.y += self.y_change  

        # edge规则1，撞边上就死
        # edge规则2，撞边上不死，循环游走
        # 依据初始选择的策略，来处理
        self.game_close,self.x,self.y = \
            self.current_edge_strategy.process(self.x,self.y,
                                               self.window_width,self.window_height)

        # 此处的head是蛇头的下一个位置
        snake_head = [int(self.x),int(self.y)]

        # 自身碰撞逻辑，下一步的坐标已经包含在蛇身里面，游戏结束
        for i in self.snake_list[:-1]:
            if i == snake_head:
                print('自杀')
                self.game_close = True
        if not self.game_close:
            self.snake_list.insert(0,snake_head)
            if len(self.snake_list) > self.length_of_snake:
                del self.snake_list[-1]
    def handle_food_generate(self):
        # 如果吃到了事物，就重新生成
        # 如果无处生成事物，游戏结束
        if self.x==self.food_x and self.y==self.food_y:
            self.score += self.food_score
            self.game_close,self.food_x,self.food_y = \
                self.generate_food()
            if not self.game_close:
                self.length_of_snake += 1
    # 处理绘制蛇-食物
    def handle_draw(self):
        # 屏幕清空，准备绘制
        self.window.fill(self.white)
        # 绘制按钮-选择模式
        # 还没选择好模式，就先绘制按钮，选择好了再绘制游戏界面
        if not self.selected_mode:
            self.draw_buttons()
        # 若选择好了模式，再开始绘制蛇的逻辑
        else:
            self.handle_snake_move()

            self.handle_food_generate()

            ############## DRAW ##################
            self.draw_snake()
            self.draw_food()
        
        # 屏幕更新
        pygame.display.update()
    # 游戏进行中.....
    def playing(self):
        while not self.game_over:
            self.handle_game_close()
            self.handle_game_running()
            
            self.handle_draw()

            pygame.time.Clock().tick(self.snake_speed)
        pygame.quit()
        quit()  


if __name__=='__main__':
    game = GreedySnakeGame()
    game.play()

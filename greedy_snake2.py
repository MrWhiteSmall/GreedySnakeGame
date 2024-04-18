import pygame
import random
# 引入游戏模板
from test_template import GameTemplate

from test_observer import RealFood, FakeFood, Snake
from test_config import GameConfig


class GreedySnakeGame(GameTemplate):
    def __init__(self) -> None:
        super().__init__()
        # 初始化pygame
        pygame.init()

        self.config = GameConfig()
        # 字体
        font_name = pygame.font.match_font('fangsong')  # 获得字体文件
        self.font = pygame.font.Font(font_name, 20)  # 获取font对象（需要字体文件）

    def initMap(self):
        self.window = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height)
        )
        pygame.display.set_caption(self.config.caption)

    def initGameParam(self):
        # 游戏关闭【界面】、游戏结束【退回首页】、强制退出【退回首页】
        self.game_over = False
        self.game_close = False
        self.forced_stop = False

        # 重置游戏模式，重新选择
        self.config.selected_mode = None

        # 初始化贪吃蛇
        self.snake = Snake(self.config)
        # 初始化食物 = 1 real + (n-1) fake
        self.foods = []
        print('real food')
        real_food = RealFood(self.config)
        self.foods.append(real_food)
        # snake 被 realfood 监听
        self.snake.attach(real_food)
        for _ in range(self.config.num_food-1):
            print('fake food')
            fake_food = FakeFood(self.config)
            self.foods.append(fake_food)
            # realfood 被 fakefood监听
            real_food.attach(fake_food)

    def initControl(self):
        self.playing()

    def draw(self):
        pass

    # 处理游戏关闭-游戏运行
    def handle_game_close(self):
        # 游戏正常结束 or 强制结束
        # 游戏结束时屏幕上显示的文字
        while self.game_close or self.forced_stop:
            self.window.fill(self.config.white)
            text = self.font.render(
                f"真厉害！得分{self.config.score}!Press Q-Quit or C-Play Again",
                True, self.config.red)
            self.window.blit(text, ((self.config.window_width-text.get_width()) // 2,
                                    (self.config.window_height-text.get_height()) // 2))
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
            if not self.config.selected_mode and \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # 检查按钮点击
                for i, rect in enumerate(self.config.button_rects):
                    if rect.collidepoint(event.pos):
                        self.config.selected_mode = self.config.game_modes[i]
                        print(f"选择了游戏模式：{self.config.selected_mode}")
                        self.config.current_edge_strategy = \
                            self.config.edge_strategies[i]
                        break
            if self.config.selected_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.forced_stop = True
                # 蛇身长度=1，允许左右变向，上下变向
                # 蛇身长度>1，不允许左右变向
                # 使用策略模式
                self.snake.x_change, self.snake.y_change = \
                    self.config.control_strategy_adapter.process(
                        self.snake.length_of_snake,
                        event, self.config.snake_block,
                        self.snake.x_change, self.snake.y_change)
    # 绘制按钮

    def draw_buttons(self):
        for i, rect in enumerate(self.config.button_rects):
            pygame.draw.rect(self.window,
                             self.config.gray if rect.collidepoint(pygame.mouse.get_pos())
                             else self.config.black,
                             rect)
            text_surface = self.font.render(self.config.game_modes[i],
                                            True, self.config.white)
            x = rect.centerx - text_surface.get_width() // 2
            y = rect.centery - text_surface.get_height() // 2
            self.window.blit(text_surface, (x, y))
    # 绘制食物

    def draw_food(self):
        for food in self.foods:
            food.draw(self.window)
    # 处理绘制蛇-食物

    def handle_draw(self):
        # 屏幕清空，准备绘制
        self.window.fill(self.config.white)
        # 绘制按钮-选择模式
        # 还没选择好模式，就先绘制按钮，选择好了再绘制游戏界面
        if not self.config.selected_mode:
            self.draw_buttons()
        # 若选择好了模式，再开始绘制蛇的逻辑
        else:
            self.game_close = self.snake.move()

            self.snake.draw(self.window)
            self.draw_food()

        # 屏幕更新
        pygame.display.update()

    def playing(self):
        while not self.game_over:
            self.handle_game_close()
            self.handle_game_running()

            self.handle_draw()

            pygame.time.Clock().tick(self.config.snake_speed)
        pygame.quit()
        quit()

if __name__=='__main__':
    game = GreedySnakeGame()
    game.play()
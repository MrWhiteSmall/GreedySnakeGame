import random
import pygame

from test_config import GameConfig


class Food:
    def update(self):
        pass


class Subject:
    def attach(self):
        pass

    def notify(self):
        pass


class RealFood(Food):
    def __init__(self, config: GameConfig) -> None:
        super().__init__()
        self.config = config
        self.food_x = None
        self.food_y = None
        self.score = None
        self.init()

        self.fake_observers = []

    def init(self):
        self.init_score()
        self.generate_food()

    def init_score(self):
        self.score = self.config.num_food * self.config.food_score

    def generate_food(self):
        interval = self.config.snake_block
        stop_limit_x = self.config.window_width - interval
        stop_limit_y = self.config.window_height - interval
        for _ in range(1000):
            rand_x = random.randrange(0, stop_limit_x)
            food_x = round(rand_x // interval) * interval
            rand_y = random.randrange(0, stop_limit_y)
            food_y = round(rand_y // interval) * interval
            if [food_x, food_y] not in self.config.snake_list:
                print(f'生成食物，坐标 {food_x},{food_y}')
                self.food_x, self.food_y = food_x, food_y
                return True
        # 没有可用位置放置食物，游戏结束
        print('没有可用食物坐标')
        self.food_x, self.food_y = -1, -1
        return False

    # real food 提供 fake food 的监听
    # 没吃到真的，则把消息更新到假的
    # 吃到真的，则大家一起变换位置
    def attach(self, fake_observer):
        self.fake_observers.append(fake_observer)

    def notify(self, context, change=False):
        for fake in self.fake_observers:
            fake.update(context, change)

    def update(self, context):
        if context.x == self.food_x and context.y == self.food_y:
            context.config.score += self.score
            context.length_of_snake += self.config.num_food
            self.generate_food()
            # 通知到fake，吃到真的了
            self.notify(context, change=True)
        else:
            # 通知到fake，没吃到真的
            self.notify(context, change=False)

    def draw(self, window):
        snake_block = self.config.snake_block
        pygame.draw.rect(
            window, self.config.red,
            [self.food_x, self.food_y,
             snake_block, snake_block])


class FakeFood(Food):
    def __init__(self, config:GameConfig) -> None:
        super().__init__()
        self.config = config
        self.food_x = None
        self.food_y = None
        self.score = None
        self.init()

    def init(self):
        self.init_score()
        self.generate_food()

    def init_score(self):
        self.score = 0

    def generate_food(self):
        interval = self.config.snake_block
        stop_limit_x = self.config.window_width - interval
        stop_limit_y = self.config.window_height - interval
        for _ in range(1000):
            rand_x = random.randrange(0, stop_limit_x)
            food_x = round(rand_x // interval) * interval
            rand_y = random.randrange(0, stop_limit_y)
            food_y = round(rand_y // interval) * interval
            if [food_x, food_y] not in self.config.snake_list:
                print(f'生成食物，坐标 {food_x},{food_y}')
                self.food_x, self.food_y = food_x, food_y
                return True
        # 没有可用位置放置食物，游戏结束
        print('没有可用食物坐标')
        self.food_x, self.food_y = -1, -1
        return False

    # 吃到了假的，变换位置
    # 吃到了真的，变换位置
    def update(self, context, change=False):
        if change or (context.x == self.food_x and context.y == self.food_y):
            self.generate_food()

    def draw(self,window):
        snake_block = self.config.snake_block
        pygame.draw.rect(
            window, self.config.red,
            [self.food_x, self.food_y,
             snake_block, snake_block])


class Snake(Subject):
    def __init__(self, config: GameConfig) -> None:
        super().__init__()
        self.config = config

        # 贪吃蛇初始位置
        self.x = self.config.window_width // 2
        self.y = self.config.window_height // 2

        # 贪吃蛇初始位置和长度
        self.snake_list = [[self.x, self.y]]
        self.length_of_snake = 1

        # 贪吃蛇移动方向
        self.x_change = 0
        self.y_change = 0

        self.foods_observer = []

        # 更新蛇身在config中的数据，以便生成food
        self.config.snake_list = self.snake_list

    def attach(self, food):
        self.foods_observer.append(food)

    def notify(self):
        for food in self.foods_observer:
            food.update(self)

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

        # edge规则1，撞边上就死
        # edge规则2，撞边上不死，循环游走
        # 依据初始选择的策略，来处理
        game_close, self.x, self.y = \
            self.config.current_edge_strategy.process(
                self.x, self.y,
                self.config.window_width, self.config.window_height)

        # 此处的head是蛇头的下一个位置
        snake_head = [int(self.x), int(self.y)]

        # 自身碰撞逻辑，下一步的坐标已经包含在蛇身里面，游戏结束
        for i in self.snake_list[:-1]:
            if i == snake_head:
                print('自杀')
                game_close = True
        # 没有触发edge失败，也没有处罚自杀事件
        # 则加入这个点成为蛇身的一部分
        if not game_close:
            self.snake_list.insert(0, snake_head)
            if len(self.snake_list) > self.length_of_snake:
                del self.snake_list[-1]

        # 每走一步，都通知监听者
        self.notify()

        return game_close

    def draw(self, window):
        snake_block = self.config.snake_block
        for p in self.snake_list:
            pygame.draw.rect(window, self.config.black,
                             [p[0], p[1],
                              snake_block, snake_block])

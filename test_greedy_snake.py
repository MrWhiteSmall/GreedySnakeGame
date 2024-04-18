import pygame
import random

# 引入控制策略
from test_strategy_control import ControlStrategy1,ControlStrategy2
# 引入边界策略
from test_strategy_edge import EdgeStrategy1,EdgeStrategy2
control_strategy1 = ControlStrategy1()
control_strategy2 = ControlStrategy2()
edge_strategy1 = EdgeStrategy1()
edge_strategy2 = EdgeStrategy2()
edge_strategies = [edge_strategy1,edge_strategy2]
current_edge_strategy = None

# 初始化pygame
pygame.init()

# 设置游戏窗口
window_width = 600
window_height = 400

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (200,200,200)

# 定义贪吃蛇和食物的大小
snake_block = 10
snake_speed = 15

# 创建贪吃蛇
def draw_snake(snake_block, snake_list):
    for p in snake_list:
        pygame.draw.rect(window, black, [p[0], p[1], snake_block, snake_block])

# 生成食物
def generate_food(snake_list):
    game_close = False
    for _ in range(1000):
        food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
        if [food_x,food_y] not in snake_list:
            return game_close,food_x,food_y
    # 没有可用位置放置食物，游戏结束
    game_close = True
    return game_close,-1,-1

def draw_food(food_x,food_y):
    # 绘制食物food
    pygame.draw.rect(window, red, [food_x, food_y, snake_block, snake_block])
            
# 选择模式
# 模式1：电网恢恢
# 模式2：循环往复
# 创建按钮的矩形对象
button_width, button_height = 200, 50
button_margin = 20
button_rects = [
    pygame.Rect((window_width - button_width) // 2, (window_height - button_height * 2 - button_margin) // 2, button_width, button_height),
    pygame.Rect((window_width - button_width) // 2, (window_height - button_height) // 2, button_width, button_height)
]
# 设置字体
'''
新细明体：PMingLiU 
细明体：MingLiU 
标楷体：DFKai-SB 
黑体：SimHei 
宋体：SimSun 
新宋体：NSimSun 
仿宋：FangSong 
楷体：KaiTi 
仿宋_GB2312：FangSong_GB2312 
楷体_GB2312：KaiTi_GB2312 
微软正黑体：Microsoft JhengHei 
微软雅黑体：Microsoft YaHei
'''
font_name = pygame.font.match_font('fangsong')  # 2.获得字体文件
font = pygame.font.Font(font_name, 20)  # 1.获取font对象（需要字体文件）
# 游戏模式
game_modes = ['电网恢恢', '循环往复']
selected_mode = None
# 绘制按钮
def draw_buttons():
    for i, rect in enumerate(button_rects):
        pygame.draw.rect(window, gray if rect.collidepoint(pygame.mouse.get_pos()) else black, rect)
        text_surface = font.render(game_modes[i], True, white)
        window.blit(text_surface, ((rect.centerx - text_surface.get_width()) // 2, 
                                   (rect.centery - text_surface.get_height()) // 2))



# 游戏循环
def gameLoop():
    game_over = False
    game_close = False
    forced_stop = False

    # 贪吃蛇初始位置和长度
    snake_list = []
    length_of_snake = 1

    # 贪吃蛇初始位置
    x = window_width / 2
    y = window_height / 2

    # 贪吃蛇移动方向
    x_change = 0
    y_change = 0

    # 食物位置
    food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    global selected_mode,current_edge_strategy

    while not game_over:

        # 游戏正常结束 or 强制结束
        # 游戏结束时屏幕上显示的文字
        while game_close or forced_stop:
            window.fill(white)
            font = pygame.font.SysFont(None, 25)
            text = font.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            window.blit(text, [window_width / 3, window_height / 3])
            pygame.display.update()

            selected_mode = None

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        forced_stop = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if not selected_mode and event.type == pygame.MOUSEBUTTONDOWN:
                # 检查按钮点击
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        selected_mode = game_modes[i]
                        print(f"选择了游戏模式：{selected_mode}")
                        current_edge_strategy = edge_strategies[i]
                        break
            if selected_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    forced_stop = True
                # 蛇身长度=1，允许左右变向，上下变向
                # 蛇身长度>1，不允许左右变向
                # 使用策略模式
                if length_of_snake==1:
                    x_change,y_change = control_strategy1.process(event,snake_block,x_change,y_change)
                else:
                    x_change,y_change = control_strategy2.process(event,snake_block,x_change,y_change)
      
        # 屏幕清空，准备绘制
        window.fill(white)
        # 绘制按钮-选择模式
        # 还没选择好模式，就先绘制按钮，选择好了再绘制游戏界面
        if not selected_mode:
            draw_buttons()
        # 若选择好了模式，再开始绘制蛇的逻辑
        else:
            x += x_change
            y += y_change  

            # edge规则1，撞边上就死
            # edge规则2，撞边上不死，循环游走
            # 依据初始选择的策略，来处理
            game_close,x,y = current_edge_strategy.process(x,y,window_width,window_height)

            # 此处的head是蛇头的下一个位置
            snake_head = [int(x),int(y)]

            # 自身碰撞逻辑，下一步的坐标已经包含在蛇身里面，游戏结束
            for i in snake_list[:-1]:
                if i == snake_head:
                    print('自杀')
                    game_close = True
            if not game_close:
                snake_list.insert(0,snake_head)
                if len(snake_list) > length_of_snake:
                    del snake_list[-1]


            # 如果吃到了事物，就重新生成
            # 如果无处生成事物，游戏结束
            if x==food_x and y==food_y:
                game_close,food_x,food_y = generate_food(snake_list)
                if not game_close:
                    length_of_snake += 1

            ############################### DRAW ##########################################
            # 绘制食物food
            pygame.draw.rect(window, red, [food_x, food_y, snake_block, snake_block])
            # 绘制snake，舌头在snake list[0]的位置
            draw_snake(snake_block, snake_list)
        
        # 屏幕更新
        pygame.display.update()

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

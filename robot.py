import random
import pygame
import sys
from pygame.locals import *
import os

robot_speed = 15  # 机器人的速度
windows_width = 600
windows_height = 600  # 游戏窗口的大小
cell_size = 100  # 机器人身体方块大小,注意身体大小必须能被窗口长宽整除

map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
Gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 139)
yellow = (255, 255, 0)
gray = (194, 192, 75)
BG_COLOR = white  # 游戏背景颜色
direction = 0
g1_direction = random.randint(0, 1) * 2 - 1
g2_direction = random.randint(0, 1) * 2 - 1

# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

mode_A = 0
mode_B = 1
mode = 0
no_right = no_left = no_down = no_up = []


# 主函数
def main():
    pygame.init()  # 模块初始化
    robot_speed_clock = pygame.time.Clock()  # 创建Pygame时钟对象
    screen = pygame.display.set_mode((windows_width, windows_height + 50))  #
    screen.fill(white)
    pygame.display.set_caption("Python 智闯鬼屋小游戏")  # 设置标题
    show_start_info(screen)  # 欢迎信息
    while True:
        ret = running_game(screen, robot_speed_clock)
        if ret == 0:
            show_gameover_info(screen)
        if ret == 2:
            show_win_info(screen)


# 游戏运行主体
def running_game(screen, robot_speed_clock):
    screen.fill(BG_COLOR)
    draw_grid(screen)
    global direction
    startx = 0  # 开始位置
    starty = 5
    step_cnt = 0
    hit_cnt = 0
    robot_coords = {'x': startx, 'y': starty}  # 初始机器人
    ghost1_coords = {'x': random.randint(0, 5), 'y': 2}  # 初始幽灵1（水平移动）
    ghost2_coords = {'x': 3, 'y': random.randint(0, 5)}  # 初始幽灵2（垂直移动）
    screen.fill(BG_COLOR)
    draw_grid(screen)
    draw_robot(screen, robot_coords)
    draw_ghost(screen, ghost1_coords)
    draw_ghost(screen, ghost2_coords)
    draw_score(screen, step_cnt)
    draw_hit_cnt(screen, hit_cnt)
    draw_cold_degree(screen, robot_coords, ghost1_coords, ghost2_coords)
    # for i in no_down:
    #     draw_robot(screen, i)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                print(no_right)
                if (event.key == K_LEFT or event.key == K_a) and robot_coords['x'] != 0:
                    direction = LEFT
                    if robot_coords in no_left:
                        hit_cnt += 1
                        print('撞墙了')
                    else:
                        step_cnt += 1
                        move(screen, direction, robot_coords, robot_speed_clock, step_cnt, ghost1_coords, ghost2_coords)
                elif (event.key == K_RIGHT or event.key == K_d) and robot_coords['x'] != 5:
                    direction = RIGHT
                    if robot_coords in no_right:
                        hit_cnt += 1
                        print('撞墙了')
                    else:
                        step_cnt += 1
                        move(screen, direction, robot_coords, robot_speed_clock, step_cnt, ghost1_coords, ghost2_coords)
                elif (event.key == K_UP or event.key == K_w) and robot_coords['y'] != 0:
                    direction = UP
                    if robot_coords in no_up:
                        hit_cnt += 1
                        print('撞墙了')
                    else:
                        step_cnt += 1
                        move(screen, direction, robot_coords, robot_speed_clock, step_cnt, ghost1_coords, ghost2_coords)
                elif (event.key == K_DOWN or event.key == K_s) and robot_coords['y'] != 5:
                    direction = DOWN
                    if robot_coords in no_down:
                        hit_cnt += 1
                        print('撞墙了')
                    else:
                        step_cnt += 1
                        move(screen, direction, robot_coords, robot_speed_clock, step_cnt, ghost1_coords, ghost2_coords)
                elif event.key == K_ESCAPE:
                    terminate()
        ret = robot_is_alive(robot_coords, ghost1_coords, ghost2_coords)
        if ret != 1:
            return ret  # 机器人死了. 游戏结束


def move(screen, direction, robot_coords, robot_speed_clock, step_cnt, ghost1_coords, ghost2_coords):
    move_robot(direction, robot_coords)  # 移动机器人
    move_ghost1(ghost1_coords)
    move_ghost2(ghost2_coords)
    screen.fill(BG_COLOR)
    draw_grid(screen)
    draw_robot(screen, robot_coords)
    draw_ghost(screen, ghost1_coords)
    draw_ghost(screen, ghost2_coords)
    # draw_score(screen, step_cnt)
    draw_word(screen,step_cnt,'谢谢')
    draw_cold_degree(screen, robot_coords, ghost1_coords, ghost2_coords)
    # draw_hit_cnt(screen, hit_cnt)
    pygame.display.update()
    robot_speed_clock.tick(robot_speed)  # 控制fps


# 将机器人画出来
def draw_robot(screen, robot_coords):
    x = robot_coords['x'] * cell_size
    y = robot_coords['y'] * cell_size
    # InnerSegmentRect = pygame.Rect(
    #     x + 4, y + 4, cell_size - 8, cell_size - 8)
    # pygame.draw.rect(screen, blue, InnerSegmentRect)
    pic = pygame.image.load(os.path.join('pic', 'robot.png'))
    screen.blit(pic, (x + 1, y + 1))

    # SegmentRect = pygame.Rect(x, y, cell_size, cell_size)
    # pygame.draw.rect(screen, dark_blue, SegmentRect)


def draw_ghost(screen, ghost_coords):
    x = ghost_coords['x'] * cell_size
    y = ghost_coords['y'] * cell_size
    # SegmentRect = pygame.Rect(x, y, cell_size, cell_size)
    # pygame.draw.rect(screen, dark_gray, SegmentRect)
    # InnerSegmentRect = pygame.Rect(
    #     x + 2, y + 2, cell_size - 3, cell_size - 3)
    # pygame.draw.rect(screen, gray, InnerSegmentRect)
    pic = pygame.image.load(os.path.join('pic','ghost.png'))
    screen.blit(pic, (x + 4, y + 4))


# 画网格(可选)
def draw_grid(screen):
    global mode
    for y in range(6):
        rect = pygame.Rect(3 * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, yellow, rect)
    for x in range(6):
        rect = pygame.Rect(x * cell_size, 2 * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, yellow, rect)
    # rect = pygame.Rect(5 * cell_size, 0 * cell_size, cell_size, cell_size)
    # pygame.draw.rect(screen, Green, rect)

    pic = pygame.image.load(os.path.join('pic','safe_out.png'))
    screen.blit(pic, (5 * cell_size, 0 * cell_size))

    for x in range(0, windows_width, cell_size):  # draw 水平 lines
        pygame.draw.line(screen, dark_gray, (x, 0), (x, windows_height))
    for y in range(0, windows_height, cell_size):  # draw 垂直 lines
        pygame.draw.line(screen, dark_gray, (0, y), (windows_width, y))
    if mode == mode_B:
        pygame.draw.line(screen, Red, (3 * cell_size, 0), (3 * cell_size, cell_size), width=7)
        pygame.draw.line(screen, Red, (cell_size, cell_size), (cell_size, 2 * cell_size), width=7)
        pygame.draw.line(screen, Red, (4 * cell_size, cell_size), (4 * cell_size, 3 * cell_size), width=7)
        pygame.draw.line(screen, Red, (4 * cell_size, 4 * cell_size), (4 * cell_size, 5 * cell_size), width=7)
        pygame.draw.line(screen, Red, (2 * cell_size, 5 * cell_size), (2 * cell_size, 6 * cell_size), width=7)
        pygame.draw.line(screen, Red, (cell_size, cell_size), (2 * cell_size, cell_size), width=7)
        pygame.draw.line(screen, Red, (3 * cell_size, 2 * cell_size), (4 * cell_size, 2 * cell_size), width=7)
        pygame.draw.line(screen, Red, (cell_size, 3 * cell_size), (3 * cell_size, 3 * cell_size), width=7)
        pygame.draw.line(screen, Red, (4 * cell_size, 3 * cell_size), (5 * cell_size, 3 * cell_size), width=7)
        pygame.draw.line(screen, Red, (0 * cell_size, 4 * cell_size), (cell_size, 4 * cell_size), width=7)
        pygame.draw.line(screen, Red, (2 * cell_size, 4 * cell_size), (3 * cell_size, 4 * cell_size), width=7)
        pygame.draw.line(screen, Red, (5 * cell_size, 5 * cell_size), (6 * cell_size, 5 * cell_size), width=7)
        pygame.draw.line(screen, Red, (0 * cell_size, 0 * cell_size), (0 * cell_size, 6 * cell_size), width=7)
        pygame.draw.line(screen, Red, (0 * cell_size, 0 * cell_size), (6 * cell_size, 0 * cell_size), width=7)
        pygame.draw.line(screen, Red, (0 * cell_size, 6 * cell_size), (6 * cell_size, 6 * cell_size), width=7)
        pygame.draw.line(screen, Red, (6 * cell_size, 0 * cell_size), (6 * cell_size, 6 * cell_size), width=7)


# 移动机器人
def move_robot(direction, robot_coords):
    if direction == UP:
        robot_coords['y'] = robot_coords['y'] - 1
    elif direction == DOWN:
        robot_coords['y'] = robot_coords['y'] + 1
    elif direction == LEFT:
        robot_coords['x'] = robot_coords['x'] - 1
    elif direction == RIGHT:
        robot_coords['x'] = robot_coords['x'] + 1


# 移动幽灵1
def move_ghost1(ghost1_coords):
    global g1_direction
    if ghost1_coords['x'] == 5:
        g1_direction = -1
    if ghost1_coords['x'] == 0:
        g1_direction = 1
    ghost1_coords['x'] = ghost1_coords['x'] + g1_direction


# 移动幽灵2
def move_ghost2(ghost2_coords):
    global g2_direction
    if ghost2_coords['y'] == 5:
        g2_direction = -1
    if ghost2_coords['y'] == 0:
        g2_direction = 1
    ghost2_coords['y'] = ghost2_coords['y'] + g2_direction


# 判断机器人死了没
def robot_is_alive(robot_coords, ghost1_coords, ghost2_coords):
    tag = 1
    if robot_coords['x'] == 5 and robot_coords['y'] == 0:
        tag = 2
    if ((robot_coords['x'] == ghost1_coords['x'] and robot_coords['y'] == ghost1_coords['y']) or
            (robot_coords['x'] == ghost2_coords['x'] and robot_coords['y'] == ghost2_coords['y'])):
        tag = 0  # 机器人碰到幽灵啦
    if (robot_coords['x'] == ghost1_coords['x'] - g1_direction and robot_coords['y'] == ghost1_coords['y']) and (
            (direction == LEFT and g1_direction == 1) or (direction == RIGHT and g1_direction == -1)):
        tag = 0
    if (robot_coords['x'] == ghost2_coords['x'] and robot_coords['y'] == ghost2_coords['y'] - g2_direction) and (
            (direction == UP and g2_direction == 1) or (direction == DOWN and g2_direction == -1)):
        tag = 0
    return tag


# 开始信息显示
def show_start_info(screen):
    global mode
    global no_right, no_left, no_down, no_up
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 40)
    tip = font.render('按下a或b开始游戏~~~', True, (65, 105, 225))
    gamestart = pygame.image.load(os.path.join('pic','gamestart.png'))
    screen.blit(gamestart, (40, 30))
    screen.blit(tip, (150, 550))
    pygame.display.update()
    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # 终止程序
                    terminate()  # 终止程序
                elif event.key == K_a:
                    mode = mode_A
                    no_right = no_left = no_down = no_up = []
                    return  # 结束此函数, 开始游戏
                elif event.key == K_b:
                    mode = mode_B
                    no_right = [{'x': 2, 'y': 0}, {'x': 0, 'y': 1}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2},
                                {'x': 3, 'y': 4},
                                {'x': 1, 'y': 5}]
                    no_left = [{'x': 3, 'y': 0}, {'x': 1, 'y': 1}, {'x': 4, 'y': 1}, {'x': 4, 'y': 2}, {'x': 4, 'y': 4},
                               {'x': 2, 'y': 5}]
                    no_down = [{'x': 1, 'y': 0}, {'x': 3, 'y': 1}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2}, {'x': 4, 'y': 2},
                               {'x': 0, 'y': 3},
                               {'x': 2, 'y': 3}, {'x': 5, 'y': 4}]
                    no_up = [{'x': 1, 'y': 1}, {'x': 3, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 3}, {'x': 4, 'y': 3},
                             {'x': 0, 'y': 4},
                             {'x': 2, 'y': 4}, {'x': 5, 'y': 5}]
                    return  # 结束此函数, 开始游戏


# 游戏结束信息显示
def show_gameover_info(screen):
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 40)
    tip = font.render('按Q或者ESC退出游戏', True, (65, 105, 225))
    tip2 = font.render('按任意键重新开始游戏~', True, (65, 105, 225))
    gamestart = pygame.image.load(os.path.join('pic','gameover.png'))
    screen.blit(gamestart, (-20, -20))
    screen.blit(tip, (130, 480))
    screen.blit(tip2, (130, 540))
    pygame.display.update()
    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                    terminate()  # 终止程序
                else:
                    return  # 结束此函数, 重新开始游戏


# 游戏胜利信息显示
def show_win_info(screen):
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 40)
    tip = font.render('按Q或者ESC退出游戏', True, (65, 105, 225))
    tip2 = font.render('按任意键重新开始游戏~', True, (65, 105, 225))
    pic = pygame.image.load(os.path.join('pic','wow.png'))
    screen.blit(pic, (0, -20))
    screen.blit(tip, (130, 480))
    screen.blit(tip2, (130, 540))
    pygame.display.update()
    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                    terminate()  # 终止程序
                else:
                    return  # 结束此函数, 重新开始游戏


# 画成绩
def draw_word(screen, score,s):
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 30)
    scoreSurf = font.render(s+': %s' % score, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 10)
    screen.blit(scoreSurf, scoreRect)

# 画成绩
def draw_score(screen, score):
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 30)
    scoreSurf = font.render('步数: %s' % score, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 10)
    screen.blit(scoreSurf, scoreRect)


# 画成绩
def draw_hit_cnt(screen, hit_cnt):
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 30)
    scoreSurf = font.render('撞墙次数: %s' % hit_cnt, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 90)
    screen.blit(scoreSurf, scoreRect)


# 画成绩
def draw_cold_degree(screen, robot_coords, ghost1_coords, ghost2_coords):
    cold_degree = 0
    if abs(robot_coords['x'] - ghost1_coords['x']) + abs(robot_coords['y'] - ghost1_coords['y']) == 1:
        cold_degree = 2
    if abs(robot_coords['x'] - ghost1_coords['x']) + abs(robot_coords['y'] - ghost1_coords['y']) == 2:
        cold_degree = 1
    if abs(robot_coords['x'] - ghost1_coords['x']) + abs(robot_coords['y'] - ghost1_coords['y']) >= 3:
        cold_degree = 0
    if abs(robot_coords['x'] - ghost2_coords['x']) + abs(robot_coords['y'] - ghost2_coords['y']) == 1:
        cold_degree += 2
    if abs(robot_coords['x'] - ghost2_coords['x']) + abs(robot_coords['y'] - ghost2_coords['y']) == 2:
        cold_degree += 1
    if abs(robot_coords['x'] - ghost2_coords['x']) + abs(robot_coords['y'] - ghost2_coords['y']) >= 3:
        cold_degree += 0
    font = pygame.font.Font(os.path.join('pic','myfont.ttf'), 30)
    scoreSurf = font.render('寒意浓度: %s' % cold_degree, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 50)
    screen.blit(scoreSurf, scoreRect)


# 程序终止
def terminate():
    pygame.quit()
    sys.exit()


main()

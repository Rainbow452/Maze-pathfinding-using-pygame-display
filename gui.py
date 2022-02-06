from mazeMap import Rand_shape_maze,Rand_maze
from pygame import init
from pygame import display
from pygame import font as pyfont
from pygame import image
from pygame import Color as pyColor
from  pygame import time 
from  pygame import quit
from  pygame import mouse
from  pygame import event as pyevent
from pygame import  MOUSEBUTTONDOWN
from pygame import KEYDOWN
from pygame import QUIT
import pygame
from findpathing import pathfinding_maze
#行列数

#默认 迷宫大小
maze_rows = 20
maze_cols = 20

#页面更新频率 界面宽、高
FPS = 30
display_width = 800
display_height = 600

#颜色RGB值
WHITE = (255, 255, 255)
bg_yellow=(255, 242, 0)
GREE= (107, 194, 53)
RED = (247, 68, 97)
BULE = (69 ,137 ,148)

#背景图片载入
bg_location = 'source/yellow_bg.png'
bg = image.load(bg_location)

#pygame 初始化 设置显示界面  界面左上角图标
init()
screen=display.set_mode((display_width,display_height))
display.set_caption('maze')
icon = image.load('source/icon.png')
display.set_icon(icon)

#墙类
class  wall():
    def __init__(self,loc,m_x,m_y):
        # 墙的贴图路径， 坐标 x， y
        self.img = image.load(loc)
        self.x = m_x
        self.y = m_y
#迷宫类
class maze():
    def __init__(self,maze_input_mazeList,loc,screen):
        '''输入:
                迷宫列表（二维数组， 最外围是墙（1））
                墙贴图路径
                显示界面
        '''
        self.screen = screen
        self.indoor = 'source/in_door.png'
        self.outdoor = 'source/out_door.png'
        self.mazeWall = []
        self.maze_input_mazeList = maze_input_mazeList
        self.route = []
        self.loc = loc




    def showMaze(self,maze_input_mazeList):
        '''迷宫显示
            输入:
                迷宫列表（二维数组， 最外围是墙, 墙（1）  走过的路线（2）， 最终路线（3））
        '''
        self.mazeWall = []
        self.maze_input_mazeList = maze_input_mazeList

        #转换出迷宫在显示界面的坐标
        for i in range(len(self.maze_input_mazeList)):
            for j in range(len(self.maze_input_mazeList[i])):
                if self.maze_input_mazeList[i, j] == 1:  #墙
                    self.mazeWall.append(wall(self.loc, 300 - self.maze_input_mazeList.shape[0]*8 + i * 16, 300 - self.maze_input_mazeList.shape[1]*8 + j * 16))

                elif self.maze_input_mazeList[i, j] == 2: #走过的路
                    self.mazeWall.append(wall('source/foot_1.png', 300 - self.maze_input_mazeList.shape[0]*8 + i * 16, 300 - self.maze_input_mazeList.shape[1]*8 + j * 16))
                elif self.maze_input_mazeList[i, j] == 3: #最终路线
                    self.mazeWall.append(wall('source/foot_2.png', 300 - self.maze_input_mazeList.shape[0]*8 + i * 16, 300 - self.maze_input_mazeList.shape[1]*8 + j * 16))

            #入口图标
        self.mazeWall.append(wall(self.indoor, 300 - self.maze_input_mazeList.shape[0] * 8 + 1 * 16, 300 - self.maze_input_mazeList.shape[1] * 8 + 1 * 16))
            #出口图标
        self.mazeWall.append(wall(self.outdoor, 300 - self.maze_input_mazeList.shape[0] * 8 + (self.maze_input_mazeList.shape[0] - 2) * 16, 300 - self.maze_input_mazeList.shape[1] * 8 + (self.maze_input_mazeList.shape[1] - 2) * 16))
        print('show maze')
        #将迷宫放到显示界面上
        for w in self.mazeWall:
            self.screen.blit(w.img, (w.x, w.y))
    #显示迷宫右边的与数据的分割线
    def showWall(self,loc):
        img = image.load(loc)
        for i  in range(38):
            self.screen.blit(img, (600 ,16*i))
        print('show wall')

#按钮字体大小设置
start_font_addr = pyfont.get_default_font()
font = pyfont.Font('source/smyw.ttf', 64)

#按钮类
class Button(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        '''输入:
                按钮文字
                文字颜色
                x, y坐标
        '''

        self.text = text
        #渲染文字
        self.surface = font.render(self.text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y
    #显示
    def display(self):
        screen.blit(self.surface, (self.x, self.y))
    #鼠标点击检查, 在按钮范围内点击返回 True
    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False
# 字体大小设置， 开始界面图片载入
start_font = pyfont.Font('source/Folkard.ttf', 64)
title_img = image.load('source/start_maze.png')
#1开始界面
def starting_screen():
    # 背景
    screen.fill(bg_yellow)
    #开始界面  中间标题
    game_title = start_font.render('MAZE PATHFINDING', True, (1,77,107))
    #标题 图片显示
    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 150))
    screen.blit(title_img,(display_width // 2 - 32, 80))
    #按钮
    play_button = Button('Play', RED, None, 300, centered_x=True)
    exit_button = Button('Exit', WHITE, None, 400, centered_x=True)
    #鼠标指在按钮上时改变颜色
    while True:
        if play_button.check_click(mouse.get_pos()):
            play_button = Button('Play', RED, None, 300, centered_x=True)
        else:
            play_button = Button('Play', WHITE, None, 300, centered_x=True)

        if exit_button.check_click(mouse.get_pos()):
            exit_button = Button('Exit', RED, None, 400, centered_x=True)
        else:
            exit_button = Button('Exit', WHITE, None, 400, centered_x=True)
        #按钮显示更新
        play_button.display()
        exit_button.display()

        # 点 右上角 X 退出
        for event in pyevent.get():
            if event.type == QUIT:
                quit()
                raise SystemExit
        #点击切换界面  改变 modeSelect 切换不同界面  0（开始界面）  1（设置界面）   2（迷宫界面）
        if mouse.get_pressed()[0]:
            if play_button.check_click(mouse.get_pos()):
                global  modeSelect
                modeSelect = 1
                break
            if exit_button.check_click(mouse.get_pos()):

                quit()
                raise SystemExit
                break
        display.update()

# pygame 自带颜色
COLOR_INACTIVE = pyColor('lightskyblue3')
COLOR_ACTIVE = pyColor('dodgerblue2')
# COLOR_INACTIVE = (255,242,0)
# COLOR_ACTIVE = (255,242,0)
#字体（smym(水墨英文字体库)）和字体大小
FONT = pyfont.Font('source/smyw.ttf', 100)

font_48 = pyfont.Font('source/smyw.ttf', 44)
font_64 = pyfont.Font('source/smyw.ttf', 64)

# 数字输入框类
class InputBox:

    def __init__(self, x, y, w, h, text='20'):
        '''
        输入:
                x， y坐标
                框宽高（输入框大小（隐形）与字体大小不相关. 输入框宽高 与显示字体宽高并不相同）
                默认显示 20 （默认迷宫大小）
        '''
        self.color = WHITE
        self.line = font_64.render('___', True, self.color)
        self.text = text
        self.x = x
        self.y = y
        self.txt_surface = FONT.render(text, True, GREE)
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # 如果鼠标在检测区域内，activate=True，下划线变色
            if  event.pos[0] > self.x and event.pos[0] < self.x + self.line.get_width() and self.y - (self.txt_surface.get_height() - self.line.get_height()) // 3 and event.pos[1] < self.y+64 + (self.txt_surface.get_height() - self.line.get_height()) // 3:
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            # self.color = BULE if self.active else WHITE       #指到时改变颜色
            # self.line = font_line.render('___', True, self.color)


        if event.type == KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:  # 键盘按下返回按下值
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text)>=2:
                        pass
                    else:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, GREE)
    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.line.get_width()
        y_match = position[1] > self.y - (self.txt_surface.get_height() - self.line.get_height()) // 3 and position[1] < self.y+64 + (self.txt_surface.get_height() - self.line.get_height()) // 3
        if x_match and y_match:
            return True
        else:
            return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.line,(self.x,self.y))
        screen.blit(self.txt_surface, (self.x + 20, self.y -20))
        #修改行列

class ButtonBox:

    def __init__(self, x, y, w, h, text=''):
        self.color = WHITE
        self.line = font_64.render('___', True, self.color)
        self.text = text
        self.x = x
        self.y = y
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == mouseBUTTONDOWN:
            # 如果鼠标在检测区域内，activate=True，下划线变色
            if  event.pos[0] > self.x and event.pos[0] < self.x + self.line.get_width() and self.y - (self.txt_surface.get_height() - self.line.get_height()) // 3 and event.pos[1] < self.y+64 + (self.txt_surface.get_height() - self.line.get_height()) // 3:
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.line.get_width()
        y_match = position[1] > self.y - (self.txt_surface.get_height() - self.line.get_height()) // 3 and position[1] < self.y+64 + (self.txt_surface.get_height() - self.line.get_height()) // 3
        if x_match and y_match:
            return True
        else:
            return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.line,(self.x,self.y))
        screen.blit(self.txt_surface, (self.x , self.y -40))



#2.设置界面
font_50 = pyfont.Font('source/smyw.ttf', 50)
maze_mode = 'rand'
wayfinding = ''  #DFS（深度优先） / BFS（宽度优先） 选择
def setting_screen():
    global maze_mode,  modeSelect
    screen.fill(bg_yellow)
    FONT_80 = pyfont.Font('source/smyw.ttf', 80)
    FONT_48 = pyfont.Font('source/smyw.ttf', 36)

    row_title = font.render('rows:', True, BULE)
    col_title = font.render('cols:', True, BULE)
    #文字渲染
    maze_mode_title = font_48.render('maze mode:', True, BULE)
    setting_title = FONT_80.render('Setting:', True, BULE)
    tips_title = FONT_48.render('(Tips:0<rows<36; 0<cols<36)',True,RED)

    #两个输入框
    input_box1 = InputBox( 90+row_title.get_width(), 150, 76, 64)
    input_box2 = InputBox(430+col_title.get_width(), 150, 76, 64)
    #两个按钮 DFS 深度优先， BFS  广度优先    ，back 返回键  返回开始菜单
    Button_box1 = ButtonBox(150, 480, 76, 64,text='DFS')
    Button_box2= ButtonBox(500, 480, 76, 64,text='BFS')
    back_button = Button1('BACK', WHITE, 680, 50)
    # 迷宫样式按钮 1. rand  2. rand shape
    rand_button = Button('Rand', RED, 300, 290)
    rand_shape_button = Button('Rand shape', RED, 470, 290 )
    rand_button.surface = font_64.render(rand_button.text,True,WHITE)
    rand_shape_button.surface = font_64.render(rand_shape_button.text,True,WHITE)

    input_boxes = [input_box1, input_box2]
    Button_boxes = [Button_box1,Button_box2]

    global wayfinding
    while True:
        screen.fill(bg_yellow)
        rand_button.display()
        rand_shape_button.display()
        screen.blit(setting_title, (0, 0))
        screen.blit(row_title, (70, 150))
        screen.blit(col_title, (440, 150))
        screen.blit(maze_mode_title, (70, 300))
        screen.blit(tips_title, (175, 230))
        # 鼠标指按钮颜色改变
        if back_button.check_click(mouse.get_pos()):
            back_button = Button1('BACK', RED, 680, 50)
        else:
            back_button = Button1('BACK', WHITE, 680, 50)
        #选择迷宫样式  按钮字体颜色改变
        if maze_mode == 'rand':
            rand_button.surface = font_64.render(rand_button.text, True, GREE)
            rand_shape_button.surface = font_64.render(rand_shape_button.text, True, WHITE)
        if maze_mode == 'rand shape':
            rand_button.surface = font_64.render(rand_button.text, True, WHITE)
            rand_shape_button.surface = font_64.render(rand_shape_button.text, True, GREE)


        #鼠标指DFS BFS按钮   下划线颜色改变
        for box in Button_boxes:
            if box.check_click(mouse.get_pos()):
                box.line = font_64.render('___', True, RED)
                box.txt_surface = FONT.render(box.text, True, RED)
            else:
                box.line = font_64.render('___', True, WHITE)
                box.txt_surface = FONT.render(box.text, True, WHITE)
        #鼠标左键点击按钮时 切换页面 设置寻路算法  迷宫类型
        if mouse.get_pressed()[0]:
            if Button_box1.check_click(mouse.get_pos()):

                modeSelect = 2
                wayfinding= 'DFS'
                break
            if Button_box2.check_click(mouse.get_pos()):
                modeSelect = 2
                wayfinding= 'BFS'
                break
            if rand_button.check_click(mouse.get_pos()):
                rand_button.surface = font_64.render(rand_button.text, True,GREE)
                rand_shape_button.surface = font_64.render(rand_shape_button.text, True, WHITE)
                maze_mode = 'rand'
            if rand_shape_button.check_click(mouse.get_pos()):
                rand_button.surface = font_64.render(rand_button.text, True,WHITE)
                rand_shape_button.surface = font_64.render(rand_shape_button.text, True, GREE)
                maze_mode = 'rand shape'
            if back_button.check_click(mouse.get_pos()):

                modeSelect = 0
                break

        #数字输入框 下划线颜色改变
        for box in input_boxes:
            if box.check_click(mouse.get_pos()):
                box.line = font_64.render('___', True, RED)
            else:
                box.line = font_64.render('___', True, WHITE)
        # 右上角 X 退出
        for event in pyevent.get():
            if event.type == QUIT:
                quit()
                raise SystemExit
            for box in input_boxes:
                box.handle_event(event)
        #在界面显示 按钮 输入框
        for box in Button_boxes:
            box.draw(screen)
        for box in input_boxes:
            box.draw(screen)
        #修改行列值
        global maze_rows,maze_cols
        if not input_box1.text == '' and not input_box2.text == '':
            maze_rows = int(input_box1.text)
            maze_cols = int(input_box2.text)
        back_button.display()

        # 更新界面  （之前的的文字，输入框显示 相当于把它们放到一个画布上， 下面才是更新显示到屏幕上）
        display.flip()


#字体 大小
font_32 = pyfont.Font('source/smyw.ttf', 32)

class Button1(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font_32.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

node_num = 0
def node(maze_input_mazeList):
    '''返回迷宫中最终路线的步数'''
    node_n = 0
    for i in range(len(maze_input_mazeList)):
        for j in range(len(maze_input_mazeList[i])):
            if maze_input_mazeList[i, j] == 2 or maze_input_mazeList[i, j] == 3 :
                node_n +=1
    return node_n

# 地图界面 按钮的坐标
DFS_button_x = 670
DFS_button_y = 400
BFS_button_x = 670
BFS_button_y = 320
ASTAR_button_x = 670
ASTAR_button_y = 360

#当前方法(method)标题的 x坐标
method_x = 615


#地图界面
def map():
    global wayfinding
    global node_num
    screen.fill(bg_yellow)
    #根据迷宫类型和大小 随机生成迷宫(基于mazelab模块)
    if maze_mode == 'rand':
        rand_mazeList = Rand_maze(maze_rows, maze_cols)
    elif maze_mode == 'rand shape':
        rand_mazeList = Rand_shape_maze(maze_rows,maze_cols)
    #迷宫类
    maze_cfg = maze(rand_mazeList, 'source/wall-16.png',screen)
    maze_cfg.showMaze(rand_mazeList)
    # 迷宫右侧的分割线(墙)
    maze_cfg.showWall('source/wall2-16.png')
    # 迷宫界面 右侧 文字数字渲染与显示
    step = ''
    min_step = ''
    step_title = font_32.render('Step:', True, BULE)
    node_title = font_32.render('Node:', True, BULE)
    min_step_title = font_32.render('Min-Step:', True, BULE)
    min_step_num = font_48.render(str(min_step), True, GREE)
    step_num = font_48.render(str(step), True, GREE)
    node_num_title = font_48.render(str(node_num), True, GREE)
    DFS = font_32.render('Method: DFS', True, BULE)
    BFS = font_32.render('Method: BFS', True, BULE)
    ASTAR = font_32.render('Method:ASTAR', True, BULE)
    find_way_button = Button1('Find Way !', WHITE, 630, 450)
    DFS_button = Button1('DFS', WHITE, DFS_button_x, DFS_button_y)
    BFS_button = Button1('BFS', WHITE, BFS_button_x, BFS_button_y)
    ASTAR_button = Button1('ASTAR', WHITE, ASTAR_button_x, ASTAR_button_y)
    skip_button = Button1('ship', WHITE, 670, 510)
    back_button = Button1('BACK', WHITE, 670, 10)
    # find_way_button.display()
    # DFS_maze = DFS_maze

    maze_pathfinding = pathfinding_maze()
    #三种 寻路算法
    maze_pathfinding.BFS_maze(1, 1, rand_mazeList.shape[0] - 2, rand_mazeList.shape[1] - 2, rand_mazeList)

    maze_pathfinding.DFS_maze(1, 1, rand_mazeList.shape[0] - 2, rand_mazeList.shape[1] - 2, rand_mazeList)

    maze_pathfinding.AStar_maze(1, 1, rand_mazeList.shape[0] - 2, rand_mazeList.shape[1] - 2, rand_mazeList)

    while True:
        # 迷宫界面 实时显示
        # screen.fill(bg_yellow)
        # 文本标题显示
        node_num_title = font_48.render(str(node_num), True, GREE)
        screen.blit(step_title, (630, 130))
        screen.blit(min_step_title, (640, 200))
        screen.blit(node_title, (630, 520))
        screen.blit(node_num_title, (715, 515))


        # 按钮颜色改变
        if find_way_button.check_click(mouse.get_pos()):
            find_way_button = Button1('Find Way !', RED, 630, 450)
        else:
            find_way_button = Button1('Find Way !', WHITE, 630, 450)
        if back_button.check_click(mouse.get_pos()):
            back_button = Button1('BACK', RED, 670, 10)
        else:
            back_button = Button1('BACK', WHITE, 670, 10)
        if DFS_button.check_click(mouse.get_pos()):
            DFS_button = Button1('DFS', RED, DFS_button_x, DFS_button_y)
        else:
            DFS_button = Button1('DFS', WHITE, DFS_button_x, DFS_button_y)
        if BFS_button.check_click(mouse.get_pos()):
            BFS_button = Button1('BFS', RED, BFS_button_x, BFS_button_y)
        else:
            BFS_button = Button1('BFS', WHITE, BFS_button_x, BFS_button_y)
        if ASTAR_button.check_click(mouse.get_pos()):
            ASTAR_button = Button1('ASTAR', RED, ASTAR_button_x, ASTAR_button_y)
        else:
            ASTAR_button = Button1('ASTAR', WHITE, ASTAR_button_x, ASTAR_button_y)
        # 根据当前选择的算法, 显示其他两种算法的切换按钮
        if wayfinding == 'BFS':
            DFS_button.display()
            ASTAR_button.display()
        if wayfinding == 'DFS':
            BFS_button.display()
            ASTAR_button.display()
        if wayfinding == 'ASTAR':
            BFS_button.display()
            DFS_button.display()

        #当前方法 标题显示
        if wayfinding == 'DFS':
            screen.blit(DFS, (method_x, 70))
        if wayfinding == 'BFS':
            screen.blit(BFS, (method_x, 70))
        if wayfinding == 'ASTAR':
            screen.blit(ASTAR,(method_x, 70))
        #按钮 点击触发
        if mouse.get_pressed()[0]:
            #切换 A star 算法
            if ASTAR_button.check_click(mouse.get_pos()):
                node_num = 0
                screen.fill(bg_yellow)
                wayfinding = 'ASTAR'
                screen.blit(step_title, (630, 130))
                screen.blit(min_step_title, (640, 200))

                maze_cfg.showMaze(rand_mazeList)
                maze_cfg.showWall('source/wall2-16.png')
                print('mode: ASTAR')
                if wayfinding == 'DFS':
                    screen.blit(DFS, (method_x, 70))
                if wayfinding == 'BFS':
                    screen.blit(BFS, (method_x, 70))
                if wayfinding == 'ASTAR':
                    screen.blit(ASTAR, (method_x, 70))
            #切换 深度优先算法
            if DFS_button.check_click(mouse.get_pos()):
                node_num = 0
                screen.fill(bg_yellow)
                wayfinding = 'DFS'
                screen.blit(step_title, (630, 130))
                screen.blit(min_step_title, (640, 200))

                maze_cfg.showMaze(rand_mazeList)
                maze_cfg.showWall('source/wall2-16.png')
                print('mode: DFS')
                if wayfinding == 'DFS':
                    screen.blit(DFS, (method_x, 70))
                if wayfinding == 'BFS':
                    screen.blit(BFS, (method_x, 70))
                if wayfinding == 'ASTAR':
                    screen.blit(ASTAR, method_x, 70)
            #切换 广度优先算法
            if BFS_button.check_click(mouse.get_pos()):
                node_num = 0
                screen.fill(bg_yellow)
                screen.blit(step_title, (630, 130))
                screen.blit(min_step_title, (640, 200))
                maze_cfg.showMaze(rand_mazeList)
                maze_cfg.showWall('source/wall2-16.png')
                print('mode: BFS')
                wayfinding = 'BFS'
                if wayfinding == 'DFS':
                    screen.blit(DFS, (method_x, 70))
                if wayfinding == 'BFS':
                    screen.blit(BFS, (method_x, 70))
                if wayfinding == 'ASTAR':
                    screen.blit(ASTAR, method_x, 70)
            # 路径显示按钮
            if find_way_button.check_click(mouse.get_pos()):
                screen.fill(bg_yellow)
                screen.blit(step_title, (630, 130))
                screen.blit(step_num, (720, 125))
                screen.blit(min_step_title, (640, 200))
                if wayfinding == 'DFS':
                    screen.blit(DFS, (method_x, 70))
                if wayfinding == 'BFS':
                    screen.blit(BFS, (method_x, 70))
                if wayfinding == 'ASTAR':
                    screen.blit(ASTAR, (method_x, 70))
                # 显示 深度优先 的寻路过程
                if wayfinding == 'DFS':
                    min_step = font_48.render(str(maze_pathfinding.DFS_step + 1), True, GREE)
                    for x, maze_p in enumerate(maze_pathfinding.DFS_process):
                        screen.fill(bg_yellow)

                        screen.blit(min_step, (680, 250))
                        skip_button.display()
                        screen.blit(step_title, (630, 130))

                        back_button.display()
                        find_way_button.display()
                        step_num = font_48.render(str(x + 1), True, GREE)
                        screen.blit(step_num, (720, 125))
                        screen.blit(min_step_title, (640, 200))

                        if wayfinding == 'DFS':
                            screen.blit(DFS, (method_x, 70))
                        if wayfinding == 'BFS':
                            screen.blit(BFS, (method_x, 70))
                        if wayfinding == 'ASTAR':
                            screen.blit(ASTAR, method_x, 70)

                        for event in pyevent.get():
                            if event.type == QUIT:
                                quit()
                                raise SystemExit

                        if find_way_button.check_click(mouse.get_pos()):
                            find_way_button = Button1('Find Way !', RED, 630, 450)
                        else:
                            find_way_button = Button1('Find Way !', WHITE, 630, 450)
                        if back_button.check_click(mouse.get_pos()):
                            back_button = Button1('BACK', RED, 670, 10)
                        else:
                            back_button = Button1('BACK', WHITE, 670, 10)
                        if skip_button.check_click(mouse.get_pos()):
                            skip_button = Button1('skip', RED, 670, 510)
                        else:
                            skip_button = Button1('skip', WHITE, 670, 510)
                        if mouse.get_pressed()[0]:
                            if skip_button.check_click(mouse.get_pos()):
                                screen.fill(bg_yellow)
                                maze_cfg.showMaze(maze_pathfinding.DFS_process[-1])
                                maze_cfg.showWall('source/wall2-16.png')
                                break

                        maze_cfg.showMaze(maze_p)
                        maze_cfg.showWall('source/wall2-16.png')
                        display.update()
                        dtime = time.delay(50)
                    screen.fill(bg_yellow)
                    screen.blit(step_title, (630, 130))


                    node_num = node(maze_pathfinding.DFS_process[-1]) +2 

                    step_num = font_48.render(str(len(maze_pathfinding.DFS_process)), True, GREE)
                    screen.blit(step_num, (720, 125))
                    maze_cfg.showMaze(maze_pathfinding.DFS_process[-1])
                    maze_cfg.showWall('source/wall2-16.png')
                    min_step = font_48.render(str(maze_pathfinding.DFS_step+1), True, GREE)
                    screen.blit(min_step, (680, 250))
                # 显示 广度优先 的寻路过程
                if wayfinding == 'BFS':

                    for i,maze_b in enumerate(maze_pathfinding.BFS_process):
                        print(maze_b.shape[0])
                        screen.fill(bg_yellow)
                        skip_button.display()
                        screen.blit(step_title, (630, 130))
                        min_step = font_48.render(str(maze_pathfinding.BFS_step+1), True, GREE)
                        step_num = font_48.render(str(maze_pathfinding.step_list[i]), True, GREE)

                        back_button.display()
                        find_way_button.display()
                        screen.blit(min_step, (680, 250))
                        screen.blit(step_num, (720, 125))
                        screen.blit(min_step_title, (640, 200))

                        if wayfinding == 'DFS':
                            screen.blit(DFS, (method_x, 70))
                        if wayfinding == 'BFS':
                            screen.blit(BFS, (method_x, 70))
                        if wayfinding == 'ASTAR':
                            screen.blit(ASTAR, method_x, 70)

                        for event in pyevent.get():
                            if event.type == QUIT:
                                quit()
                                raise SystemExit

                        if find_way_button.check_click(mouse.get_pos()):
                            find_way_button = Button1('Find Way !', RED, 630, 450)
                        else:
                            find_way_button = Button1('Find Way !', WHITE, 630, 450)
                        if back_button.check_click(mouse.get_pos()):
                            back_button = Button1('BACK', RED, 670, 10)
                        else:
                            back_button = Button1('BACK', WHITE, 670, 10)
                        if skip_button.check_click(mouse.get_pos()):
                            skip_button = Button1('skip', RED, 670, 510)
                        else:
                            skip_button = Button1('skip', WHITE, 670, 510)
                        if mouse.get_pressed()[0]:
                            if skip_button.check_click(mouse.get_pos()):
                                screen.fill(bg_yellow)
                                maze_cfg.showMaze(maze_pathfinding.BFS_process[-1])
                                maze_cfg.showWall('source/wall2-16.png')
                                break

                        maze_cfg.showMaze(maze_b)
                        maze_cfg.showWall('source/wall2-16.png')
                        display.update()
                        btime = time.delay(10)
                    screen.fill(bg_yellow)
                    step_num = font_48.render(str(maze_pathfinding.step_list[-1]), True, GREE)
                    screen.blit(step_title, (630, 130))
                    screen.blit(min_step_title, (640, 200))
                    screen.blit(min_step, (680, 250))
                    screen.blit(step_num, (720, 125))

                    node_num =node(maze_pathfinding.BFS_process[-1]) + 2
                    maze_cfg.showMaze(maze_pathfinding.BFS_process[-1])
                    maze_cfg.showWall('source/wall2-16.png')
                #显示 A star 寻路过程
                if wayfinding == 'ASTAR':

                    for i, maze_a in enumerate(maze_pathfinding.ASTAR_process):
                        screen.fill(bg_yellow)
                        skip_button.display()
                        screen.blit(step_title, (630, 130))
                        min_step = font_48.render(str(maze_pathfinding.ASTAR_step_list[-1]), True, GREE)
                        step_num = font_48.render(str(maze_pathfinding.ASTAR_step_list[i]), True, GREE)

                        back_button.display()
                        find_way_button.display()
                        screen.blit(min_step, (680, 250))
                        screen.blit(step_num, (720, 125))
                        screen.blit(min_step_title, (640, 200))

                        if wayfinding == 'DFS':
                            screen.blit(DFS, (method_x, 70))
                        if wayfinding == 'BFS':
                            screen.blit(BFS, (method_x, 70))
                        if wayfinding == 'ASTAR':
                            screen.blit(ASTAR, (method_x, 70))
                        for event in pyevent.get():
                            if event.type == QUIT:
                                quit()
                                raise SystemExit

                        if find_way_button.check_click(mouse.get_pos()):
                            find_way_button = Button1('Find Way !', RED, 630, 450)
                        else:
                            find_way_button = Button1('Find Way !', WHITE, 630, 450)
                        if back_button.check_click(mouse.get_pos()):
                            back_button = Button1('BACK', RED, 670, 10)
                        else:
                            back_button = Button1('BACK', WHITE, 670, 10)
                        if skip_button.check_click(mouse.get_pos()):
                            skip_button = Button1('skip', RED, 670, 510)
                        else:
                            skip_button = Button1('skip', WHITE, 670, 510)
                        if mouse.get_pressed()[0]:
                            if skip_button.check_click(mouse.get_pos()):
                                screen.fill(bg_yellow)
                                maze_cfg.showMaze(maze_pathfinding.BFS_process[-1])
                                maze_cfg.showWall('source/wall2-16.png')
                                break

                        maze_cfg.showMaze(maze_a)
                        maze_cfg.showWall('source/wall2-16.png')
                        display.update()
                        btime = time.delay(100)
                    screen.fill(bg_yellow)
                    step_num = font_48.render(str(maze_pathfinding.ASTAR_step_list[-1]), True, GREE)
                    screen.blit(step_title, (630, 130))
                    screen.blit(min_step_title, (640, 200))
                    screen.blit(min_step, (680, 250))
                    screen.blit(step_num, (720, 125))

                    node_num = node(maze_pathfinding.ASTAR_process[-1]) + 2

                    maze_cfg.showMaze(maze_pathfinding.ASTAR_process[-1])
                    maze_cfg.showWall('source/wall2-16.png')

            if back_button.check_click(mouse.get_pos()):
                global modeSelect
                modeSelect = 1
                break

        for event in pyevent.get():
            if event.type == QUIT:
                quit()
                raise SystemExit

        back_button.display()
        find_way_button.display()

        # 显示更新
        display.flip()

# 界面显示 切换
def interface():
    #开始界面
    if modeSelect == 0:
        starting_screen()
    #设置界面
    if modeSelect == 1:
        setting_screen()
    #地图界面
    if modeSelect ==2:
        map()
#游戏主循环

# 默认进入开始界面   0（开始界面）  1（设置界面）   2（迷宫界面）
modeSelect =0

while True:
    interface()
    # try:
    #     clock = time.Clock()
    #     interface()
    # except:
    #     pass
    # else:
    #     pass



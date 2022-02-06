from mazelab.generators import random_maze
from mazelab.generators import random_shape_maze
'''使用 mazelab 模块 生成迷宫'''


# 生成随机迷宫
def Rand_maze(x,y):
    maze = random_maze(width=x, height=y, complexity=.1, density=50)
    return maze
# 生成随机形状迷宫
def Rand_shape_maze(w,h):
    maze = random_shape_maze(width=w, height=h, max_shapes=w, max_size=w/4, allow_overlap=True, shape=None)
    return maze














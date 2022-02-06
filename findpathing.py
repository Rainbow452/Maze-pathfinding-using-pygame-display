from collections import deque  # 双端队列

bg_yellow=(255,242,0)

def get_pos(coordinate, block_size, border_size):
    l, t = coordinate[1] * block_size + border_size[0], coordinate[0] * block_size + border_size[1]
    coordinate = (l + block_size // 2, t + block_size // 2)
    return coordinate

'''查表 有返回下标 无返回-1'''

dirs = [
    lambda x, y: (x + 1, y),  # 右
    lambda x, y: (x, y + 1),  # 下
    lambda x, y: (x - 1, y),  # 左
    lambda x, y: (x, y - 1),  # 上

]

def check(x, y, table):
    for index, item in enumerate(table):
        if item['x'] == x and item['y'] == y:
            return index
    return -1


#DFS 循环下列步骤
#1。从起点节点  检视四周  是否为0（路）：第一个0赋值为2（标记走过的路），坐标入栈
#2.栈中最后一个坐标检视四周为0赋值为2，否则将该坐标出栈
class pathfinding_maze():


     #寻路函数 输出路线数组
    def DFS_maze(self, x1, y1, x2, y2,in_maze):
        self.stack_=[]
        self.DFS_process = []
        stack = []
        self.DFS_step = 0
        self.DFS_out_maze = in_maze.copy()

        stack.append((x1, y1))
        self.DFS_out_maze[x1][y1] = 2  # 表示已经走过的路
        while len(stack) > 0:
            cur_node = stack[-1]
            if cur_node == (x2, y2): #到达终点
                for i , maze in enumerate(self.DFS_process): #图序号  i
                    maze[self.stack_[i][0],self.stack_[i][1]] = 3
                    maze[1, 1] = 0
                    maze[maze.shape[0] - 2, maze.shape[1] - 2] = 0


                for x,y in stack:
                    self.DFS_out_maze[x,y] = 3

                self.DFS_out_maze[1,1] = 0
                self.DFS_out_maze[self.DFS_out_maze.shape[0] - 2,self.DFS_out_maze.shape[1] - 2] = 0
                self.DFS_process.append(self.DFS_out_maze)
                self.DFS_step = len(stack) - 1

                break

            for d in dirs:
                next_x, next_y = d(*cur_node)
                #1 墙
                #2 探索过的路
                #3 最终路线
                if self.DFS_out_maze[next_x][next_y] == 0:
                    stack.append((next_x, next_y))
                    self.DFS_out_maze[next_x][next_y] = 2
                    self.maze_tmp = self.DFS_out_maze.copy()
                    self.DFS_process.append(self.maze_tmp)
                    self.stack_.append(stack[-1])
                    break
            else:
                stack.pop()
                self.maze_tmp = self.DFS_out_maze.copy()
                self.DFS_process.append(self.maze_tmp)
                if len(stack) != 0:
                    self.stack_.append(stack[-1])



    # BFS 使用队列解决迷宫BFS
    def BFS_maze(self,x1, y1, x2, y2,in_maze):
        self.step_list=[]
        self.real_step=0
        self.BFS_process = []
        self.BFS_out_maze = in_maze.copy()
        self.BFS_step = 0
        q = deque()
        path = []
        q.append((x1, y1, -1))
        self.BFS_out_maze[x1][y1] = 2
        while len(q) > 0:
            cur_node = q.popleft()
            path.append(cur_node)
            if cur_node[:2] == (x2, y2):
                realpath = []
                i = len(path) - 1
                while i >= 0:
                    realpath.append(path[i][:2])
                    i = path[i][2]
                realpath.reverse()

                self.BFS_step = len(realpath) - 1

                for i , maze in enumerate(self.BFS_process): #图序号  i

                    if self.real_step < len(realpath):
                        tmp_x = realpath[self.real_step][0]
                        tmp_y = realpath[self.real_step][1]
                        if self.real_step >0:
                            tmp_x_1 = realpath[self.real_step-1][0]
                            tmp_y_1 = realpath[self.real_step-1][1]


                        if maze[tmp_x,tmp_y] == 2:
                            maze[tmp_x, tmp_y] = 3
                            self.real_step += 1
                        else:
                            maze[tmp_x_1,tmp_y_1] = 3
                    self.step_list.append(self.real_step)
                    maze[1, 1] = 0
                    maze[maze.shape[0] - 2][maze.shape[1] - 2] = 0
                tmp_list = self.step_list
                self.step_list.append(tmp_list[-1])
                tmp_maze = self.BFS_process[-1]
                for r_x, r_y in realpath:
                    tmp_maze[r_x, r_y] = 3
                tmp_maze[1,1] = 0
                tmp_maze[self.BFS_out_maze.shape[0] - 2,self.BFS_out_maze.shape[1] - 2] = 0
                self.BFS_process.append(tmp_maze)
                break
            for d in dirs:
                next_x, next_y = d(cur_node[0], cur_node[1])
                if self.BFS_out_maze[next_x][next_y] == 0:
                    q.append((next_x, next_y, len(path) - 1))  # path列表n-1位置的点是它的父亲
                    self.BFS_out_maze[next_x][next_y] = 2
            maze_tmp = self.BFS_out_maze.copy()
            self.BFS_process.append(maze_tmp)



    def AStar_maze( self,x1,y1,x2,y2, in_maze):
        self.ASTAR_out_maze = in_maze.copy()
        self.ASTAR_input_maze = in_maze.copy()
        self.ASTAR_process = []
        real_step = 0
        self.ASTAR_step_list = []
        # ----计算曼哈顿距离
        def is_wall(x, y):
            if self.ASTAR_input_maze[x][y] ==1:
                return True
            return False

        def weight(x1, y1, x2, y2, dis):
            return dis + abs(x1 - x2) + abs(y1 - y2)
        path = []
        close = []  #走过的

        open = []   #能走的
        block = {'parent': -1, 'x': x1, 'y': y1, 'dis': 0,'f': 0}
        open.append(block)

        while open:
            open = sorted(open, key=lambda x: x['f'], reverse=True)
            block = open.pop()

            close.append(block)

            if block['x']  == x2 and block['y'] == y2:

                next = len(close) - 1
                while next != -1:
                    coordinate = (close[next]['x'], close[next]['y'])
                    path.append(coordinate)
                    next = close[next]['parent']
                path.reverse()

                for i, maze in enumerate(self.ASTAR_process):  # 图序号  i
                    if real_step < len(path):
                        tmp_x = path[real_step][0]
                        tmp_y = path[real_step][1]

                        if real_step > 0:
                            tmp_x2 = path[real_step - 1][0]
                            tmp_y2= path[real_step - 1][1]


                        if maze[tmp_x,tmp_y] == 2:
                            maze[tmp_x, tmp_y] = 3
                            real_step += 1

                        else:
                            maze[tmp_x2, tmp_y2] = 3
                        self.ASTAR_step_list.append(real_step)
                        maze[1,1] = 0
                        maze[maze.shape[0] - 2][maze.shape[1] - 2] = 0
                tmp_list = self.ASTAR_step_list
                self.ASTAR_step_list.append(tmp_list[-1])

                tmp_maze = self.ASTAR_out_maze.copy()
                for r_x, r_y in path:
                    tmp_maze[r_x, r_y] = 3
                tmp_maze[1, 1] = 0
                tmp_maze[self.ASTAR_out_maze.shape[0] - 2, self.ASTAR_out_maze.shape[1] - 2] = 0
                self.ASTAR_process.append(tmp_maze)

                self.ASTAR_step = len(path)


                # print(self.ASTAR_process)
                break




            for i,d in enumerate(dirs):
                x_tmp ,y_tmp= d(block['x'],block['y'])
                block_new = {'parent': check(block['x'],block['y'],close), 'x':x_tmp,'y':y_tmp,'dis': block['dis']+1,'f': weight(x_tmp,y_tmp,x2,y2,block['dis']+1) }
            # 检查是否在close中
                p = check(block_new['x'],block_new['y'],close)
                #没有墙且不在close中
                if  p == -1 and not is_wall(block_new['x'], block_new['y']):

                    #检查是否在open表中
                    idx = check(block_new['x'], block_new['y'], open)
                    if idx == -1:
                        open.append(block_new)

                        # 在 比较路径距离 短则更新
                    else:
                        if open[idx]['dis'] > block_new['dis']:
                            open[idx] = block_new
            for b in open:
                self.ASTAR_out_maze[b['x']][b['y']] = 2
            for b in close:
                self.ASTAR_out_maze[b['x']][b['y']] = 2
            aa = self.ASTAR_out_maze.copy()
            self.ASTAR_process.append(aa)









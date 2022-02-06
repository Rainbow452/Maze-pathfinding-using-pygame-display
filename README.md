# Maze-pathfinding-using-pygame-display
西安邮电大学智能科学与技术课设。   使用pygame作为可视化显示界面，mazelab包作为迷宫生成算法（迷宫生成是随机的）。

首先在设置界面 设置迷宫大小、迷宫类型、选用深度/广度优先算法(A* 作为扩展算法，在迷宫界面可以切换)，
在迷宫界面，可以看到迷宫寻路的过程，当前算法的步数等，以及算法切换。
可选择使用深度优先、广度优先、A*可视化

## 环境
**Python 3.8.8**  
**pygame 2.0.1** (SDL 2.0.14, Python 3.8.8)  
**mazelab** 项目链接（按介绍可安装） https://github.com/zuoxingdong/mazelab.git  
## 文件结构
**source:** 贴图、两个英文字体库、图标  
**findpathing.py:** 三种迷宫寻路算法。深度优先，广度优先，A* 算法  
**mazeMap:** 使用 _mazelab_ 生成迷宫  
**gui：** 界面显示（运行这个就行）  
其他文件没有用 :joy:  
## 可执行文件
可以使用 _py2exe_ 生成可执行文件(.exe)
但是生成的整个文件很大，有900+M

## 界面
界面只有三个: 开始界面、 设置界面、 迷宫界面   
### 开始界面  
![image](https://github.com/Rainbow452/Maze-pathfinding-using-pygame-display/blob/main/img/1.png)  
### 设置界面  
![image](https://github.com/Rainbow452/Maze-pathfinding-using-pygame-display/blob/main/img/2.png)  
### 迷宫界面  
![image](https://github.com/Rainbow452/Maze-pathfinding-using-pygame-display/blob/main/img/3.png)  

## 总结
这份代码是我在课设时突发奇想，想要做成一个类似游戏的可视化界面。查找资料时发现了pygame这个模块，于是在b站学习了一点pygame的使用方法，用不到两周的时间做出来的可视化界面。其中比较有趣的就是字体  和贴图了，这两个字体是在字体库上下载的，还有图标是在阿里矢量库上下载的。   

当然这个代码还是存在很多问题的，代码复用率很低，其中有至少1/3的代码是可以通过设计函数进行复用的。  这也导致了代码看起来很冗长。而且他还有很多bug你如果想要使用这个代码过课设，我的建议是，你可以改变一下部分贴图、 页面布局、颜色等等。因为我们   
  
可能是同一个老师 :joy:



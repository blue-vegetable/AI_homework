import settings
import copy

def dfs(maze_origin, start, end):
    """

    @param maze_origin: 二维列表，基本元素是字符，迷宫字符
    @param start: 元组 起始坐标
    @param end:  元组 终点坐标
    @return: 前置节点表 prev: 从终点向前倒推出路径。二维列表,基本元素是元组，存放前置结点
    """
    maze = []

    # 从maze_origin深拷贝一份到maze
    # 待补全 1
    maze = copy.deepcopy(maze_origin);


    prev = []

    # 根据maze的尺寸初始化prev，每个结点初始化为(-1,-1)
    # 待补全 2
    cols = len(maze[0])  #maze的列数
    rows = len(maze)     #maze的行数
    prev = [[(-1, -1) for col in range(cols)] for row in range(rows)]

    openlist = []
    openlist.append(start)
    maze[start[0]][start[1]] = settings.wall_char

    # dfs
    while len(openlist) != 0:

        # 从openlist将栈顶元素出栈->current
        # 待补全 3
        current = openlist.pop()

        # 如果current为终点end，则循环结束
        # 待补全 4
        if maze[current[0]][current[1]] == settings.end_char:
            break

        # 按照上-下-左-右的顺序依次扩展current四周的结点
        # 判断  如果当前结点current的四周不超出迷宫的范围 and 四周结点不是障碍字符，那么
        #               就进栈openlist成为带扩展的结点
        #               maze表对应的位置设置成障碍字符
        #               prev表对应的位置更新成当前位置
        # 待补全 5
        up = (current[0]-1, current[1])
        down = (current[0]+1, current[1])
        left = (current[0], current[1]-1)
        right = (current[0], current[1]+1)
        directions = [up, down, left, right]
        if up[0] >= 0 and down[0] <= rows and right[1] <= cols and left[1] >= 0:
            for i in directions:
                print(i[0], i[1])
                if maze[i[0]][i[1]] != settings.wall_char:
                    openlist.append(i)
                    if maze[i[0]][i[1]] != settings.end_char:
                        maze[i[0]][i[1]] = settings.wall_char
                    prev[i[0]][i[1]] = current

    return prev

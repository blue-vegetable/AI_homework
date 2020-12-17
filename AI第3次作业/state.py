from copy import deepcopy

class State:
    # 类属性
    # 深度最大值
    max_deep = 10
    # 目标状态
    end = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    """
    __init__ 初始化函数
    input：
        state节点状态
        deep深度
        parent(=None)父节点
    output：
        无output
    """

    def __init__(self, state, deep, parent=None):  # 初始化函数
        self.state = state
        self.deep = deep
        self.parent = parent
        self.cost = None

    def calculate_cost(self):
        end_state = self.end  # 目标状态
        h_cost = self.position_cost(end_state)  # 启发函数: 错位启发

        # 此处为A*算法，启发函数f(n) = d(n) + w(n)
        # 即f(n) = 搜索树的深度 + 放错位置的数字个数
        self.cost = self.deep + h_cost

    """ 
    get_cost函数，获取节点f(n)（代价函数）
    output：节点代价  
    """

    def get_cost(self):
        self.calculate_cost()  # 计算cost
        return self.cost

    """ 
        find_zero_pos函数，寻找当前节点状态中的0的坐标
        output：0的坐标 
        """
    def find_zero_pos(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    """ 
        get_subs函数，获取当前节点的扩展出的后继子节点
        output：后继子节点集sub_States  
    """

    def get_subs(self):
        sub_states = []  # 子节点集合
        # 获取空白（0）的坐标位置
        zero_x, zero_y = self.find_zero_pos()
        # 如果深度大于规定最大深度，返回空，目的为避免深度一直拓展
        if self.deep > self.max_deep:
            return None
        # 上移
            # 深拷贝一份self.state到s
            # 移动（修改s的内容不会影响原本的self.state
            # 初始化新节点new （利用State类的构造函数，参数列表为(state, deep, parent)）
            # new加入到sub_states
        s = deepcopy(self.state)
        if zero_x != 0:
            s[zero_x][zero_y], s[zero_x - 1][zero_y] = s[zero_x - 1][zero_y], s[zero_x][zero_y]
        new = State(s,self.deep+1,self)
        sub_states.append(new)
        # 下移
            # 同上
        s1 = deepcopy(self.state)
        if zero_x != 2:
            s1[zero_x][zero_y], s1[zero_x + 1][zero_y] = s1[zero_x + 1][zero_y], s1[zero_x][zero_y]
        new1 = State(s1, self.deep + 1, self)
        sub_states.append(new1)
        # 左移
            # 同上
        s2 = deepcopy(self.state)
        if zero_y != 0:
            s2[zero_x][zero_y], s2[zero_x][zero_y - 1] = s2[zero_x][zero_y - 1], s2[zero_x][zero_y]
        new2 = State(s2, self.deep + 1, self)
        sub_states.append(new2)
        # 右移
            # 同上
        s3 = deepcopy(self.state)
        if zero_y != 2:
            s3[zero_x][zero_y], s3[zero_x][zero_y + 1] = s3[zero_x][zero_y + 1], s3[zero_x][zero_y]
        new3 = State(s3, self.deep + 1, self)
        sub_states.append(new3)
        return sub_states

    """ 
    print函数：打印当前节点状态
    无input，output 
    """

    def print(self):
        for i in range(3):
            for j in range(3):
                print(self.state[i][j], end='   ')
            print("\n")
        # print("deep:%d,cost:%d"%(self.deep,self.cost))

    """
    position_cost函数：计算错位代价
    input：
        state：目标状态
    output：
        cost：错位代价
    """
    # 这里需要替换成【所有棋子与目标位置的曼哈顿距离之和】
    def position_cost(self, state):
        count = 0  # 计数器
        for i in range(3):
            for j in range(3):
                if (self.state[i][j] != 0 and  # 对应位非空白点
                        self.state[i][j] != state[i][j]):  # 对应位不相等
                    temp = self.state[i][j]
                    temp_i = i
                    temp_j = j
                    if temp== 4 or temp == 8:
                        temp_i = abs(temp_i - 1)
                    elif temp > 4:
                        temp_i = abs(temp_i - 2)
                    if temp == 3 or temp == 4 or temp == 5:
                        temp_j = abs(temp_j - 2)
                    elif temp  == 2 or temp == 6:
                        temp_j = abs(temp_j - 1)
                    count += temp_i + temp_j
        return count

import numpy as np
import copy
from collections import deque


class Maze:
    def __init__(self, maze, x_len, y_len):
        self.x_len = x_len  # 블록 정보
        self.y_len = y_len
        self.result = []

        h = maze.shape[0]  # 높이
        w = maze.shape[1]  # 넓이

        maze_map = np.zeros((h - y_len + 1, w - x_len + 1))
        for i in range(w - x_len + 1):
            for j in range(h - y_len + 1):
                # print(maze[i:i+x][j:j+x])
                if 1 not in maze[j:j + y_len, i:i + x_len]:
                    maze_map[j][i] = 1

        self.maze = maze
        # print(maze_map)
        self.maze_map = maze_map
        # print(maze_map)
        self.maze_map_2 = copy.deepcopy(maze_map)
        self.maze_map_h = maze_map.shape[0]
        self.maze_map_w = maze_map.shape[1]

        # print(self.x_len)
        # print(self.y_len)
        # print(self.maze_map)
        # print(maze)
        # asdf = input()

        # self.start = (self.maze_map_h, self.maze_map_w)
        # self.start = (0, 0)
        self.goal = (self.maze_map_h - 1, self.maze_map_w - 1)

    def find_start(self, flag):
        start = []
        result = []

        a = np.where(self.maze_map[0, :])  # 위
        b = np.where(self.maze_map[:, 0])  # 왼
        c = np.where(self.maze_map[:, -1])  # 오
        d = np.where(self.maze_map[-1, :])  # 아래

        a1 = [(0, j) for i in a for j in i]
        b1 = [(j, 0) for i in b for j in i]
        c1 = [(j, self.maze_map_w-1) for i in c for j in i]
        d1 = [(self.maze_map_h - 1, j) for i in d for j in i]

        start.append(a1)
        start.append(b1)
        start.append(c1)
        start.append(d1)

        for i in range(4):
            if flag[i]:
                result.extend(start[i])

        self.result = list(set(result))  # 중복 제거

        return self.result

    def nearest_side(self, start):
        route = [(i, j) for i in range(self.maze_map_h) for j in range(self.maze_map_w) if self.maze_map[i][j] > 1]
        # print("aval_route", route)
        side_4_str = ['up', 'down', 'left', 'right']

        if not route:  # 자기 자신 밖에 없으면
            asdf = input()
            route.append(start)

        min_side = start[0]
        min_side_index = 0
        near_index = start
        for i in route:
            up = i[0]
            left = i[1]
            down = self.maze_map_h - up - 1
            right = self.maze_map_w - left - 1
            side_4 = [up, down, left, right]
            side = min(side_4)
            side_index = side_4.index(min(side_4))
            if side < min_side:  # 여기 범위를 지정 해줘서 다른 출구도 찾을수 있게 하던지
                min_side = side
                min_side_index = side_index
                near_index = i
                # print("nearest side", side_4_str[side_index])

        return near_index, min_side_index  # 출구에서 가장 가까운 위치

    def obstruct_block(self, near, index):  # 출구로 나갈때 까지 블록의 경로 마스크
        side_4_str = [0, 1, 2, 3] # up,down,left,right
        if index == 0:
            self.maze_map[:near[0], near[1]] = 999
            self.maze[:near[0], near[1]:near[1] + self.x_len] = 999
        elif index == 1:
            self.maze_map[near[0]+1:, near[1]] = 999
            self.maze[near[0] + self.y_len - 1:, near[1]:near[1] + self.x_len] = 999
        elif index == 2:
            self.maze_map[near[0], :near[1]] = 999
            self.maze[near[0]:near[0] + self.y_len, :near[1]] = 999
        elif index == 3:
            self.maze_map[near[0], near[1]+1:] = 999
            self.maze[near[0]:near[0] + self.y_len, near[1] + self.x_len - 1 + 1:] = 999

        print(self.maze_map)
        print(self.maze)

    def bfs(self, start):
        dx = [-1, 1, 0, 0]  # 위로가는거 방지, 아래로 가는거 방지 [-1,1,0,0]
        dy = [0, 0, -1, 1]  # 왼쪽으로 가는거 방지, 오른쪽으로 가는거 방지 [0,0,-1,1]
        graph_list = []
        # 큐(Queue) 구현을 위해 deque 라이브러리 사용
        queue = deque()
        queue.append(start)
        # 큐가 빌 때까지 반복하기
        while queue:
            x, y = queue.popleft()
            # print("현재위치", x, y)
            # 현재 위치에서 4가지 방향으로의 위치 확인
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                # 미로 찾기 공간을 벗어난 경우 무시
                if nx < 0 or nx >= self.maze_map_h or ny < 0 or ny >= self.maze_map_w:
                    continue
                # 벽인 경우 무시
                if self.maze_map[nx][ny] == 0:
                    continue
                # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
                if self.maze_map[nx][ny] == 1:
                    graph_list.append((nx, ny))
                    self.maze_map[nx][ny] = self.maze_map[x][y] + 1
                    queue.append((nx, ny))
        # 가장 오른쪽 아래까지의 최단 거리 반환랜
        # print(graph_list) # 경로
        # self.maze_map[start[0], start[1]] = 100  # 출발지점 표시
        # print(self.maze_map)
        # return self.maze_map[self.maze_map_h - 1][self.maze_map_h - 1]
        # return sorted(graph_list)

        self.maze_map = self.maze_map_2

        return graph_list

    def search_path(self, start):
        dx = [-1, 1, 0, 0]  # 위로가는거 방지, 아래로 가는거 방지 [-1,1,0,0]
        dy = [0, 0, -1, 1]  # 왼쪽으로 가는거 방지, 오른쪽으로 가는거 방지 [0,0,-1,1]
        graph_list = []
        # 큐(Queue) 구현을 위해 deque 라이브러리 사용
        queue = deque()
        queue.append(start)
        # 큐가 빌 때까지 반복하기
        while queue:
            x, y = queue.popleft()
            # print("현재위치", x, y)
            # 현재 위치에서 4가지 방향으로의 위치 확인
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                # 미로 찾기 공간을 벗어난 경우 무시
                if nx < 0 or nx >= self.maze_map_h or ny < 0 or ny >= self.maze_map_w:
                    continue
                # 벽인 경우 무시
                if self.maze_map[nx][ny] == 0:
                    continue
                # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
                if self.maze_map[nx][ny] == 1:
                    graph_list.append((nx, ny))
                    self.maze_map[nx][ny] = self.maze_map[x][y] + 1
                    queue.append((nx, ny))
        # 가장 오른쪽 아래까지의 최단 거리 반환랜
        # print(graph_list) # 경로
        # self.maze_map[start[0], start[1]] = 100  # 출발지점 표시
        # print(self.maze_map)
        # return self.maze_map[self.maze_map_h - 1][self.maze_map_h - 1]
        # return sorted(graph_list)
        self.maze_map = self.maze_map_2
        return graph_list

    # def depth(self):


if __name__ == '__main__':
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0]]
    maze = np.array(maze)
    pos_loc = []
    s = Maze(maze, 3, 2)
    flag = [True, True, True, True]  # 출입구 지정 위, 왼, 오, 아
    print(s.maze_map)
    start = s.find_start(flag)
    # start = (0, 0)
    pos_loc.extend(s.bfs((0, 0)))
    print(pos_loc)
    if not pos_loc:
        pos_loc.append((0, 0))
    print("start", start)
    print(pos_loc)
    for i in start:
        if i in pos_loc:
            print("!!!!!!!!!!")

    print(s.maze_map)
    # pos_loc.extend(s.bfs((0, 0)))  # 검증용

    # for i in start:
    #     pos_loc.extend(s.bfs(i))

    print("pos_loc", sorted(pos_loc))
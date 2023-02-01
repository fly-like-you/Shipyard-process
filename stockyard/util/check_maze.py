import numpy as np
import copy
from collections import deque


class CheckMaze:
    def __init__(self, maze, x_len, y_len, num_map, start):
        self.x_len = x_len  # 블록 정보
        self.y_len = y_len
        self.result = []
        self.num_map = num_map
        self.maze = maze.map
        self.number = self.num_map[start[0], start[1]]

        h = self.maze.shape[0]  # 높이
        w = self.maze.shape[1]  # 넓이

        maze_map = np.zeros((h - y_len + 1, w - x_len + 1), dtype=np.uint32)
        for i in range(w - x_len + 1):
            for j in range(h - y_len + 1):
                # print(maze[i:i+x][j:j+x])
                if 1 not in self.maze[j:j + y_len, i:i + x_len]:
                    maze_map[j][i] = 1

        num_maze_map = np.full((h - y_len + 1, w - x_len + 1), None)
        self.num_maze_map_temp = np.full((h - y_len + 1, w - x_len + 1), None)
        for i in range(w - x_len + 1):
            for j in range(h - y_len + 1):
                # if self.number not in self.num_map[j:j + y_len, i:i + x_len]:
                num_maze_map[j][i] = {z for k in self.num_map[j:j + y_len, i:i + x_len] for z in k if z != 999}

        self.num_maze_map = num_maze_map

        self.maze_map = maze_map
        self.maze_map_temp = copy.deepcopy(self.maze_map)

        self.maze_map_h = maze_map.shape[0]
        self.maze_map_w = maze_map.shape[1]

        self.maze_map_2 = [[set() for _ in range(self.maze_map_w)] for _ in range(self.maze_map_h)]
        self.maze_map_2 = np.array(self.maze_map_2)
        self.maze_map_2_temp = copy.deepcopy(self.maze_map_2)

        # self.start = (self.maze_map_h, self.maze_map_w)
        # self.start = (0, 0)
        # self.goal = (self.maze_map_h - 1, self.maze_map_w - 1)

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

    def best_obstruct_blocktest(self, flag):
        start = []
        result = []

        a = np.where(self.num_maze_map_temp[0, :])  # 위
        b = np.where(self.num_maze_map_temp[:, 0])  # 왼
        c = np.where(self.num_maze_map_temp[:, -1])  # 오
        d = np.where(self.num_maze_map_temp[-1, :])  # 아래

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

        length = 1000
        short = 0

        for i in self.result:
            index = self.result.index(i)
            if len(self.num_maze_map_temp[i[0]][i[1]]) < length:
                length = len(self.num_maze_map_temp[i[0]][i[1]])
                short = index
        # try:
        path = self.num_maze_map_temp[self.result[short][0]][self.result[short][1]]
        path_list = []
        for i in self.result:
            if len(self.num_maze_map_temp[i[0]][i[1]]) == len(path):
                path_list.append(self.num_maze_map_temp[i[0]][i[1]])
        #     # print(self.num_maze_map_temp)
        # except Exception as e:
        #     print(self.num_map)
        #     print(e)
        #     print("!!!!!!!!!!!!!!!!")
        #     print(a)
        #     print(a1)
        #     print(start)
        #     print(self.result)
        #     print(short)
        #     print(self.num_maze_map_temp)
        #     exit()

        # return path
        return path_list

    def best_obstruct_block(self, flag):
        start = []
        result = []

        a = np.where(self.num_maze_map_temp[0, :])  # 위
        b = np.where(self.num_maze_map_temp[:, 0])  # 왼
        c = np.where(self.num_maze_map_temp[:, -1])  # 오
        d = np.where(self.num_maze_map_temp[-1, :])  # 아래

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

        length = 1000
        short = 0

        for i in self.result:
            index = self.result.index(i)
            if len(self.num_maze_map_temp[i[0]][i[1]]) < length:
                length = len(self.num_maze_map_temp[i[0]][i[1]])
                short = index
        # try:
        path = self.num_maze_map_temp[self.result[short][0]][self.result[short][1]]
        #     # print(self.num_maze_map_temp)
        # except Exception as e:
        #     print(self.num_map)
        #     print(e)
        #     print("!!!!!!!!!!!!!!!!")
        #     print(a)
        #     print(a1)
        #     print(start)
        #     print(self.result)
        #     print(short)
        #     print(self.num_maze_map_temp)
        #     exit()

        # return path
        return path
    # 해당블록에서 가장 가까운 입구 찾기
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

    # 가장 적은 간섭블록 탐색
    def dijkstra(self, start):
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        x, y = start
        self.num_maze_map_temp[x][y] = self.num_maze_map[x][y]
        node_list = []
        best_coor = (x, y)
        # best_coor 가 없을 때 까지 반복
        while best_coor:
            x, y = best_coor[0], best_coor[1]
            self.maze_map[x][y] = 999

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
                    coordinate = (nx, ny)
                    # 기존 맵이랑 비교해서 추가
                    edge = self.num_maze_map_temp[x][y] | self.num_maze_map[nx][ny]
                    node_list.append([coordinate, edge])

            length = 1000
            good = 0

            # 더 이상 찾는 노드가 없을 때 break
            if not node_list:
                break

            # 더 짧은 노드가 업데이트 되게
            for x in node_list:
                node = node_list.index(x)
                if len(x[1]) < length:
                    length = len(x[1])
                    good = node

            # 여기서 에러 발생 해서 pass
            best = node_list.pop(good)
            best_coor = best[0]

            # 맵 생성
            self.num_maze_map_temp[best_coor[0]][best_coor[1]] = best[1]

            # 리스트에서 삭제
            for x in node_list:
                if x[0][0] == best[0][0] and x[0][1] == best[0][1]:
                    # print("ok????")
                    node_list.remove(x)


    def bfs(self, start):
        dx = [-1, 1, 0, 0]  # 위로가는거 방지, 아래로 가는거 방지 [-1,1,0,0]
        dy = [0, 0, -1, 1]  # 왼쪽으로 가는거 방지, 오른쪽으로 가는거 방지 [0,0,-1,1]
        graph_list = []
        # 큐(Queue) 구현을 위해 deque 라이브러리 사용
        queue = deque()
        queue.append(start)
        # 큐가 빌 때까지 반복하기
        # stack = []
        # stack.append(start)
        # while stack:
        while queue:
            x, y = queue.popleft()
            # x, y = stack.pop()
            # 현재 위치에서 4가지 방향으로의 위치 확인
            num = self.num_maze_map[x][y]
            # print(num)
            ooo = copy.deepcopy(self.maze_map_2[x][y])
            # print(ooo)
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                # print("현재", id(self.maze_map_2[x][y]))
                # print("동고있는", id(self.maze_map_2[nx][ny]))
                # 미로 찾기 공간을 벗어난 경우 무시
                if nx < 0 or nx >= self.maze_map_h or ny < 0 or ny >= self.maze_map_w:
                    continue
                # 벽인 경우 무시
                if self.maze_map[nx][ny] == 0:
                    continue
                # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
                if self.maze_map[nx][ny] == 1:
                    graph_list.append((nx, ny))
                    # if num != 100:
                    ooo.update(num)
                    self.maze_map_2[nx][ny] = ooo
                    # self.maze_map[nx][ny] = self.maze_map[x][y] + 1
                    self.maze_map[nx][ny] = 999
                    queue.append((nx, ny))
                    # stack.append((nx, ny))
                # 다시 한번 들릴때 현재 경로가 더 좋으면 바꿔라 하지만
                if self.maze_map[nx][ny] == 999:  # and self.num_map[nx][ny] == 100:
                    temp = copy.deepcopy(self.maze_map)
                    # print(temp)
                    if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                        pass
                    else:
                        if all(y == 999 for y in self.num_maze_map[nx][ny]):
                            # print("바꿔")
                            self.maze_map_2[nx][ny] = ooo
                            # queue1 = deque()
                            # queue1.append((nx, ny))
                            # graph_list1 = []
                            # while queue1:
                            #     x1, y1 = queue1.popleft()
                            #     for j in range(4):
                            #         nx1 = x1 + dx[j]
                            #         ny1 = y1 + dy[j]
                            #         if nx1 < 0 or nx1 >= self.maze_map_h or ny1 < 0 or ny1 >= self.maze_map_w:
                            #             continue
                            #         if temp[nx1][ny1] == 0:
                            #             continue
                            #         if temp[nx1][ny1] == 100:
                            #             if all(y == 100 for y in self.num_maze_map[nx1][ny1]):
                            #                 queue1.append((nx1, ny1))
                            #                 temp[nx1][ny1] = 101
                            #                 graph_list1.append((nx1, ny1))
                            # # print(graph_list1)
                            # for k in graph_list1:
                            #     if len(self.maze_map_2[k[0]][k[1]]) < len(self.maze_map_2[x][y]):
                            #         pass
                            #     else:
                            #         self.maze_map_2[k[0]][k[1]] = ooo

                    # temp = copy.deepcopy(self.maze_map_2[nx][ny])
                    # for j in temp.copy():
                    #     if j in self.num_maze_map[nx][ny]:
                    #         if j != 100:
                    #             temp.remove(j)
                    # print(temp)

                    # if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                    #     pass
                    # else:
                    #     if all(y == 100 for y in self.num_maze_map[nx][ny]):
                    #         # print("바꿔")
                    #         self.maze_map_2[nx][ny] = ooo

                        # flag = False
                        # for x in self.num_maze_map[nx][ny]:
                        #     if any(y == x for y in ooo):
                        #         flag = True
                        #     else:
                        #         flag = False
                        #         break
                        # if flag:
                        #     print("바꿔봐")
                        #     self.maze_map_2[nx][ny] = ooo

                    # if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                    #     pass
                    # else:
                    #     self.maze_map_2[nx][ny] = ooo

                    # TODO 일단 100 이고 걔가 더 길더라도 블록번호들고있는놈 까지 고려해서 생각해라
                    # if all([x == self.num_map[nx][ny]for x in self.num_maze_map[nx][ny]]):
                    #     pass
                    # else:
                    #     if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                    #         pass
                    #     else:
                    #         self.maze_map_2[nx][ny] = ooo
        # 가장 오른쪽 아래까지의 최단 거리 반환
        # print(graph_list) # 경로
        # self.maze_map[start[0], start[1]] = 100  # 출발지점 표시
        # print(self.maze_map)
        # return self.maze_map[self.maze_map_h - 1][self.maze_map_h - 1]
        # print(num_list)
        print(self.num_map)
        print("method1")
        print(self.maze_map_2)
        print("블록번호", self.number)

        return sorted(graph_list)

    def bfs1(self, start):
        dx = [-1, 1, 0, 0]  # 위로가는거 방지, 아래로 가는거 방지 [-1,1,0,0]
        dy = [0, 0, -1, 1]  # 왼쪽으로 가는거 방지, 오른쪽으로 가는거 방지 [0,0,-1,1]
        graph_list = []
        # 큐(Queue) 구현을 위해 deque 라이브러리 사용
        queue = deque()
        queue.append(start)
        # 큐가 빌 때까지 반복하기
        # stack = []
        # stack.append(start)
        # while stack:
        while queue:
            x, y = queue.popleft()
            # x, y = stack.pop()
            # print("현재위치", x, y)
            # 현재 위치에서 4가지 방향으로의 위치 확인
            num = self.num_maze_map[x][y]
            # print(num)
            # print(self.maze_map_2_temp)
            ooo = copy.deepcopy(self.maze_map_2_temp[x][y])
            # print(ooo)
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                # print("현재", id(self.maze_map_2[x][y]))
                # print("동고있는", id(self.maze_map_2[nx][ny]))
                # 미로 찾기 공간을 벗어난 경우 무시
                if nx < 0 or nx >= self.maze_map_h or ny < 0 or ny >= self.maze_map_w:
                    continue
                # 벽인 경우 무시
                if self.maze_map_temp[nx][ny] == 0:
                    continue
                # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
                if self.maze_map_temp[nx][ny] == 1:
                    graph_list.append((nx, ny))
                    # if num != 100:
                    ooo.update(num)
                    self.maze_map_2_temp[nx][ny] = ooo
                    # self.maze_map[nx][ny] = self.maze_map[x][y] + 1
                    self.maze_map_temp[nx][ny] = 999
                    queue.append((nx, ny))
                    # stack.append((nx, ny))
                    # print(self.maze_map)
                    # print(self.num_map)
                    # print(self.maze_map_2)
                    # print(num)
                    # print(ooo)
                    # input()
                if self.maze_map[nx][ny] == 999:  # and self.num_map[nx][ny] == 100:
                    temp = copy.deepcopy(self.maze_map)
                    # print(temp)
                    if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                        pass
                    else:
                        if all(y == 999 for y in self.num_maze_map[nx][ny]):
                            # print("바꿔")
                            self.maze_map_2[nx][ny] = ooo
                # 다시 한번 들릴때 현재 경로가 더 좋으면 바꿔라 하지만
                # if self.maze_map[nx][ny] == 100:  # and self.num_map[nx][ny] == 100:
                #     temp = copy.deepcopy(self.maze_map_2[nx][ny])
                #     sadf = temp.copy()
                #     print(temp)
                #     for j in temp.copy():
                #         if j in self.num_maze_map[nx][ny]:
                #             if j != 100:
                #                 temp.remove(j)
                #     print(temp)
                #     if len(temp) < len(self.maze_map_2[x][y]):
                #         pass
                #     else:
                #         self.maze_map_2[nx][ny] = ooo


                    # if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                    #     pass
                    # else:
                    #     self.maze_map_2[nx][ny] = ooo

                    # TODO 일단 100 이고 걔가 더 길더라도 블록번호들고있는놈 까지 고려해서 생각해라
                    # if all([x == self.num_map[nx][ny]for x in self.num_maze_map[nx][ny]]):
                    #     pass
                    # else:
                    #     if len(self.maze_map_2[nx][ny]) < len(self.maze_map_2[x][y]):
                    #         pass
                    #     else:
                    #         self.maze_map_2[nx][ny] = ooo
        # 가장 오른쪽 아래까지의 최단 거리 반환
        # print(graph_list) # 경로
        # self.maze_map[start[0], start[1]] = 100  # 출발지점 표시
        # print(self.maze_map)
        # return self.maze_map[self.maze_map_h - 1][self.maze_map_h - 1]
        # print(num_list)
        print('method2')
        print(self.maze_map_2_temp)

        return sorted(graph_list)

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
    s = CheckMaze(maze, 3, 2)
    flag = [True, True, True, True]  # 출입구 지정 위, 왼, 오, 우
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
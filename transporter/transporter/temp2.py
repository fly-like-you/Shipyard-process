# 클래스와 함수 정의
import math
class Node:
    def __init__(self, node_no, position):
        self.node_no = node_no
        self.position = position
class Route:
    def __init__(self):
        self.nodes = []
        self.length = 0

    def add_node(self, node):
        self.nodes.append(node)

    def calculate_length(self):
        for i in range(len(self.nodes) - 1):
            x1, y1 = self.nodes[i].position
            x2, y2 = self.nodes[i + 1].position
            self.length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class Scheduler:
    def __init__(self, transporters, blocks):
        self.transporters = transporters
        self.blocks = blocks

    import math

    def schedule_dp(self):
        n = len(self.blocks)
        dp_table = [[math.inf] * n for _ in range(n)]

        # 초기값 설정
        for i in range(n):
            for j in range(n):
                if i == j:
                    dp_table[i][j] = 0
                else:
                    dp_table[i][j] = math.dist(self.blocks[i].end_pos, self.blocks[j].start_pos)

        # 동적계획법 테이블 갱신
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dp_table[i][j] = min(dp_table[i][j], dp_table[i][k] + dp_table[k][j] +
                                         math.dist(self.blocks[i].end_pos, self.blocks[k].start_pos) +
                                         math.dist(self.blocks[k].end_pos, self.blocks[j].start_pos))

        # 최적 순서 찾기
        works = []
        visited = [False] * n
        for i in range(n):
            min_dist = math.inf
            min_idx = -1
            for j in range(n):
                if not visited[j] and dp_table[0][j] < min_dist:
                    min_dist = dp_table[0][j]
                    min_idx = j
            visited[min_idx] = True
            works.append(self.blocks[min_idx])
        self.works = works

    def generate_routes(self, schedule):
        routes = []
        for i in range(len(schedule)):
            block = self.blocks[schedule[i]]
            route = Route()
            route.add_node(Node(block.start_node, block.start_pos))
            route.add_node(Node(block.end_node, block.end_pos))
            for j in range(i + 1, len(schedule)):
                next_block = self.blocks[schedule[j]]
                if block.end_node == next_block.start_node:
                    route.add_node(Node(next_block.end_node, next_block.end_pos))
                    block = next_block
            route.calculate_length()
            routes.append(route)
        return routes

    def distance(self, block1, block2):
        x1, y1 = block1.start_pos
        x2, y2 = block2.start_pos
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Transporter:
    def __init__(self, no, available_weight, empty_speed, work_speed):
        self.no = no
        self.available_weight = available_weight
        self.empty_speed = empty_speed
        self.work_speed = work_speed
        self.works = []

class Block:
    def __init__(self, no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos):
        self.no = no  # 블록 번호
        self.weight = weight  # 블록 중량
        self.start_node = start_node  # 시작 노드
        self.end_node = end_node  # 종료 노드 (시작 노드에서, 종료 노드까지 운반)
        self.start_time = start_time  # 작업 운반 가능 시간
        self.end_time = end_time  # 작업 deadline
        self.start_pos = start_pos  # 시작 노드 좌표
        self.end_pos = end_pos

import math


def dp_transport(transporters):
    def calculate_distance(block1, block2):
        return math.dist(block1.end_pos, block2.start_pos)

    blocks = transporters.works

    # 물건들을 deadline이 가장 빠른 순서로 정렬
    blocks = sorted(blocks, key=lambda x: x.end_time)

    # 동적 계획법을 사용하여 최단 경로 계산
    n = len(blocks)
    T = [[float('inf'), None] for i in range(n)]

    # 초기화
    for i in range(n):
        T[i][0] = math.dist([0, 0], blocks[i].start_pos) + math.dist(blocks[i].start_pos, blocks[i].end_pos)
        T[i][1] = None

    # 점화식 계산
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j and i != k and j != k:
                    d = T[i][0] + calculate_distance(blocks[i], blocks[j]) + T[k][0]
                    if d < T[j][0]:
                        T[j][0] = d
                        T[j][1] = i

    # 최단 거리를 만드는 작업 순서 계산
    order = []
    j = n - 1
    while j is not None:
        i = T[j][1]
        order.append(j)
        j = i

    # 작업 순서를 뒤집어서 반환
    order = order[::-1]
    return order

# 물건
block1 = Block(1, 5, "A", "B", 0, 5, (0, 0), (1, 1))
block2 = Block(2, 3, "B", "C", 1, 8, (1, 1), (2, 2))
block3 = Block(3, 2, "C", "D", 2, 10, (2, 2), (3, 3))

# 기계
transporter = Transporter(1, 10, 2, 1)
transporter.works.append(block1)
transporter.works.append(block2)
transporter.works.append(block3)

result = dp_transport(transporter)
print(result)  # 출력 결과: 최소 시간 값

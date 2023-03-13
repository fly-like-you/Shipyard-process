from transporter.transporter.create_data.Graph import Graph
class Block:
    def __init__(self, no, weight, start_node, end_node, start_time, end_time, graph):
        self.no = no  # 블록 번호
        self.weight = weight  # 블록 중량
        self.start_node = start_node  # 시작 노드
        self.end_node = end_node  # 종료 노드 (시작 노드에서, 종료 노드까지 운반)
        self.start_time = start_time  # 작업 운반 가능 시간
        self.end_time = end_time  # 작업 deadline
        self.dist = self.get_dist(graph)  # 시작노드와 종료노드 사이의 최단 거리
    def get_dist(self, graph: Graph):
        return graph.node_distance(self.start_node, self.end_node)

    def __str__(self):
        ret = 'no: {}, weight: {}, start_node: {}, end_node: {}, time: {} ~ {}, dist: {}' \
            .format(self.no, self.weight, self.start_node, self.end_node, self.start_time, self.end_time, self.dist)
        return ret


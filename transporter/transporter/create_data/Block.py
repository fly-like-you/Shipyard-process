class Block:
    def __init__(self, no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos):
        self.no = no  # 블록 번호
        self.weight = weight  # 블록 중량
        self.start_node = start_node  # 시작 노드
        self.end_node = end_node  # 종료 노드 (시작 노드에서, 종료 노드까지 운반)
        self.start_time = start_time  # 작업 운반 가능 시간
        self.end_time = end_time  # 작업 deadline
        self.start_pos = start_pos  # 시작 노드 좌표
        self.end_pos = end_pos  # 종료 노드 좌표

    def __str__(self):
        ret = 'no: {}, weight: {}, start_node: {}, end_node: {}, time: {} ~ {}, pos: {} -> {}' \
            .format(self.no, self.weight, self.start_node, self.end_node, self.start_time, self.end_time,
                    self.start_pos, self.end_pos)
        return ret



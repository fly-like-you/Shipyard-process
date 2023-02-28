import csv
# 입력 양식
def create_block():
    # 양식
    # print(block.no, block.weight, block.start_node, block.end_node,
    #       block.start_time, block.end_time, block.start_pos[0], block.start_pos[1], block.end_pos[0], block.end_pos[1])

    with open('lightBlocks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['no', 'weight', 'start_node', 'end_node', 'start_time', 'end_time', 'start_pos', 'end_pos'])

        while True:
            input_str = input("Enter block member (no weight start_node end_node start_time end_time start_pos end_pos): ")
            if input_str == '':
                break

            inputs = input_str.split(' ')

            no = int(inputs[0])
            weight = int(inputs[1])
            start_node = int(inputs[2])
            end_node = int(inputs[3])
            start_time = int(inputs[4])
            end_time = int(inputs[5])
            start_pos = [int(inputs[6]), int(inputs[7])]
            end_pos = [int(inputs[8]), int(inputs[9])]

            block = [no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos]

            writer.writerow(block)
create_block()
import csv
# 입력 양식
with open('blocks.csv', mode='w', newline='') as file:
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

import stockyard
import sys
#inital value
#epoch = 10, params = [[20, 20, 3, 7, 0, 100, 100]], flag = [True,True,True,True], methods = ['random']

# 여러 파라미터 확인
# '''params = [[20, 30, 3, 4, 0, 30, 30], [20, 30, 3, 4, 15, 30, 30],[20, 30, 3, 7, 0, 30, 30],[20, 30, 3, 7, 0, 100, 100]]'''

# 여러 메소드 확인
# [출입구 지정 위쪽, 왼쪽, 오른쪽, 아래쪽]
# flag = [[True,False,False,False], [True,True,False,False], [True,True,True,False],[True,True,True,True]]
flag = [[True, False, False, False]]
# methods = ['random', 'depth', 'quad2', 'quad4']
# methods = ['random', 'quad2','quad4']
# methods = ['random', 'depth', 'new']
methods = ['new']
params = [[20, 20, 3, 6, 0, 50, 50]]

# sys.stdout = open("test.txt", "a")

stockyard.sota(epoch=10, params=params, flag=flag, methods=methods)

# sys.stdout.close()

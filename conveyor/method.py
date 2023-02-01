import numpy as np
from conveyor.conveyor import *
from conveyor.util import *

#def bubble_search(works, iteration=10000):
#	works = np.array([work["time"] for work in works])
#	n_work, n_process_seq = works.shape
#
#	conveyor, conveyor_mask = get_conveyor(works)
#	_, n_seq = conveyor.shape
#
#	best_conveyor_time = cal_conveyor_time(conveyor)
#
#	performance = 0
#	_iter = 0
#	_time = 0
#	_n_effective = 0
#	best_iter = 0
#	best_time = 0
#
#	start_time = time.time()
#	while True:
#		tmp_best_conveyor_time = best_conveyor_time
#		for i in range(n_work-1):
#			_iter += 1
#			swap(works, conveyor, i, i+1)
#			tmp_conveyor_time = cal_conveyor_time(conveyor)
#			if best_conveyor_time > tmp_conveyor_time:
#				_n_effective += 1
#				best_iter = _iter
#				best_time = time.time() - start_time
#				best_conveyor_time = tmp_conveyor_time
#			else:
#				swap(works, conveyor, i, i+1)
#			
#		if tmp_best_conveyor_time == best_conveyor_time:
#			break
#		else:
#			continue
#
#	performance = best_conveyor_time
#	_time = time.time() - start_time
#
#	return works, [performance, _iter, _time, _n_effective, best_iter, best_time]

def random_search(works, iteration=10000):
	works = np.array([work["time"] for work in works])
	works = np.array(works)
	n_works, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	best_conveyor_time = cal_conveyor_time(conveyor)
	best_works = np.copy(works)
	index = np.arange(n_works)

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	for i in range(iteration):
		_iter += 1
		np.random.shuffle(index)
		works = works[index]

		conveyor, _ = get_conveyor(works)
		tmp_conveyor_time = cal_conveyor_time(conveyor)
		if best_conveyor_time > tmp_conveyor_time:
			_n_effective += 1
			best_iter = _iter
			best_time = time.time() - start_time
			best_conveyor_time = tmp_conveyor_time
			best_works = np.copy(works)

	performance = best_conveyor_time
	_time = time.time() - start_time

	return works, [performance, _iter, _time, _n_effective, best_iter, best_time]
	
def random_bubble_search(works, iteration=10000):
	works = np.array([work["time"] for work in works])
	works = np.array(works)
	n_work, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	best_conveyor_time = cal_conveyor_time(conveyor)
	best_works = np.copy(works)
	index = np.arange(n_work)

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	for i in range(iteration):
		np.random.shuffle(index)
		works = works[index]
		conveyor, conveyor_mask = get_conveyor(works)

		tmp_best_conveyor_time = best_conveyor_time
		_iter += 1
		while True:
			before_best_conveyor_time = tmp_best_conveyor_time
			for i in range(n_work-1):
				swap(works, conveyor, i, i+1)
				tmp_conveyor_time = cal_conveyor_time(conveyor)
				if tmp_best_conveyor_time >= tmp_conveyor_time:
					_n_effective += 1
					best_iter = _iter
					best_time = time.time() - start_time
					tmp_best_conveyor_time = tmp_conveyor_time
				else:
					swap(works, conveyor, i, i+1)
			if before_best_conveyor_time == tmp_best_conveyor_time:
				break
			else:
				continue

		if best_conveyor_time > tmp_best_conveyor_time:
			best_conveyor_time = tmp_best_conveyor_time
			best_works = np.copy(works)

	performance = best_conveyor_time
	_time = time.time() - start_time

	return works, [performance, _iter, _time, _n_effective, best_iter, best_time]

def unidev_search_half(works, iteration=10000):
	if type(works[0]) is dict:
		works = np.array([work["time"] for work in works])
	else:
		pass
	works = np.array(works)
	n_work, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	count = 0
	process_count = np.sum(conveyor_mask, axis=0)

	best_conveyor_time = cal_conveyor_time(conveyor)

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	time_collector = [[], [], []]
	while True:
		_iter += 1
		time_collect = time.time()#
		process_sum = np.sum(conveyor, axis=0)
		process_mean = process_sum/process_count
#
#		process_deviation = np.copy(conveyor)
#		for i in range(n_seq):
##			process_deviation[process_deviation[:, i]>0, i] -= process_mean[i]
#			process_deviation[conveyor_mask[:, i]>0, i] -= process_mean[i]
#		process_deviation = np.absolute(process_deviation)
#		
#		process_deviation_sum = np.sum(process_deviation, axis=0)
#		process_deviation_mean = nan_to_zero(process_deviation_sum/process_count)
#
#		seq_probability = roulette_wheel(process_deviation_mean)
##		seq_probability = softmax(process_deviation_mean)
#		seq_choice = np.random.choice(n_seq, 1, p=seq_probability)[0]
		time_collector[0].append(time.time()-time_collect)#
		time_collect = time.time()#

#		work_index = [i for i, cm in enumerate(conveyor_mask[:, seq_choice]) if cm == 1]
#		if len(work_index) == 1:
#			work_choice = work_index[0]
#		else:
#			work_probability = roulette_wheel(process_deviation[conveyor_mask[:, seq_choice]>0, seq_choice])
#			work_choice = np.random.choice(work_index, 1, p=work_probability)[0]
		work_choice = np.random.choice(np.arange(n_work), 1)[0]
		time_collector[1].append(time.time()-time_collect)#
		time_collect = time.time()#
		
		error_collect = []
		for i in range(n_work):
			error1 = sum(np.absolute(process_mean[i:i+n_process_seq] - works[work_choice]))
			error2 = sum(np.absolute(process_mean[work_choice:work_choice+n_process_seq] - works[i]))
			error_collect.append(error1+error2)
		swap_probability = roulette_wheel(error_collect, True)
		swap_choice = np.random.choice(range(n_work), 1, p=swap_probability)[0]
		time_collector[2].append(time.time()-time_collect)#

		swap(works, conveyor, work_choice, swap_choice)

		count += 1

		tmp_conveyor_time = cal_conveyor_time(conveyor)
		if best_conveyor_time > tmp_conveyor_time:
			_n_effective += 1
			best_iter = _iter
			best_time = time.time() - start_time
			best_conveyor_time = tmp_conveyor_time
			best_works = np.copy(works)
		else:
			swap(works, conveyor, work_choice, swap_choice)

		if count == iteration:
			break

	performance = best_conveyor_time
	_time = time.time() - start_time

	return best_works, [performance, _iter, _time, _n_effective, best_iter, best_time]

def unidev_search(works, iteration=10000):
	if type(works[0]) is dict:
		works = np.array([work["time"] for work in works])
	else:
		pass
	works = np.array(works)
	n_work, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	count = 0
	process_count = np.sum(conveyor_mask, axis=0)

	best_conveyor_time = cal_conveyor_time(conveyor)

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	time_collector = [[], [], []]
	while True:
		_iter += 1
		time_collect = time.time()#
		process_sum = np.sum(conveyor, axis=0)
		process_mean = process_sum/process_count

		process_deviation = np.copy(conveyor)
		for i in range(n_seq):
#			process_deviation[process_deviation[:, i]>0, i] -= process_mean[i]
			process_deviation[conveyor_mask[:, i]>0, i] -= process_mean[i]
		process_deviation = np.absolute(process_deviation)
		
		process_deviation_sum = np.sum(process_deviation, axis=0)
		process_deviation_mean = nan_to_zero(process_deviation_sum/process_count)

		seq_probability = roulette_wheel(process_deviation_mean)
#		seq_probability = softmax(process_deviation_mean)
		seq_choice = np.random.choice(n_seq, 1, p=seq_probability)[0]
		time_collector[0].append(time.time()-time_collect)#
		time_collect = time.time()#

		work_index = [i for i, cm in enumerate(conveyor_mask[:, seq_choice]) if cm == 1]
		if len(work_index) == 1:
			work_choice = work_index[0]
		else:
			work_probability = roulette_wheel(process_deviation[conveyor_mask[:, seq_choice]>0, seq_choice])
			work_choice = np.random.choice(work_index, 1, p=work_probability)[0]
		time_collector[1].append(time.time()-time_collect)#
		time_collect = time.time()#
		
		error_collect = []
		for i in range(n_work):
			error1 = sum(np.absolute(process_mean[i:i+n_process_seq] - works[work_choice]))
			error2 = sum(np.absolute(process_mean[work_choice:work_choice+n_process_seq] - works[i]))
			error_collect.append(error1+error2)
		swap_probability = roulette_wheel(error_collect, True)
		swap_choice = np.random.choice(range(n_work), 1, p=swap_probability)[0]
		time_collector[2].append(time.time()-time_collect)#

		swap(works, conveyor, work_choice, swap_choice)

		count += 1

		tmp_conveyor_time = cal_conveyor_time(conveyor)
		if best_conveyor_time > tmp_conveyor_time:
			_n_effective += 1
			best_iter = _iter
			best_time = time.time() - start_time
			best_conveyor_time = tmp_conveyor_time
			best_works = np.copy(works)
		else:
			swap(works, conveyor, work_choice, swap_choice)

		if count == iteration:
			break

	performance = best_conveyor_time
	_time = time.time() - start_time

	return best_works, [performance, _iter, _time, _n_effective, best_iter, best_time]

def unidev_search_simulated_anealing(works, iteration=10000):
	works = np.array([work["time"] for work in works])
	works = np.array(works)
	n_work, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	process_count = np.sum(conveyor_mask, axis=0)

	best_conveyor_time = cal_conveyor_time(conveyor)
	before_conveyor_time = best_conveyor_time

	T = before_conveyor_time
	k = 1.0
	c = 0.99

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	while True:
		_iter += 1
		process_sum = np.sum(conveyor, axis=0)
		process_mean = process_sum/process_count

		process_deviation = np.copy(conveyor)
		for i in range(n_seq):
#			process_deviation[process_deviation[:, i]>0, i] -= process_mean[i]
			process_deviation[conveyor_mask[:, i]>0, i] -= process_mean[i]
		process_deviation = np.absolute(process_deviation)
		
		process_deviation_sum = np.sum(process_deviation, axis=0)
		process_deviation_mean = nan_to_zero(process_deviation_sum/process_count)

		seq_probability = roulette_wheel(process_deviation_mean)
#		seq_probability = softmax(process_deviation_mean)
		seq_choice = np.random.choice(n_seq, 1, p=seq_probability)[0]

		work_index = [i for i, cm in enumerate(conveyor_mask[:, seq_choice]) if cm == 1]
		if len(work_index) == 1:
			work_choice = work_index[0]
		else:
			work_probability = roulette_wheel(process_deviation[conveyor_mask[:, seq_choice]>0, seq_choice])
			work_choice = np.random.choice(work_index, 1, p=work_probability)[0]
		
		error_collect = []
		for i in range(n_work):
			error1 = sum(np.absolute(process_mean[i:i+n_process_seq] - works[work_choice]))
			error2 = sum(np.absolute(process_mean[work_choice:work_choice+n_process_seq] - works[i]))
			error_collect.append(error1+error2)
		swap_probability = roulette_wheel(error_collect, True)
		swap_choice = np.random.choice(range(n_work), 1, p=swap_probability)[0]

		swap(works, conveyor, work_choice, swap_choice)

		tmp_conveyor_time = cal_conveyor_time(conveyor)
		if best_conveyor_time > tmp_conveyor_time:
			_n_effective += 1
			best_iter = _iter
			best_time = time.time() - start_time
			best_conveyor_time = tmp_conveyor_time
			best_works = np.copy(works)

		delta = tmp_conveyor_time - before_conveyor_time
		if delta <= 0:
			before_conveyor_time = tmp_conveyor_time
		else:
			p = np.exp(-(delta/(k*T)))
			if p == 0:
				break
			if np.random.rand() > p:
				before_conveyor_time = tmp_conveyor_time
			else:
				swap(works, conveyor, work_choice, swap_choice)

		T = c*T

	performance = best_conveyor_time
	_time = time.time() - start_time

	return best_works, [performance, _iter, _time, _n_effective, best_iter, best_time]
	
def simulated_anealing(works, mode, iteration=10000):
	works = np.array([work["time"] for work in works])
	"""
	mode : 0 // single change, pairwise interchange
	mode : 1 // multiple change, pairwise interchange
	mode : 2 // single change, adjacent interchange
	mode : 3 // multiple change, adjacent interchange
	"""

	works = np.array(works)
	n_work, n_process_seq = works.shape

	n_group = n_work//5

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	current_work = np.copy(works)
	current_conveyor, _ = get_conveyor(current_work)
	current_score = cal_conveyor_time(current_conveyor)

	best_works = np.copy(current_work)
	best_conveyor_time = current_score
	n = 0

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	start_time = time.time()
	while True:
		_iter += 1
		candidate_work = np.copy(current_work)
		candidate_conveyor = np.copy(current_conveyor)

		if mode == 0:
			group_select = np.random.randint(n_group)
			group_size = len(works[group_select*5:(group_select+1)*5])
			member_select1 = np.random.randint(group_size)
			member_select2 = np.random.randint(group_size)
			swap(candidate_work, candidate_conveyor, group_select*5+member_select1, group_select*5+member_select2)
		elif mode == 1:
			group_select = np.random.randint(n_group)
			group_size = len(works[group_select*5:(group_select+1)*5])
			member_select1= np.random.randint(group_size+1)
			
			if member_select1 != group_size:
				member_select2 = member_select1-1 if member_select1 != 0 else group_size-1
				swap(candidate_work, candidate_conveyor, group_select*5+member_select1, group_select*5+member_select2)
		elif mode == 2:
			for i in range(n_group):
				group_select = i
			
				group_size = len(works[group_select*5:(group_select+1)*5])
				member_select1 = np.random.randint(group_size)
				member_select2 = np.random.randint(group_size)
				swap(candidate_work, candidate_conveyor, group_select*5+member_select1, group_select*5+member_select2)
		elif mode == 3:
			for i in range(n_group):
				group_select = i

				group_size = len(works[group_select*5:(group_select+1)*5])
				member_select1= np.random.randint(group_size+1)
				
				if member_select1 != group_size:
					member_select2 = member_select1-1 if member_select1 != 0 else group_size-1
					swap(candidate_work, candidate_conveyor, group_select*5+member_select1, group_select*5+member_select2)

		candidate_score = cal_conveyor_time(candidate_conveyor)
#		delta = current_score - candidate_score
		delta = candidate_score - current_score

		T = np.log(2)/np.log(2+delta*n)
		u = np.random.random()

		if u < np.exp(np.log(2)/T):
			if n >= iteration:
				break
		else:
			current_work = np.copy(candidate_work)
			current_conveyor = np.copy(candidate_conveyor)
			current_score = candidate_score

			if best_conveyor_time > current_score:
				_n_effective += 1
				best_iter = _iter
				best_time = time.time() - start_time
				best_works = np.copy(current_work)
				best_conveyor_time = current_score
		n += 1

	performance = best_conveyor_time
	_time = time.time() - start_time

	return best_works, [performance, _iter, _time, _n_effective, best_iter, best_time]

def grid(works, works_type, iteration=10000):
	works_type_keys = list(works_type.keys())
		
	works_type_list = [work["type"] for work in works]
	works = np.array([work["time"] for work in works])
	n_work, n_process_seq = works.shape

	conveyor, conveyor_mask = get_conveyor(works)
	_, n_seq = conveyor.shape

	best_conveyor_time = cal_conveyor_time(conveyor)
	best_works = np.copy(works)
	index = np.arange(n_work)

	performance = 0
	_iter = 0
	_time = 0
	_n_effective = 0
	best_iter = 0
	best_time = 0

	for wtk in works_type_keys:
		for i in range(N_PROCESS-1):
			work_name = []
			time_diff = []

			for wtk_ in works_type_keys:
				work_name.append(wtk_)
				time_diff.append(euclidean(works_type[wtk]["time"][(1+i):], works_type[wtk_]["time"][:-(1+i)]))
			argsort_wtd = np.argsort(time_diff)
			for aw in argsort_wtd:
				works_type[wtk]["sort"][i].append(work_name[aw])

	start_time = time.time()

	for i in range(iteration):
		_iter += 1
		np.random.shuffle(index)
		works = works[index]
		works_type_list = [works_type_list[i_] for i_ in index]

		works_type_count = [0 for wtk in works_type_keys]
		for wtl in works_type_list:
			works_type_count[works_type_keys.index(wtl)] += 1

		for j in range(n_work-1):
			works_type_score = [0 for wtk in works_type_keys]
			if j == 0:
				for wtk in works_type_keys:
					for works_type_sort in works_type[wtk]["sort"]:
						for k, wts in enumerate(works_type_sort):
							works_type_score[works_type_keys.index(wts)] += k
			else:
				for k in range(j if N_PROCESS-1>j else N_PROCESS-1):
					for l, wts in enumerate(works_type[works_type_list[j-k-1]]["sort"][k]):
						works_type_score[works_type_keys.index(wts)] += len(works_type_keys)-(l+1)
			

			if j == 0:
				am = np.argmax(np.array(works_type_count)*np.array(works_type_score))
			else:
				am = np.argmax(np.array(works_type_count)*np.array(works_type_score))
			for k in range(j, n_work):
				if works_type_list[k] == works_type_keys[am]:
					break
			works[j], works[k] = works[k], works[j]
			works_type_list[j], works_type_list[k] = works_type_list[k], works_type_list[j]
			works_type_count[works_type_keys.index(works_type_list[j])] -= 1

		conveyor, _ = get_conveyor(works)
		tmp_conveyor_time = cal_conveyor_time(conveyor)
		if best_conveyor_time > tmp_conveyor_time:
			_n_effective += 1
			best_iter = _iter
			best_time = time.time() - start_time
			best_conveyor_time = tmp_conveyor_time
			best_works = np.copy(works)

	performance = best_conveyor_time
	_time = time.time() - start_time

	return best_works, [performance, _iter, _time, _n_effective, best_iter, best_time]

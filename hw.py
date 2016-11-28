residence_limit = 90  # 45, 60
schengen_constraint = 180

# сделали работу с длиной визитов более удобной
def visit_length (visit):
	return date_difference(visit[1], visit[0])

# функции надо объявлять до того как вы их вызовите
def get_days_for_visits(visits):
	days_for_visits = []
	for visit in visits:
	    days_for_visit = 0
	    for past_visit in visits:
	        if visit[0] - schengen_constraint < past_visit[0] < visit[0]:
	            days_for_visit += visit_length(past_visit)
	    days_for_visit += visit_length(visit)
	    days_for_visits.append(days_for_visit)
	return days_for_visits
	
def print_days_future_visit(visits, date_in_future):
	days_in_EU = 0
	for visit in visits:
		if visit[1] < date_in_future - schengen_constraint:
			continue
		elif visit[1] == date_in_future - schengen_constraint:
			days_in_EU += 1
		elif visit[0] <= date_in_future - schengen_constraint <= visit[1]:
			days_in_EU += visit_length([date_in_future - schengen_constraint, visit[1]])
		else:
			days_in_EU += visit_length([visit[0], visit[1]])
	if days_in_EU >= residence_limit:
		print('Вы не сможете въехать в выбранную дату')
	else:
		print('Вы сможете провести не больше {} дней в ЕС'.format(residence_limit - days_in_EU))
		
	# assert days_in_es == 90 - 20 - 20
	# обратите внимание, этой функции не нужен return

def print_residence_limit_violation(visits):
	days_for_visits = get_days_for_visits(visits)
	
	#при изменении кода он помогает нам удостовериться, что код работает как раньше
	#assert (days_for_visits == [10, 10 + 30, 10 + 30 + 40, 10 + 30 + 40 + 20, 40 + 20 + 20])
	
	for visit, total_days in zip(visits, days_for_visits):
	    if total_days > residence_limit:
	        overstay_time = total_days - residence_limit
	        print('Во время визита', visit, 'количество время пребывания превышено на', overstay_time, 'дней')

def add_visit():
	print('Начало:')
	start = int(input())
	print('Конец:')
	end = int(input())
	if start > end:
		print('Дата въезда не должна быть больше двты выезда')
		return
	if visits.count([start, end]) > 0:
		print('Визит {} уже есть в списке'.format([start, end]))
		return
	if not check_one_visit([start, end]):
		return
	visits.append([start, end])

def new_visit():
	start = int(input('Дата въезда:'))
	if start <= max(visits)[1]:
		print('Дата въезда должна быть больше даты последнего выезда ({})'.format(max(visits)[1]))
		return
	print_days_future_visit(visits, start)
	
def delete_visit():
	print('Начало:')
	start = int(input())
	print('Конец:')
	end = int(input())
	if visits.count([start, end]) == 0:
		print('Визита {} нет в списке'.format([start, end]))
		return
	visits.remove([start, end])
	print('Визит {} успешно удален'.format([start, end]))

visits = [[1, 10], [61, 90], [101, 110], [141, 160], [271, 290]]

def check_one_visit(visit):
	for another_visit in visits:
		if visit == another_visit:
			continue
		if not (visit[0] <= visit[1] < another_visit[0] or another_visit[1] < visit[0] <= visit[1]):
			print('Визит {} пересекается с визитом {}'.format(visit, another_visit))
			return False
	return True

def check_visits():
	for visit in visits:
		if len(visit) != 2 or visit[0] > visit[1]:
			print('Неправильно введен визит {}'.format(visit))
			return False
		if visits.count(visit) > 1:
			print('Визит {} встречается в списке дважды'.format(visit))
			return False
		if not check_one_visit(visit):
			return False
	return True

# бесконечный цикл
while True:
	#проверим список визитов
	if not check_visits():
		break
	print_residence_limit_violation(visits)
	#выбираю режим
	print('v - добавить визит')
	print('p - запланировать визит')
	print('r - удалить визит')
	print('e - выход')
	user_input = input()
	if user_input == 'v':
		add_visit()
	elif user_input == 'p':
		new_visit()
	elif user_input == 'r':
		delete_visit()
	elif user_input == 'e':
		break

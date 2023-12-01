from collections import Counter


# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2

students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]

value_counts = Counter(s['first_name'] for s in students)
print('\n'.join(f'{name}: {cnt}' for name, cnt in value_counts.items()))

# через цикл:
tmp = {}
for student in students:
    name = student['first_name']
    tmp.setdefault(name, 0)
    tmp[name] += 1
print('\n'.join(f'{name}: {cnt}' for name, cnt in tmp.items()))


# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]
value_counts = Counter(s['first_name'] for s in students)
res = value_counts.most_common()[0]
print(f'Самое частое имя среди учеников: {res[0]}')

# через цикл:
tmp = {}
most_common_name = {'name': '', 'cnt': 0}
for student in students:
    name = student['first_name']
    tmp.setdefault(name, 0)
    tmp[name] += 1
    if tmp[name] > most_common_name['cnt']:
        most_common_name['name'] = name
        most_common_name['cnt'] = tmp[name]
print(f'Самое частое имя среди учеников: {most_common_name["name"]}')


# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ], [  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
for class_num, students in enumerate(school_students, 1):
    most_common_name = Counter(s['first_name'] for s in students).most_common()[0]
    print(f'Самое частое имя в классе {class_num}: {most_common_name[0]}')

# через цикл
tmp = []
for class_num, students in enumerate(school_students, 1):
    most_common_name = {'name': '', 'cnt': 0}
    tmp = {}
    for student in students:
        name = student['first_name']
        tmp.setdefault(name, 0)
        tmp[name] += 1
        if tmp[name] > most_common_name['cnt']:
            most_common_name['name'] = name
            most_common_name['cnt'] = tmp[name]
    print(f'Самое частое имя в классе {class_num}: {most_common_name["name"]}')



# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2в', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}


for row in school:
    tmp = {'girls': 0, 'boys': 0,}
    for student in row['students']:
        if is_male[student['first_name']]:
            tmp['boys'] += 1
        else:
            tmp['girls'] += 1
    print(f'Класс {row["class"]}: девочки {tmp["girls"]}, мальчики {tmp["boys"]} ')


# Задание 5
# По информации об учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}

res = {'girls_class': '', 'girls_cnt': 0, 'boys_class': '', 'boys_cnt': 0 }
for row in school:
    tmp = {'girls': 0, 'boys': 0,}
    for student in row['students']:
        if is_male[student['first_name']]:
            tmp['boys'] += 1
        else:
            tmp['girls'] += 1
    if tmp['girls'] > res['girls_cnt']:
        res['girls_class'] = row['class']
        res['girls_cnt'] = tmp['girls']
    if tmp['boys'] > res['boys_cnt']:
        res['boys_class'] = row['class']
        res['boys_cnt'] = tmp['boys']
print(f'Больше всего мальчиков в классе {res["boys_class"]}')
print(f'Больше всего девочек в классе {res["girls_class"]}')


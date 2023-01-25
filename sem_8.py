# Вычислить значение выражения

# Уровень 1:
# 1 действие
# 2 аргумента 12 + 15
# Уровень 2:
# Количество действий произвольное
# 12 + 15 - 4

# Уровень 3:
# Действия имеют приоритет
# 12 - 4*2 +6/3

# Уровень 4 * (дополнительная задача, сдавать не обязательно)
# Действия разделяются скобками
# (12 - 4) * 2
import re

'''выбор типа для числа, если в результате промежуточного 
деления получается вещественное число'''

def chooseNumType(text):
    if '.' in text:
        return float(text)
    return int(text)


'''разбиение строки для 2 и 3 уровней'''

def separating(text):
    '''отсекаются случаи, такие как 6 + (-5), чтобы в массиве были значения [6, '+', -5], 
    а также случаи, когда не хватает пробелов или есть лишние:'''
    text = text.replace(' ', '').replace('(', '').replace(')', '') 
    temp = ''
    if text[0] == '-': 
        n = 1
        res = ['-']
    else:
        n = 0
        res = []
    for i in range(n, len(text)):
        if text[i].isdigit() or text[i] == '.':
            temp += text[i]
            if i == len(text) - 1: 
                res.append(chooseNumType(temp))
        elif text[i] in '+-/*^' and text[i - 1].isdigit():
            res.append(chooseNumType(temp))
            res.append(text[i])
            temp = ''
        
        elif text[i] == '-' and text[i - 1] in '+-/*^': 
            temp = '-'           
    if res[0] == '-':
        res.pop(0)
        res[0] = - res[0]
    return res

'''Первый уровень'''

def calcFirstlevel(a, b, c):
    if c == '+': return a + b
    if c == '-': return a - b
    if c == '*': return a * b
    if c == '/': return a / b
    if c == '^': return a ** b

print('test of the first level: ', calcFirstlevel(3, 2, '*'))

'''Второй уровень'''
def calcSecondLevel(text):
    temp_list = separating(text)
    while len(temp_list) > 1:
        for i in range(1, len(temp_list), 2):
            temp = calcFirstlevel(temp_list[i - 1], temp_list[i + 1], temp_list[i])
            temp_list[i - 1] = temp
            temp_list.pop(i)
            temp_list.pop(i)
            break
    return temp_list[0]

print('test of the second level: ', calcSecondLevel('13 - 5 +10 +100'))

'''Третий уровень'''
def calcThirdLevel(text):
    temp_list = separating(text)
    while '^' in temp_list:
        i = temp_list.index('^')
        temp = calcFirstlevel(temp_list[i - 1], temp_list[i + 1], temp_list[i])
        temp_list[i - 1] = temp
        temp_list.pop(i)
        temp_list.pop(i)
    while '*' in temp_list or '/' in temp_list:
        for i in range(1, len(temp_list)):
            if temp_list[i] in ['*', '/']:
                temp = calcFirstlevel(temp_list[i - 1], temp_list[i + 1], temp_list[i])
                temp_list[i - 1] = temp
                temp_list.pop(i)
                temp_list.pop(i)
                break
    if len(temp_list) > 1:
        text_temp = ''.join(map(str, temp_list))
        return calcSecondLevel(text_temp)
    else: return temp_list[0]

print('test of the third level: ', calcThirdLevel('12 - 4*2 +6/3'))

'''Четвертый уровень'''
def calc(text):
    pattern = r'.*?(\([^()]{3,}\)).*?'
    while re.findall(pattern, text):
        temp = re.findall(pattern, text)
        for item in temp:
            res_temp = calcThirdLevel(item[1:-1])
            text = text.replace(item, str(res_temp))
    return calcThirdLevel(text)


print('test of the fourth level: ', calc('(12 - 4) * 2'))
print('Еще немного тестов: ')
print('(-2 +(3 - 5)*6 + (-6 - 3)) / (2 - 1) * (-5^-1) = ', calc('(-2 +(3 - 5)*6 + (-6 - 3)) / (2 - 1) * (-5^-1)'))
print('( 10 - 5 ) * ( 2 + 3 ) - 1 + ( 4 * ( 20 - 20 / ( 5 - 1 ))) * ( 2 + 7 ) = ' , calc('( 10 - 5 ) * ( 2 + 3 ) - 1 + ( 4 * ( 20 - 20 / ( 5 - 1 ))) * ( 2 + 7 )'))
print('((2    + 3  ) ^2 -1) / 2^  3 = ' , calc('((2    + 3  ) ^2 -1) / 2^  3'))
print('((2+3)^2-1)/2^ (-3) = ' , calc('((2+3)^2-1)/2^ (-3)'))



while True:
    try:
        n = input("Введите числовое выражение, которое хотите вычислить либо enter, чтобы выйти из калькулятора >>> ")
        if n:
            print(n, calc(n), sep = ' = ')
        else:
            print('Хорошего дня! До новой встречи!') 
            break
    except ZeroDivisionError:
        print('В результате вычислений в знаменателе получился 0. Ошибка деления на 0')
    except:
        print("Введено некорректное математическое выражение, проверьте и повторите запрос")
print()
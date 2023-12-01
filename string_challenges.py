# Вывести последнюю букву в слове
word = 'Архангельск'
print(word[-1])


# Вывести количество букв "а" в слове
word = 'Архангельск'
print(len([l for l in word if l == 'а']))
print(len([l for l in word.lower() if l == 'а']))  # если без учета регистра


# Вывести количество гласных букв в слове
word = 'Архангельск'
print(len([l for l in word.lower() if l in ['а', 'е', 'и', 'о', 'у', 'э', 'ю', 'я']]))

# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(len([w for w in sentence.split() if len(w) > 1 or w.lower() == 'я']))


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
print('\n'.join([w[0] for w in sentence.split() if len(w) > 1 or w.lower() == 'я']))


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
words = [len(w) for w in sentence.split() if len(w) > 1 or w.lower() == 'я']
from functools import reduce
print((reduce(lambda x, y: x + y, words))/len(words))

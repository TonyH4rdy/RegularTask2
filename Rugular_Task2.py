# УСЛОВИЕ :
# Иногда при знакомстве мы записываем контакты в адресную книгу кое-как, с мыслью,
# что когда-нибудь потом всё обязательно поправим. Копируем данные из интернета или из смс.
# Добавляем людей в разных мессенджерах. В результате получается адресная книга, в которой
# невозможно кого-то найти: мешает множество дублей и разная запись одних и тех же имен.
#
# Кейс основан на реальных данных из https://www.nalog.ru/opendata/, https://www.minfin.ru/ru/opendata/.
#
# Ваша задача: починить адресную книгу, используя регулярные выражения.
# Структура данных будет всегда:
# lastname,firstname,surname,organization,position,phone,email
# Предполагается, что телефон и e-mail у человека может быть только один.
#
# Необходимо:
## 1)Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
# Подсказка: работайте со срезом списка ( три первых элемента ) при помощи " ".join([:2]) и split(" ").
# Регулярки здесь не нужны .
# 2)Привести все телефоны в формат +7(999)999-99-99.
# Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
# 3)Объединить все дублирующиеся записи о человеке в одну.

import csv
from pprint import pprint
import re

# Читаем CSV- файл , сохраняем в виде списка списков contacts_list
with open('phonebook_raw.csv' , encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# print(contacts_list)  # [['lastname', 'f...], ['Усольцев Олег Валентинович', '', '', 'ФНС', 'главный специалист

# Порядок в записи ФИО
for elem in contacts_list :

  # Выделили нулевой элемент текущего элемента  списка
  elem_zero = elem[0]
  # Выделили первый элемент текущего элемента  списка
  elem_first = elem[1]
  # print(elem_zero)
  # Преобразовали нулевой и  первый элемент в список
  elem_zero_list = elem_zero.split()
  elem_first_list = elem_first.split()
  # print (elem_zero_list)
  # Переписали , когда ФИО записаны в первой ячейке
  if len(elem_zero_list) == 3 :
    elem[0]=elem_zero_list[0]
    elem[1] = elem_zero_list[1]
    elem[2] = elem_zero_list[2]
  #   # Переписали , когда ФИ записаны в первой ячейке
  if len(elem_zero_list) == 2 :
    elem[0]=elem_zero_list[0]
    elem[1] = elem_zero_list[1]

  # Переписали, когда ИО написаны во 2-й ячейки
  if len(elem_first_list) == 2 :
    elem[1] = elem_first_list[0]
    elem[2] = elem_first_list[1]

#print(contacts_list)

# Заполняем пустые ячейки  в данных :

# Проход от первого списка из contacts_list:
for i in range(len(contacts_list)):
  # Проход от второго списка из contacts_list:
    for q in range(i + 1, len(contacts_list)):
      # Проход по внутренним элементам  списка :
        for j in range(len(contacts_list[0])):
          # Проверка условия совпадений ФИ и наличия пустой ячейки
            if contacts_list[i][0] == contacts_list[q][0]  and contacts_list[i][1] == contacts_list[q][1] and contacts_list[i][j] == '':
                # Заполнение пустых ячеек первой записи для дубликатов по ФИ
                contacts_list[i][j]+=contacts_list[q][j]

# print (len(contacts_list),contacts_list)


# Рабочий список из первых 2-х составляющих из элементов списка списков
double_list=[]

# Выходной список без повторений:
out_list = []
# Формируем новый список без повторений по фамилии и имени
for el in contacts_list:
    doub = " ".join(el[:2])
    if doub not in double_list :
        double_list.append(doub)
        out_list.append(el)
#print(double_list)
# Для контроля :
print(len(out_list),out_list)


# Выражение для поиска номера
pattern =r"(\+7|8)\s*\(?(495)\)?[\s-]*(\d{3})[-]*(\d{2})[\s-]*(\d+)\s*\(?(доб.)?\s?(\d+)?\)?"
# Для форматирования номера
sub_ = r" +7(\2)\3-\4-\5 \6\7 "

# Переписываем номера телефонов по единому шаблону pattern
# Формируем финишный список списков. Создаём пустой шаблон
contacts_list_out = []
# Проходим циклом по списку списков out_list :
for elem in out_list:
    # Создаём пустой список для текущей итерации
    elem_list=[]
    # Проходим циклом по элементам текущего списка
    for el in elem:
        # Проверяем каждый элемент списка . Если в нём номер телефона - переписываем его по нужному шаблону
        result = re.sub(pattern, sub_, el)
        # Заполняем текущий список данными
        elem_list.append(result)
    # Добавляем изменённый список текущей итерации в финишный список списков
    contacts_list_out.append(elem_list)
# Для контроля - проверяем результат
print(contacts_list_out)

# Записываем финишный список списков в CSV-файл 'phonebook_2.csv'
with open('phonebook_2.csv', 'w',encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list_out)
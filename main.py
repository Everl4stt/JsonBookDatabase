import json
import os


'''
Функция меню с обработкой всех возможных значений ,которые введет пользователь
'''
def menu():
    while True:
        print('Вы в главном меню библиотеки, выберите опцию из перечисленных\n'
        'Для того, чтобы выбрать опцию, введите в консоль её номер из списка:\n'
              '\t1. Просмотр списка книг \n'
              '\t2. Добавление книги в библиотеку \n'
              '\t3. Сохранить изменения \n'
              '\t4. Найти книгу в библиотеке \n'
              '\t5. Удаление книги из библиотеки\n'
              '\t6. Поменять статус книги\n'
              '\t7. Выход\n')
        option = input()
        if option not in ('1', '2', '3', '4', '5', '6', '7'):
            print(f'Варианта {option} нет в списке, попробуйте выбрать из списка\n')
        else:
            break
    return option

'''
Функция для чтения информации о хеш-таблицах из json файла в переменную
Если хеш-таблицы еще не создавались, то создаются json файлы со списком пустых словарей размером 2^16 
'''
def get_hash_data(hash_file_name):
    if not os.path.exists(hash_file_name):
        with open(hash_file_name, 'w', encoding='utf-8') as f:
            json.dump([{} for _ in range(65536)], f, ensure_ascii=False, indent=4)
    with open(hash_file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

'''
Функция получения базы данных из json файла
В случае ,когда файл отсутствует, он создается пустым
'''
def get_data(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4 )
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

'''
Глобальные переменные, содержащие в себе хеш-таблицы для быстрого поиска по трем параметрам
:hash_table_title: Хеш-таблица по названию
:hash_table_author: Хеш-таблица по автору
:hash_table_year: Хеш-таблица по году издания
'''
hash_table_title = get_hash_data('hash_table_title.json')
hash_table_author = get_hash_data('hash_table_author.json')
hash_table_year = get_hash_data('hash_table_year.json')

'''
Функция сохранения данных в json файл
'''
def save_data(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

'''
Функция добавления новой записи в локальную переменную, содержащую базы данных
Возможность ничего не ввести и вернуться в главное меню
Также внутри проверка валидности данных с помощью отдельной функции isdatavalid
При добавлении status устанавливается автоматически для каждой записи на 'в наличии'
Если в переменной spaces есть данные о пропущенных id то в первую очередь они занимаются новыми данными
Сразу после добавления данные добавляются в хеш-таблицы для ускоренного поиска
В качестве id каждой записи используется ее порядковый номер в базе
'''
def add_data(data, spaces):
    title = input('Введите название книги: (или нажмите Enter для возврата в меню) ')
    if not title:
        print('Вы ничего не ввели, возврат в меню\n')
        return
    author = input('Введите автора книги (или нажмите Enter для возврата в меню): ')
    if not author:
        print('Вы ничего не ввели, возврат в меню\n')
        return
    title = title.strip().upper()
    author = author.strip().lower().capitalize()
    if isdatavalid(title=title, author=author) or not data:
        year = input('Введите год издания книги (или нажмите Enter для возврата в меню): ')
        if not year:
            print('Вы ничего не ввели, возврат в меню\n')
            return
        year = year.strip().lower()
        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии',
        }
        if spaces:
            position = spaces[0]
            data[spaces.pop(0)] = new_book
        else:
            data.append(new_book)
            position = len(data) - 1
        print(f'Новая книга "{new_book['title']}" добавлена в библиотеку!\n')
        hash_table_add(hash_table=hash_table_title,     key=title,  value=position)
        hash_table_add(hash_table=hash_table_author,    key=author, value=position)
        hash_table_add(hash_table=hash_table_year,      key=year,   value=position)
    return data, spaces

'''
Функция добавления информации в хеш-таблицу с учетом возможных коллизий
'''
def hash_table_add(hash_table, key, value):
    if key in hash_table[hash(key)]:
        hash_table[hash(key)][key].append(value)
    else:
        hash_table[hash(key)][key] = [value]

'''
Функция проверки данных на совпадения, чтобы избежать дубликатов в базе
'''
def isdatavalid(title, author):
        if search_data(title=title, author=author) == 'Ничего не нашлось\n':
            return True
        print('Такая книга этого автора уже есть в библиотеке\n')
        return False

'''
Функция красивого вывода данных из базы в консоль, с учетом возможности использования этой функции
после поиска для вывода данных
'''
def show_data(data, positions=None):
    result = ''
    if positions == 'Ничего не нашлось\n':
        return positions
    if not positions:
        for id, books in enumerate(data):
            if books:
                result += (''.join(f'{id}: {books['title']}, {books['author']}, {books['year']} год, {books['status']}')
                           + '\n')
        return result
    for n in positions:
        result += (''.join(f'{n}: {data[n]['title']}, {data[n]['author']}, {data[n]['year']} год, {data[n]['status']}')
                    + '\n')
    return result

'''
Функция удаления данных из базы по ее id (т. е. порядковому номеру), 
а также каскадное удаление этой записи из хеш-таблиц
При удалении записи ее номер попадает в переменную spaces, чтобы следующие записи заняли место удаленной,
с учетом сохранения у всех записей порядкового номера без смещения
Учитывается возможность пользовательского ввода других возможных вариантов 
'''
def del_data(data, spaces):
    search_id = input('Введите id книги, которую хотите удалить (или нажмите Enter для возврата в меню)\n')
    if not search_id:
        print('Вы ничего не ввели, возврат в меню\n')
        return
    try:
        search_id_int = int(search_id)
    except ValueError:
        print('Книги с таким id нет в библиотеке\n')
        return
    if search_id_int in range(len(data)) and search_id_int not in spaces:
        print(f'Книга "{data[search_id_int]['title']}" c id: {search_id_int}  удалена из библиотеки\n')
        hash_table_del(hash_table=hash_table_title,   key=data[search_id_int]['title'],   value=search_id_int)
        hash_table_del(hash_table=hash_table_author,  key=data[search_id_int]['author'],  value=search_id_int)
        hash_table_del(hash_table=hash_table_year,    key=data[search_id_int]['year'],    value=search_id_int)
        data[search_id_int] = None
        spaces.append(search_id_int)
    else:
        print('Книги с таким id нет в библиотеке\n')
    return data, spaces

'''
Функция удаления данных из хеш-таблицы
'''
def hash_table_del(hash_table, key, value):
    hash_table[hash(key)][key].remove(value)

'''
Функция хеширования данных:
Применяем XOR (исключающее ИЛИ) к каждому символу в строке, умножаем результат на 'магическое число' 
В конце возвращаем остаток от деления на максимальный размер таблицы для избежания выхода за предела массива
'''
def hash(string):
    hash = 0x811c9dc5
    for char in string:
        hash ^= ord(char)
        hash *= 0x01000193
    return hash % 65536

'''
Функция поиска данных, учитывающая возможность ее вызова из других функция с заданными параметрами, 
вместо введенных пользователем
Поиск происходит с помощью трех хеш-таблиц, это ускоряет его для больших баз, вместо просто перебора всех данных
и сравнивания их с нужными
В качестве параметров поиска можно как задать все три: автора, название и год выпуска, так и пропустить любой из них
После ввода данных пользователем ни форматируются, поэтому регистр не важен
'''
def search_data(title=None, author=None, year=None):
    result = set()
    if not title:
        print('Введите данные для поиска: (или введите Enter если хотите пропустить какой-то параметр)')
        title = input('Название книги (регистром можно пренебречь)\n')
        author = input('Автора книги (регистром можно пренебречь)\n')
        year = input('Год издания книги\n')
        title = title.strip().upper()
        author = author.strip().lower().capitalize()
        year = year.strip().lower()
    try:
        if title:
                res_tmp = list()
                for value in hash_table_title[hash(title)][title]:
                    res_tmp.append(value)
                if res_tmp:
                    result = set(res_tmp)
                result = result
        if author:
                res_tmp = list()
                for value in hash_table_author[hash(author)][author]:
                    res_tmp.append(value)
                if res_tmp:
                    if not result:
                        result = set(res_tmp)
                    else:
                        result &= set(res_tmp)
        if year:
                res_tmp = list()
                for value in hash_table_year[hash(year)][year]:
                    res_tmp.append(value)
                if res_tmp:
                    if not result:
                        result = set(res_tmp)
                    else:
                        result &= set(res_tmp)
    except KeyError:
        return 'Ничего не нашлось\n'
    if not result:
         return 'Ничего не нашлось\n'
    return result


'''
Функция замены статуса книги
Учитывается возможность пользовательского ввода других возможных вариантов id и status
Включена проверка status, чтобы не менять его, если о уже задан таким, как хочет пользователь
'''
def swap_status(data, spaces):
    print('Введите id книги, которой хотите изменить статус (или нажмите Enter для возврата в меню):\n')
    search_id = input()
    if not search_id:
        return 'Вы ничего не ввели, возврат в меню\n'
    try:
        search_id_int = int(search_id)
    except ValueError:
        return 'Книги с таким id нет в библиотеке'
    if search_id_int in range(len(data)) and search_id_int not in spaces:
        print('Введите новый  статус книги: "в наличии" для выданных или "выдана" для тех, которые в наличии '
              '(или нажмите Enter для возврата в меню):\n')
        new_status = input()
        if not new_status:
            return 'Вы ничего не ввели, возврат в меню\n'
        new_status = new_status.strip().lower()
        if new_status not in ('в наличии', 'выдана'):
            return 'Такой статус нельзя установить\n'
        if data[search_id_int]['status'] == new_status:
            return f'У этой книги уже статус "{new_status}"\n'
        data[search_id_int]['status'] = new_status
        return f'Статус книги "{data[search_id_int]['title']}" поменян на "{new_status}"'
    return 'Книги с таким id нет в библиотеке\n'

'''
Функция main(), описывающая весь функционал приложения и вызывающаяся в начале работы программы
В зависимости от опции ,которую выбрал пользователь в меню функция проводит нужные действия
Также есть опция выхода для завершения работы программы
Стоит обратить внимание, что авто сохранение не предусмотренно, 
так что нужно обязательно сохранить данные перед выходом
'''
def main():
    spaces = get_data(file_name='spaces.json')
    data = get_data(file_name='books_database.json')
    while True:
        option = menu()
        if option == '1':
            if not data:
                print('В библиотеке пока что нет книг\n')
            else:
                print(show_data(data))
        if option == '2':
            add_data(data=data, spaces=spaces)
        if option == '3':
            save_data(data=data,                file_name='books_database.json' )
            save_data(data=spaces,              file_name='spaces.json')
            save_data(data=hash_table_title,    file_name='hash_table_title.json')
            save_data(data=hash_table_author,   file_name='hash_table_author.json')
            save_data(data=hash_table_year,     file_name='hash_table_year.json')
            print('Изменения сохранены!\n')
        if option == '4':
            print('Результаты поиска: ', show_data(data, positions = search_data()))
        if option == '5':
            del_data(data=data, spaces=spaces)
        if option == '6':
            print(swap_status(data=data, spaces=spaces))
        if option == '7':
            break

'''
Точка входа в программу
'''
if __name__ == '__main__':
    main()
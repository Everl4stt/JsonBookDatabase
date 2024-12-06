import json
import os


file_name = 'books_database.json'


def menu():
    while True:
        print('Вы в главном меню библиотеки, выберите опцию из перечисленных\n'
        'Для того, чтобы выбрать опцию введите в консоль её номер из списка:\n'
              '\t1. Просмотр списка книг \n'
              '\t2. Добавление книги в библиотеку \n'
              '\t3. Сохранить изменения \n'
              '\t4. Найти книгу в библиотеке \n'
              '\t5. Удаление книги из библиотеки\n'
              '\t6. Выход\n')
        option = input()
        if option not in ('1', '2', '3', '4', '5', '6'):
            print(f'Варианта {option} нет в списке, попробуйте выбрать из списка\n')
        else:
            break
    return option

def get_hash_data(hash_file_name):
    if not os.path.exists(hash_file_name):
        with open(hash_file_name, 'w', encoding = 'utf-8') as f:
            json.dump([{} for _ in range(65536)], f, ensure_ascii = False, indent = 4)
    with open(hash_file_name, 'r', encoding = 'utf-8') as f:
        return json.load(f)


hash_table_title = get_hash_data('hash_table_title.json')
hash_table_author = get_hash_data('hash_table_author.json')
hash_table_year = get_hash_data('hash_table_year.json')

def save_hash_table(data, hash_table):
    with open(hash_table, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_spaces():
    if not os.path.exists('spaces.json'):
        with open('spaces.json', 'w', encoding = 'utf-8') as f:
            json.dump([], f, ensure_ascii = False, indent = 4)
    with open('spaces.json', 'r', encoding = 'utf-8') as f:
        return json.load(f)

def get_data():
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding = 'utf-8') as f:
            json.dump([], f, ensure_ascii = False, indent = 4 )
    with open(file_name, 'r', encoding = 'utf-8') as f:
        return json.load(f)

def save_spaces(spaces):
    with open('spaces.json', 'w', encoding = 'utf-8') as f:
        json.dump(spaces, f, ensure_ascii = False, indent = 4)

def save_data(data, spaces):
    with open(file_name, 'w', encoding = 'utf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)
    save_spaces(spaces)
    save_hash_table(data = hash_table_title, hash_table = 'hash_table_title.json')
    save_hash_table(data = hash_table_author, hash_table = 'hash_table_author.json')
    save_hash_table(data = hash_table_year, hash_table = 'hash_table_year.json')
    print('Изменения сохранены!\n')

def add_data(data, spaces):
    position = 0
    title = input('Введите название книги: (или нажмите Enter для возврата в меню) ')
    if not title:
        print('Вы ничего не ввели, возврат в меню')
        return
    author = input('Введите автора книги (или нажмите Enter для возврата в меню): ')
    if not author:
        print('Вы ничего не ввели, возврат в меню')
        return
    if isdatavalid(title = title, author = author) or not data:
        year = input('Введите год издания книги (или нажмите Enter для возврата в меню): ')
        if not year:
            print('Вы ничего не ввели, возврат в меню')
            return
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
        hash_table_add(hash_table = hash_table_title, key = title, value = position)
        hash_table_add(hash_table = hash_table_author, key = author, value = position)
        hash_table_add(hash_table = hash_table_year, key = year, value = position)
    return data, spaces

def hash_table_add(hash_table, key, value):
    if key in hash_table[hash(key)]:
        hash_table[hash(key)][key].append(value)
    else:
        hash_table[hash(key)][key] = [value]

def isdatavalid(title, author):
        if search_data(title = title, author = author) == 'Ничего не нашлось\n':
            return True
        print('Такая книга этого автора уже есть в библиотеке\n')
        return False

def show_data(data, positions = None):
    result = ''
    if positions == 'Ничего не нашлось\n':
        return
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

def del_data(data, spaces):
    search_id = input('Введите id книги, которую хотите удалить (или нажмите Enter для возврата в меню)\n')
    if not search_id:
        print('Вы ничего не ввели, возврат в меню')
        return
    try:
        search_id_int = int(search_id)
    except ValueError:
        print('Книги с таким id нет в библиотеке')
        return
    if search_id_int in range(len(data)) and search_id_int not in spaces:
        print(f'Книга "{data[search_id_int]['title']}" c id: {search_id_int}  удалена из библиотеки')
        hash_table_del(hash_table = hash_table_title,   key = data[search_id_int]['title'],   value = search_id_int)
        hash_table_del(hash_table = hash_table_author,  key = data[search_id_int]['author'],  value = search_id_int)
        hash_table_del(hash_table = hash_table_year,    key = data[search_id_int]['year'],    value = search_id_int)
        data[search_id_int] = None
        spaces.append(search_id_int)
    else:
        print('Книги с таким id нет в библиотеке')
    return data, spaces

def hash_table_del(hash_table, key, value):
    hash_table[hash(key)][key].remove(value)

def hash(string):
    hash = 0x811c9dc5
    for char in string:
        hash ^= ord(char)
        hash *= 0x01000193
    return hash % 65536

def search_data(title = None, author = None, year = None):
    result = set()
    if not title:
        print('Введите данные для поиска: (или введите Enter если хотите пропустить какой-то параметр)')
        title = input('Название книги (регистром можно пренебречь)\n')
        author = input('Автора книги (регистром можно пренебречь)\n')
        year = input('Год издания книги\n')
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

def main():
    spaces = get_spaces()
    data = get_data()
    while True:
        option = menu()
        if option == '1':
            if not data:
                print('В библиотеке пока что нет книг\n')
            else:
                print(show_data(data))
        if option == '2':
            add_data(data = data, spaces = spaces)
        if option == '3':
            save_data(data = data, spaces = spaces)
        if option == '4':
            print('Результаты поиска: ', show_data(data, positions = search_data(data)))
        if option == '5':
            del_data(data = data, spaces = spaces)
        if option == '6':
            break


if __name__ == '__main__':
    main()


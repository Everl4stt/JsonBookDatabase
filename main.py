import json


def menu():
    while True:
        print('Вы в главном меню библиотеки, выберите опцию из перечисленных\n'
        'Для того, чтобы выбрать опцию введите в консоль её номер из списка')
        option = input('''
        1. Просмотр списка книг
        2. Добавление книги в библиотеку
        3. Удаление книги из библиотеки
        4. Найти книгу в библиотеке
        ''')
        if option not in ('1', '2', '3', '4'):
            print(f'Варианта {option} нет в списке, попробуйте выбрать из списка')
        else:
            break
    return option

def booklist():
    with open('booklist.json', 'r', encoding = 'utf-8') as f:
        booklist = json.load(f)
        if booklist == '':
            return 'В библиотеке пока что нет книг'
    return booklist

if __name__ == '__main__':
    option = menu()
    if option == '1':
        print(booklist())


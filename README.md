# Онлайн Библиотека

Это приложение для управления коллекцией книг в библиотеке. Оно позволяет добавлять, удалять, искать книги, а также изменять их статус. Программа хранит данные в JSON-файлах и использует хеш-таблицы для ускорения поиска.

## Особенности

- **Добавление книг**: Ввод информации о книге (название, автор, год издания) с автоматической проверкой на уникальность.
- **Удаление книг**: Удаление книги по её идентификатору (ID) с освобождением места для новых записей.
- **Поиск книг**: Быстрый поиск по названию, автору или году издания благодаря хеш-таблицам.
- **Изменение статуса книг**: Переключение между статусами "в наличии" и "выдана".
- **Сохранение изменений**: Обеспечивается сохранение данных в локальных JSON-файлах.
- **Управление через консоль**: Интуитивно понятный текстовый интерфейс.

## Установка

1. Скачайте или клонируйте репозиторий:
   ```bash
   git clone <URL репозитория>
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd online-library
   ```
3. Убедитесь, что установлен Python версии 3.7 или выше.

## Использование

1. Запустите программу:
   ```bash
   python main.py
   ```
2. В главном меню выберите необходимую опцию, введя её номер:
   - **1**: Просмотр списка книг.
   - **2**: Добавление новой книги.
   - **3**: Сохранение изменений.
   - **4**: Поиск книги.
   - **5**: Удаление книги.
   - **6**: Изменение статуса книги.
   - **7**: Выход.

## Пример работы

### Добавление книги
```plaintext
Введите название книги: Гарри Поттер
Введите автора книги: Дж. К. Роулинг
Введите год издания книги: 1997
Новая книга "ГАРРИ ПОТТЕР" добавлена в библиотеку!
```

### Поиск книги
```plaintext
Введите данные для поиска:
Название книги: Гарри Поттер
Результаты поиска:
0: ГАРРИ ПОТТЕР, Дж. К. Роулинг, 1997 год, в наличии
```

## Файлы для хранения информации

- **books_database.json**: Хранит информацию о книгах.
- **hash_table_title.json, hash_table_author.json, hash_table_year.json**: Хеш-таблицы для быстрого поиска.
- **spaces.json**: Хранит освобождённые ID для эффективного повторного использования.

## Технологии

- **Язык**: Python 3
- **Хранение данных**: JSON
- **Алгоритмы**: Хеш-таблицы, обработка коллизий.

---

# Преимущества и производительность этого консольного приложения
## Введение

Разработанное приложение консольной библиотеки обладает рядом особенностей, которые значительно повышают его производительность и удобство использования. Основное преимущество программы заключается в применении хеш-таблиц для организации данных, а также в эффективном управлении освобожденными идентификаторами записей. Это делает приложение быстрым, масштабируемым и устойчивым к росту объема данных.

---


## Управление освобожденными идентификаторами

### Проблема удаления записей

При удалении записей из базы данных возникает необходимость:
- Сохранять непрерывность идентификаторов записей.
- Избегать сдвига оставшихся данных, что может быть затратным по времени.

### Решение

Приложение использует список освобожденных идентификаторов (“spaces”):
- Удаленные записи помечаются как “None”, и их идентификаторы добавляются в список.
- При добавлении новой книги используется первый доступный идентификатор из списка.

### Преимущества подхода:

1. **Экономия ресурсов:** Отсутствие необходимости сдвигать массив данных при удалении записи.
2. **Стабильность идентификаторов:** Все записи сохраняют уникальные и постоянные идентификаторы.
3. **Ускорение вставки:** Повторное использование освобожденных идентификаторов ускоряет процесс добавления новых записей.

---

## Сравнение с линейным поиском

### Линейный поиск

Линейный поиск предполагает последовательное перебирание всех записей до нахождения нужной. Это приводит к временной сложности **O(n)**, что становится проблемой для больших объемов данных.

### Поиск с использованием хеш-таблиц

1. **Скорость:** Хеш-таблицы находят данные за **O(1)** в среднем случае.
2. **Поиск по нескольким параметрам:** Программа поддерживает пересечение результатов из нескольких хеш-таблиц для поиска по нескольким критериям (например, автору и году).
3. **Сложность:** Даже при худшем сценарии временная сложность хеш-таблиц остается значительно ниже, чем у линейного поиска.

---
## Особенность хранения данных
В этом консольном приложении к качестве уникального ID для каждой записи используется не конкретное поле в записи, а ее порядковый номер в хранимом массиве словарей.
Этот подход позволяет избежать возможного дублирования ID для некоторых записей и облегчает поиск по ID для функций. Также, это позволяет 
не использовать сложных функций для генерации уникального ID, что облегчает запись в базу.






# Получение статистики вакансий с headhunter и superjob для Москвы

### Как установить

1. Зарегестрироваться на `https://api.superjob.ru/`
2. Создайте пустой `.env` файл в корне с исполнительными файлами. 
3. Поместите значение `Secret key` в `.env` файл, в переменную 
```bash
SJ_API_ID="Ваш ключ"
```
4. Для того, чтобы задать необходимые профессии, необходимо в функциях `predict_vacancy_hh` и `predict_vacancy_sj` изменить содержимое списка `vacancies` на необходимые профессии, пример:
```python
vacancies = ["Python", "JavaScript", "Ruby", "Java", "PHP", "C++", "Go", "Swift"]
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Запуск скрипта:

```bash
python3 main.py
```

Сайт headhunter разрешает смотреть до 2000 вакансий одновременно. Зарплата считается по 2000 вакансиям.

### Пример успешного запуска
```
+Head Hunter Moscow-----+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Swift                 | 1177             | 285                 | 201401           |
| Go                    | 2917             | 957                 | 104671           |
| C++                   | 3951             | 675                 | 148790           |
| PHP                   | 4603             | 944                 | 140819           |
| Java                  | 6868             | 306                 | 205747           |
| Ruby                  | 548              | 108                 | 165013           |
| JavaScript            | 9294             | 749                 | 159265           |
| Python                | 9248             | 578                 | 167872           |
+-----------------------+------------------+---------------------+------------------+
+Super job Moscow-------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Swift                 | 7                | 5                   | 153600           |
| Go                    | 17               | 11                  | 96018            |
| C++                   | 41               | 27                  | 142400           |
| PHP                   | 49               | 40                  | 138590           |
| Java                  | 31               | 21                  | 159809           |
| Ruby                  | 6                | 4                   | 233500           |
| JavaScript            | 66               | 49                  | 116489           |
| Python                | 78               | 52                  | 128861           |
+-----------------------+------------------+---------------------+------------------+
```




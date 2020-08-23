## Сравнение модулей
### tabula-py 1.4.1
* [oписание и документация](https://tabula-py.readthedocs.io/en/latest/)
* проблемы:
    * первая строка распознается как заголовок
    * объединение нескольких колонок в одну
    * не распознается продолжение таблицы на след. стр.
    * в таблицу вставляются колонки с пустыми значениями
### camelot-py 0.8.2
* [описание и документация](https://camelot-py.readthedocs.io/en/master/)
* проблемы:
    * распознает как строки таблицы весть текст документа
    * не выделяет колонки
    * новую стр. в документе относит кновойтаблиуе (не распознает продолжение)
### PDFLayoutTextStripper (рекомендуется в [описании](task_description/PDF Invoice Parsing.docx) задания)
* [описание и документация](https://github.com/JonathanLink/PDFLayoutTextStripper) (java class for Apache PDFBox)
* [python API](https://github.com/thoqbk/PDFLayoutTextStripper)
* [py4j](https://www.py4j.org/py4j_java_gateway.html#examples) (java to python)
* проблемы:
    * ошибка на файле [PO#_077-2706402.pdf(sysco PO#_077-2706402.pdf)](task_description/examples/PO#_077-2706402.pdf):
    ```python
    {'success': 'false', 'error': 'String index out of range: -1'}
    ```

## TODO
1. Предусмотреть обработку ошибки ```{'success': 'false', 'error': 'String index out of range: -1'}```
2.
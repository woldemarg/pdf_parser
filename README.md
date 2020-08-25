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
### PDFLayoutTextStripper 2.2.3 (рекомендуется в [описании](task_description/PDF%20Invoice%20Parsing.docx) задания)
* [описание и документация](https://github.com/JonathanLink/PDFLayoutTextStripper) (java class for Apache PDFBox)
* [python API](https://github.com/thoqbk/PDFLayoutTextStripper) / [py4j](https://www.py4j.org/py4j_java_gateway.html#examples) (java to python)
* проблемы:
    * ошибка на файле [sysco PO#_077-2706402.pdf](task_description/examples/sysco%20PO#_077-2706402.pdf):
    ```python
    {'success': 'false', 'error': 'String index out of range: -1'}
    ```
### pdftotext 2.1.5 (рекомендуется в [описании](task_description/PDF%20Invoice%20Parsing.docx) задания)
* [описание и документация](https://github.com/jalan/pdftotext)
* проблемы:
    * однострочные заголовки таблиц могут дробиться на несколько рядов
### Резюме:
* примеры работы модулей- см. [ноутбук](scripts/notebooks/compare_modules.ipynb)
* все модули требуют значительной дополнительной работы с текстом
* *camelot*, *pdflayouttextstripper*, *pdftotext* сохраняют максимум входной информации (два последних - в т.ч. и layout документа). Но:
    * *camelot* работает значительно дольше *pdftotext*
    * *pdflayouttextstripper* не принимает некоторые документы
    * *pdftotext* склонен дробить одну строку текста (с подчеркиванием) на несколько блоков (отельных строк)
* с помощью *pdftotext* и *camelot* можно добиться схожих результатов, будем продолжать работу с этими модулями

## TODO
1. ~~Решить вопрос с ошибкой ```{'success': 'false', 'error': 'String index out of range: -1'}``` в *PDFLayoutTextStripper*~~
    * 23.08.2020 - все файлы типа *sysco PO#_077-2706402.pdf* имеют bookmarks. Удалил закладки через [avepdf.com](https://avepdf.com/en/remove-pdf-content) + при удалении обновляется версия pdf c 1.0 до 1.5. Изм. файл [sysco PO#_077-2706402_no_bmrks.pdf](task_description/examples/no_bookmarks/sysco%20PO#_077-2706402_no_bmrks.pdf) дает ту же ошибку.
    * 24.08.2020 - отказ от работы с модулем *pdflayouttextstripper* в пользу других модулей
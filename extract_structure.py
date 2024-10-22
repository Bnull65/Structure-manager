import fitz
import json


def get_toc(pdf_file):
    doc = fitz.open(pdf_file)
    toc = doc.get_toc()

    if not toc:  # Проверяем, есть ли оглавление
        print("Оглавление не найдено")
        return None

    result = {}
    for item in toc:  # Проходим по каждому пункту оглавления
        level, title, page = item

        if level == 1:  # Если это глава
            chapter = title
            result[chapter] = {}
        elif level == 2:  # Если это раздел
            section = title
            result[chapter][section] = []
        elif level == 3:  # Если это подраздел
            result[chapter][section].append(title)

    return result


def save_to_json(data, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


pdf_file = r"C:\Users\toshk\OneDrive\Рабочий стол\Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf"
json_file = r"C:\Users\toshk\OneDrive\Рабочий стол\structure.json"
toc_data = get_toc(pdf_file)

if toc_data:  # Если найдена
    save_to_json(toc_data, json_file)
    print("Структура сохранена в structure.json")
else:  # Если не найдена
    print("Не удалось получить структуру")

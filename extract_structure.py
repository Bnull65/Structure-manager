import fitz
import re
import json
import os

def get_toc(pdf):
    try:
        doc = fitz.open(pdf)
    except Exception as e:
        print(f"Ошибка открытия PDF: {e}")
        return None

    toc = {}
    cur_chap = None
    cur_sec = None

    # Регулярные выражения
    chap_pat = re.compile(r'Глава\s*(\d+)(?:[:\-–.]?\s*)?$')
    sec_pat = re.compile(r'(\d+\.\d+)\s+(.*)')
    subsec_pat = re.compile(r'(\d+\.\d+\.\d+)\s+(.*)')
    num_pat = re.compile(r'^\d+\s*$')
    title_pat = re.compile(r'^(.*?)(?:\.\s*|$)')

    for pg_num in range(doc.page_count):
        lines = doc[pg_num].get_text("text").split('\n')

        for i, line in enumerate(lines):
            line = line.strip()

            # Обработка глав
            chap_match = chap_pat.match(line)
            if chap_match:
                chap_num = chap_match.group(1)
                title = ""
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if num_pat.match(next_line):
                        j += 1
                        continue
                    title_match = title_pat.match(next_line)
                    if title_match:
                        title = title_match.group(1).strip()
                    break
                title = re.sub(r'\d+', '', title).strip()

                toc[chap_num] = {"title": title, "sections": {}}
                cur_chap = chap_num
                cur_sec = None
                continue

            # Обработка разделов
            sec_match = sec_pat.match(line)
            if sec_match and cur_chap:
                sec_num, title = sec_match.groups()
                if sec_num.split('.')[0] == cur_chap:
                    title = re.sub(r'\d+', '', title).strip().split('.')[0]
                    toc[cur_chap]["sections"][sec_num] = {
                        "title": title.strip(),
                        "subsections": {}
                    }
                    cur_sec = sec_num
                continue

            # Обработка подразделов
            subsec_match = subsec_pat.match(line)
            if subsec_match and cur_chap and cur_sec:
                subsec_num, title = subsec_match.groups()
                title = re.sub(r'\d+', '', title).strip().split('.')[0]
                toc[cur_chap]["sections"][cur_sec]["subsections"][subsec_num] = {
                    "title": title.strip()
                }

    return toc

def show_toc(toc):
    if not toc:
        print("Оглавление не найдено.")
    else:
        print(json.dumps(toc, ensure_ascii=False, indent=4))

def save_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Сохранено в {json_path}")

# Пути к файлам
pdf_path = r"C:\Users\toshk\OneDrive\Рабочий стол\Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf"
json_path = r"C:\Users\toshk\OneDrive\Рабочий стол\extracted_structure.json"

if os.path.exists(pdf_path):
    toc_data = get_toc(pdf_path)
    if toc_data:
        show_toc(toc_data)
        save_json(toc_data, json_path)
    else:
        print("Не удалось получить структуру")
else:
    print("Файл PDF не найден.")

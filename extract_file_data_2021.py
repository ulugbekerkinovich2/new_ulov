import pandas as pd
import sqlite3
import re
from datetime import datetime


def clean_product_name(product_name):
    # Remove unwanted characters from the product name using regular expressions
    return re.sub(r'[\"\'\[\]/,()!?:;«»–]', '', product_name).lower()


def extract_file_data_2021(file_name, file_id):
    current_time = datetime.now()
    file_id_ = int(file_id)
    print(file_name, '2021')
    df = pd.read_excel(file_name, sheet_name=1)
    data = df.values
    k = 0
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT model_name, mark_name FROM model1 INNER JOIN mark ON model1.mark_id = mark.id")
    models = cursor.fetchall()
    for i in range(3, len(data)):
        product_name = ' '.join(str(data[i][8]).lower().split('\n')).split(' ')
        product_name = clean_product_name(str(product_name))
        accreditation_date = str(data[i][4]).split(' ')[0].replace('-', '.')

        for model_info in models:
            model_name = model_info[0]
            mark_name = model_info[1]
            if model_name.isdigit():
                continue

            if f" {model_name.lower()} " in product_name and len(model_name) > 3:
                print(accreditation_date, '------------------->Accreditation date')
                print(model_name, '-------------->', mark_name, '\n')
                print(product_name, '\n\t')
                print('\t\t', k, "\033[36m" + model_name.lower() + "\033[0m\n" + 'topildi\n')

                # Update the date format to match the Excel date string format
                date_format = "%Y.%m.%d"
                date_obj = datetime.strptime(accreditation_date, date_format)
                formatted_date = date_obj.strftime("%Y-%m-%d")
                print(formatted_date)

                k += 1
                sql = """
                    INSERT INTO data21 (sana, model_id, mark_id,file_id_id,time)
                    VALUES (?, (SELECT id FROM model1 WHERE model_name = ?),
                            (SELECT id FROM mark WHERE mark_name = ?), ?,?)
                """
                cursor.execute(sql, (formatted_date, model_name, mark_name, file_id_, current_time))
    conn.commit()
    cursor.close()
    conn.close()
    print('done')

# Example usage:
# extract_file_data_2021('D:\Telegram_New\Там. база 2021г.(1).xls', 123)  # Replace 123 with the actual file_id value

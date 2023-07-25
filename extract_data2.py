import pandas as pd
import re
from datetime import datetime
import sqlite3


def clean_product_name(product_name):
    # Remove unwanted characters from the product name using regular expressions
    return re.sub(r'[\"\'\[\]/,()!?:;«»–]', '', product_name).lower()


def extract_file_data_2022(file_name, file_id):
    file_id_ = int(file_id)
    print(file_name)
    print('keldi 2022')
    df = pd.read_excel(file_name, sheet_name=0)
    data = df.values
    k = 0

    # Use pandas sqlite3.connect for connection pooling
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT model_name, mark_name FROM model1 INNER JOIN mark ON model1.mark_id = mark.id""")
        models = cursor.fetchall()

        for i in range(3, len(data)):
            product_name = ' '.join(str(data[i][7]).lower().split('\n')).split(' ')
            product_name = clean_product_name(str(product_name)).lower()
            measure = data[i][8]
            country = data[i][13]
            sana = str(data[i][1]).split('/')[1].replace('-', '.')
            date_format = "%d.%m.%Y"
            if measure != 'Количество штук':
                continue

            for model_info in models:
                model_name = model_info[0]
                mark_name = model_info[1]
                if model_name.isdigit():
                    continue

                if f" {model_name.lower()} " in product_name and len(model_name) > 3:
                    print(sana, '------------------->Accreditation date')
                    print(country, '------------------->Mamlakat')
                    print(model_name, '-------------->', mark_name, '\n')
                    print(product_name, '\n')
                    print('\t\t', k, "\033[36m" + model_name.lower() + "\033[0m\n" + 'topildi\n')
                    date_obj = datetime.strptime(sana, date_format)
                    formatted_date = date_obj.date()
                    k += 1
                    sql = """
                        INSERT INTO data22 (sana, model_id, mark_id, file_id_id, country)
                        VALUES (?, (SELECT id FROM model1 WHERE model_name = ?),
                                (SELECT id FROM mark WHERE mark_name = ?), ?, ?)
                    """

                    # Execute the SQL query with data values
                    cursor.execute(sql, (formatted_date, model_name, mark_name, file_id_, country))

        # Commit the changes to the database
    conn.commit()

    cursor.close()
    print('done')

# Example usage:
# extract_file_data_2022(r'D:\Downloads\Там._база_2022_г.3_2.xls', 123)  # Replace 123 with the actual file_id value

import pandas as pd
import re
from datetime import datetime
import sqlite3



def clean_product_name(product_name):
    # Remove unwanted characters from the product name using regular expressions
    return re.sub(r'[\"\'\[\]/,()!?:;«»–]', '', product_name).lower()


def extract_file_data_2022(file_name, file_id):
    from basic_app.models import DATA22, Model1, Mark
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
            # print(data[i][1])
            sana = str(data[i][1]).split('/')[1].replace('.', '.')
            # try:
            #     sana = str(data[i][1]).split('/')[1].replace('.', '.')
            # except:
            #     print(sana)
            #     print('sana topilmadi')
            # print(sana, '------------------->Accreditation date')
            if measure != 'Количество штук':
                continue

            for model_info in models:
                model_name = model_info[0]
                mark_name = model_info[1]
                if model_name.isdigit():
                    continue

                if f" {model_name.lower()} " in product_name and len(model_name) > 3:

                    print(country, '------------------->Mamlakat')
                    print(model_name, '-------------->', mark_name, '\n')
                    print(product_name, '\n')
                    print('\t\t', k, "\033[36m" + model_name.lower() + "\033[0m\n" + 'topildi\n')
                    date_obj = datetime.strptime(sana, "%d.%m.%Y").date()
                    print(date_obj, '------------------->Accreditation date')
                    k += 1
                    try:
                        model_instance = Model1.objects.filter(model_name=model_name).first()
                        mark_instance = Mark.objects.filter(mark_name=mark_name).first()
                        if model_instance and mark_instance:
                            data22_instance = DATA22.objects.create(
                                time=datetime.now(),
                                file_id_id=file_id_,
                                sana=date_obj,
                                model=model_instance,
                                mark=mark_instance,
                                country=country
                            )
                            data22_instance.save()
                        else:
                            print('Model1 or Mark instance not found.')
                    except Exception as e:
                        print('Error:', str(e))
                        continue
                    # serializer = Data22serializer(data={
                    #     'sana': formatted_date,
                    #     'model_id': model_name,
                    #     'mark_id': mark_name,
                    #     'file_id_id': file_id_,
                    #     'country': country,
                    #     'time': datetime.now()
                    # })

                    # if serializer.is_valid():
                    #     serializer.save()
                    # else:
                    #     print(serializer.errors)
                    #     print('not saved')
                    #     continue

    cursor.close()
    return {'status': 'ok'}

# Example usage:
# extract_file_data_2022(r'D:\Downloads\Там._база_2022_г.3_2.xls', 123)  # Replace 123 with the actual file_id value

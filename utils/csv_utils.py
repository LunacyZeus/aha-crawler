import csv

from loguru import logger


def write_new_csv_file(filename, data_list):  # 写入到csv文件
    # CSV 表头
    headers = ['ahaId', 'resultType', 'orgDisplayName', 'personDisplayName', 'title', 'ahaMember']

    # 写入 CSV 文件
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # 写入表头
        writer.writerows(data_list)  # 写入数据行

def append_csv_file(filename, data_list):  # 追加到csv文件
    # 追加写入 CSV 文件
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['ahaId', 'resultType', 'orgDisplayName', 'personDisplayName', 'title',
                                                  'ahaMember'])
        writer.writerows(data_list)  # 直接写入数据行（不再写入表头）
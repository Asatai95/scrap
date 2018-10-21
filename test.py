

import csv

def test():

    header = ['ID', 'name'],

    body = [
    [0, 'Alex'],
    [1, 'John'],
    [2, 'Bob']
    ]
    with open('sample_test.csv', 'w') as f:
        writer = csv.writer(f)  # writerオブジェクトを作成
        writer.writerow(header) # ヘッダーを書き込む
        writer.writerows(body)  # 内容を書き込む

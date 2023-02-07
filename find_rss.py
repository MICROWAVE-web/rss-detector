import csv
import json
from first import findfeed
from second import find_feeds

rss_result_file = 'rss_result.json'


def append_data(new_data: dict):
    with open(rss_result_file, encoding='utf8') as f:
        data = json.load(f)
    data.append(new_data)
    with open(rss_result_file, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


methods = [
    findfeed,
    find_feeds,
]


def main():
    with open('result.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for index, row in enumerate(spamreader):
            if index == 0:
                continue
            print(index)
            output_rss = set()
            output_rss.add((row[2], False))
            for ind, m in enumerate(methods):
                try:
                    ress = list(m(row[1]))
                    for rss_url in ress:
                        output_rss.add((rss_url, True))
                except Exception as e:
                    print(f'Ошибка (метод №{ind}): {e}')
            if output_rss:
                context = {
                    "title": row[0],
                    "issn": row[3].split(', '),
                    "publisher": row[4],
                    "subjects": row[5].split(';'),
                    "url": row[1],
                    "rss": [
                        {
                            "url": rssurl,
                            "status": status
                        } for rssurl, status in output_rss
                    ]
                }
                try:
                    append_data(context)
                except Exception as e:
                    print(f'Ошибка записи {row[0]}')


if __name__ == '__main__':
    # if not os.path.exists(rss_result_file):
    #     open(rss_result_file, 'w', newline='', encoding='utf-8')
    with open(rss_result_file, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    main()

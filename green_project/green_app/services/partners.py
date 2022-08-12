import csv


def int_or_zero(x: str) -> int:
    return int(x) if x else int()


def get_sponsors(csv_file_path: str) -> dict:
    """Получение наставников со списком их партнеров"""

    sponsors: dict[list] = dict()

    with open(csv_file_path, encoding='utf-8') as csvf:
        csvReader = csv.reader(csvf, skipinitialspace=True, delimiter=',')
        # пропускаем название колонок
        next(csvReader)
        # читаем файл и формируем словарь
        for row in csvReader:
            partner_id, sponsor = map(int_or_zero, row)
            if partner_id:
                if sponsor:
                    if sponsor in sponsors:
                        sponsors[sponsor].append(partner_id)
                    else:
                        sponsors[sponsor] = [partner_id]

                if partner_id not in sponsors:
                    sponsors[partner_id] = []
    return sponsors

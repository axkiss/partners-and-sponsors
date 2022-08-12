import pandas as pd


def sum_partners_volumes_form_orders(csv_file_path: str, state_list: list) -> dict:
    """Подсчет объемов собственных продаж партнера"""

    partners_volumes: dict[dict] = dict()

    df_orders = pd.read_csv(csv_file_path)
    if state_list:
        df_orders = df_orders.loc[df_orders['STATE'].isin(state_list)]
    df_partners_vol = df_orders.groupby('RECIPIENT', as_index=False)['item_vol'].sum()
    for partner_id, vol in zip(df_partners_vol['RECIPIENT'], df_partners_vol['item_vol']):
        partners_volumes[partner_id] = {'myself': vol, 'sponsorship': None}
    return partners_volumes


def calculate_volume(sponsor: int, sponsors: dict, partners_volumes: dict, include_last: bool) -> None:
    """Рекурсивный подсчет объема продаж всех партнеров наставника"""

    if sponsor in partners_volumes:
        if partners_volumes[sponsor]['sponsorship'] is None:
            partners_volumes[sponsor]['sponsorship'] = .0
            for partner in sponsors[sponsor]:
                if partner not in partners_volumes: continue
                if sponsors[partner]:
                    calculate_volume(partner, sponsors, partners_volumes, include_last)
                    partners_volumes[sponsor]['sponsorship'] += partners_volumes[partner]['sponsorship'] + \
                                                                partners_volumes[partner]['myself']
                elif include_last:
                    partners_volumes[sponsor]['sponsorship'] += partners_volumes[partner]['myself']


def calculate_sponsors_volume(sponsors: dict, partners_volumes: dict, include_last: bool = True) -> None:
    """Подсчет объема продаж каждого наставника"""

    for sponsor in sponsors:
        if sponsor in partners_volumes and partners_volumes[sponsor]['sponsorship'] is None:
            calculate_volume(sponsor, sponsors, partners_volumes, include_last)

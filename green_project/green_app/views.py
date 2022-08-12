import time

from django.shortcuts import render
from django.views.generic import View

from green_project.settings import ORDERS_PATH, PARTNERS_PATH

from .services.partners import get_sponsors
from .services.orders import sum_partners_volumes_form_orders, calculate_sponsors_volume


class Index(View):
    """Отображение результатов расчета"""
    template_name = 'green_app/index.html'

    def get(self, request):
        # получение состояний для отбора заказов
        state_list = []
        if request.GET.get('ok') == 'on':
            state_list.append('OK')
        if request.GET.get('condition') == 'on':
            state_list.append('CONDITION')
        if request.GET.get('process') == 'on':
            state_list.append('PROCESS')

        # выбор номера задания
        last = True
        if request.GET.get('task') == '1':
            last = True
        elif request.GET.get('task') == '2':
            last = False

        context = {}
        # подсчет времени выполнения задания
        if request.GET.get('task'):
            start = time.perf_counter()
            sponsors_dict = get_sponsors(PARTNERS_PATH)
            partners_time = time.perf_counter() - start

            start = time.perf_counter()
            partners_volumes_dict = sum_partners_volumes_form_orders(ORDERS_PATH, state_list)
            orders_time = time.perf_counter() - start

            start = time.perf_counter()
            calculate_sponsors_volume(sponsors_dict, partners_volumes_dict, include_last=last)
            calculate_volume_time = time.perf_counter() - start

            # Округление объемов
            for partner in partners_volumes_dict:
                partners_volumes_dict[partner]['myself'] = round(partners_volumes_dict[partner]['myself'], 2)
                if partners_volumes_dict[partner]['sponsorship'] is not None:
                    partners_volumes_dict[partner]['sponsorship'] = round(partners_volumes_dict[partner]['sponsorship'],
                                                                          2)

            context = {
                'partners_time': round(partners_time, 3),
                'orders_time': round(orders_time, 3),
                'calculate_volume_time': round(calculate_volume_time, 3),
                'final_time': round(orders_time + partners_time + calculate_volume_time, 3),
                'partners': partners_volumes_dict.items()
            }

        return render(request, self.template_name, context)

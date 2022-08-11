from django.shortcuts import render
from django.views.generic import View


class Index(View):
    template_name = 'green_app/index.html'
    paginate_by = 20

    def get(self, request):

        return render(request, self.template_name)
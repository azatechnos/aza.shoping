from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from item.models import Category


class DashBoardView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        print dir(category)
        context = {'category': category}
        return self.render_to_response(context)
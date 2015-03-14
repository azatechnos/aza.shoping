from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.generic import TemplateView


class DashBoardView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)
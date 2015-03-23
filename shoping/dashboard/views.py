from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView


class DashBoardView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)
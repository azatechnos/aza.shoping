from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from item.models import Category, Product


class DashBoardView(TemplateView):
    template_name = 'shop.html'

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        print dir(category)
        product = Product.objects.all()
        context = {'category': category, 'product': product}
        return self.render_to_response(context)
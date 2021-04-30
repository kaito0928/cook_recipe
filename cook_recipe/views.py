from django.shortcuts import render
from django.views import generic
from .models import Stock
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import StockCreateForm,SearchForm
from django.contrib import messages
import json
import requests

SEARCH_URL = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=1037313654723951125'

def get_api_data(params):
    api = requests.get(SEARCH_URL,params=params).text
    result = json.loads(api)
    items = result['items']
    return items


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class StockListView(LoginRequiredMixin,generic.ListView):
    model = Stock
    template_name = 'stock_list.html'

    def get_queryset(self):
        stocks = Stock.objects.filter(user=self.request.user).order_by('-update_at')
        return stocks

    def get(self,request,*args,**kwargs):
        form = SearchForm(request.POST or None)
        return render(request,'stock_list.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = SearchForm(request.POST or None)
        if form.is_valid():
            keyword = form.cleaned_data['product']
            params = {
                'product': keyword,
                'hits': 28
            }
            items = get_api_data(params)
            recipe_data = []
            for i in items:
                item = i['Item']
                product = item['product']
                image = item['image']
                isbn = item['isbn']
                query = {
                    'product': product,
                    'image': image,
                    'isbn': isbn
                }
                recipe_data.append(query)
            return render(request,'cook_recipe:recipe_list.html',{'recipe_data':recipe_data,'keyword':keyword})
        return render(request,'cook_recipe:stock_list.html',{'form':form})

class StockCreateView(LoginRequiredMixin,generic.CreateView):
    model = Stock
    template_name = 'stock_create.html'
    form_class = StockCreateForm
    success_url = reverse_lazy('cook_recipe:stock_list')

    def form_valid(self, form):
        stock = form.save(commit=False)
        stock.user = self.request.user
        stock.save()
        messages.success(self.request,'商品を追加しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'商品の追加に失敗しました。')
        return super().form_invalid(form)


class StockDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Stock
    template_name = 'stock_delete.html'
    success_url = reverse_lazy('cook_recipe:stock_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request,'商品を削除しました。')
        return super().delete(request,*args,**kwargs)
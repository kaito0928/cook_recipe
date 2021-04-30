from django.urls import path
from . import views

app_name = 'cook_recipe'
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('stock-list/',views.StockListView.as_view(),name='stock_list'),
    path('stock-create/', views.StockCreateView.as_view(), name='stock_create'),
    path('stock-delete/<int:pk>/', views.StockDeleteView.as_view(), name='stock_delete'),

]
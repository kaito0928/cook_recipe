from .models import Stock
from django import forms

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('product','maker','sell_by',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'


class SearchForm(forms.Form):
    product = forms.CharField(label='商品',max_length=50,required=True)
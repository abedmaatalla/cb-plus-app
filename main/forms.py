from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from main.models import Product, Stock


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('id', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('product', 'expired_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

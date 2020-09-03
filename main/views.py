from django.db.models import Max, Min, Subquery, OuterRef
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.timezone import now
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from django.views.generic import CreateView, UpdateView, ListView

from forms import ProductForm, StockForm
from main.models import Stock, Product
from main.serializer import StockSerializer, ProductSerializer


class StockExpirationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = StockSerializer
    filter_fields = ['product__id', 'expired_at']

    def get_object(self):
        pk_product = self.kwargs['pk']
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        try:
            obj = get_object_or_404(queryset, product__id=pk_product)
        except:
            obj = get_object_or_404(queryset, pk=pk_product)
        return obj

    def get_queryset(self):
        from django.db.models import F, ExpressionWrapper, fields
        duration = ExpressionWrapper(F('expired_at') - now(), output_field=fields.DurationField())
        return Stock.objects.annotate(duration=duration).filter(duration=Subquery(
            Stock.objects.filter(product=OuterRef('product')).filter(expired_at__gt=now()).annotate(duration=duration)
                .values('duration').annotate(duration_min=Min('duration')).values('duration_min')[:1]
        )).order_by('-expired_at')


class StockViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = StockSerializer
    filter_fields = ['product__id', 'expired_at']

    def get_object(self):
        pk_product = self.kwargs['pk']
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        try:
            obj = get_object_or_404(queryset, product__code=pk_product)
        except:
            obj = get_object_or_404(queryset, pk=pk_product)
        return obj

    def get_queryset(self):
        return Stock.objects.order_by('-expired_at')


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     GenericViewSet):
    serializer_class = ProductSerializer
    filter_fields = ['id', ]

    def get_queryset(self):
        return Product.objects.all()


class StockListView(ListView):
    model = Stock
    context_object_name = 'stocks'

    def get_queryset(self):
        product__id = self.request.GET.get('product__id', None)
        if product__id:
            return Stock.objects.filter(product__id=product__id)
        return Stock.objects.all()


class StockCreateView(CreateView):
    model = Stock
    fields = ('product', 'expired_at')


class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/stock_update_form.html'


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    fields = ('id', 'name')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update_form.html'


class StockReadingListView(ListView):
    model = Stock
    template_name = 'main/stock_reading.html'

    def get_queryset(self):
        from django.db.models import F, ExpressionWrapper, fields
        duration = ExpressionWrapper(F('expired_at') - now(), output_field=fields.DurationField())
        return Stock.objects.annotate(duration=duration).filter(duration=Subquery(
            Stock.objects.filter(product=OuterRef('product'))
                .filter(expired_at__gt=now()).annotate(duration=duration)
                .values('duration').annotate(duration_min=Min('duration')).values('duration_min')[:1]
        )).order_by('-expired_at')

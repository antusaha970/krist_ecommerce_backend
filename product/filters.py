from django_filters import rest_framework as filter
from .models import Product


class ProductFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filter.NumberFilter(field_name="price", lookup_expr="lte")
    keyword = filter.CharFilter(field_name="title", lookup_expr="icontains")
    categories = filter.CharFilter(
        field_name="categories__name", lookup_expr="iexact")
    colors = filter.CharFilter(
        field_name="colors__name", lookup_expr="iexact")
    sizes = filter.CharFilter(
        field_name="sizes__name", lookup_expr="iexact")
    ordering = filter.OrderingFilter(
        fields=(
            ('created_on', 'created_on'),
        ),
        field_labels={
            'created_on': 'Created On',
        },
        label="Order by"
    )

    class Meta:
        model = Product
        fields = ("rating", "created_on")

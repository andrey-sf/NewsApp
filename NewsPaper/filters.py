import django_filters
from django_filters import CharFilter, ModelChoiceFilter
from django import forms
from .models import Post, Author, Category


class PostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(
        field_name='created_at',
        label='Дата создания позже чем',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        input_formats=['%d-%m-%Y', '%d-%m', '%m', '%d', '%m-%Y', '%Y-%m-%d', '%Y-%m', '%m-%d', '%d.%m.%Y']
    )
    title = django_filters.CharFilter(field_name='title', label='Заголовок', lookup_expr='icontains')
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категории',
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['created_at', 'title', 'author', 'categories']

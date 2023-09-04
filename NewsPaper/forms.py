from django.forms import ModelForm
from .models import Post, Category
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'categories', 'title', 'text']
        widgets = {
            'author': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title post'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

    categories = forms.MultipleChoiceField(
        choices=[(category.id, category.name) for category in Category.objects.all()],
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

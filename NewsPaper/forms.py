from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если объект Post уже существует, установите начальное значение для поля categories
        if self.instance.pk:
            initial_categories = self.instance.categories.all()
            self.fields['categories'].queryset = Category.objects.all()
            self.fields['categories'].initial = initial_categories

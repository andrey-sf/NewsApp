from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    banned_words = ['хуй', 'пидор', 'иди на хуй']  # Список нежелательных слов
    for word in banned_words:
        value = value.replace(word, '***')
    return value

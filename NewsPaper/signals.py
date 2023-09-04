from django.utils import timezone

from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from NewsPaper.tasks import new_post_subscription
from .models import PostCategory, Post


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    author = instance.author
    posts_today = Post.objects.filter(author=author, created_at__date=
        timezone.now().date()).count()
    if posts_today >= 3:
        # На странице ошибки выводим заголовок и текст поста чтобы пользователь мог его сохранить.
        raise PermissionDenied('Превышен лимит на количество постов в день.<br>'
                               'Попробуйте опубликовать новый пост завтра или удалите '
                               'один из трех ваших последних постов<br><br>'
                               f'Вот заголовок и текст вашего поста:<br>Заголовок:'
                               f' {instance.title}<br>Текст:<br>{instance.text}')
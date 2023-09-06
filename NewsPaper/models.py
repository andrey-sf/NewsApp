from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f"{self.authorUser}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass

    def get_category(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=100, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Post #{self.pk} - Название: {self.title} - Автор: {self.author}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def email_preview(self):
        return f'{self.text[0:50]}...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categoryThrough}-----{self.postThrough}"


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

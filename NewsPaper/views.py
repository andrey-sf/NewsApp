from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, DeleteView, TemplateView
from .models import Post, Category, PostCategory, Author
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy, resolve


class PostsList(ListView):
    model = Post
    template_name = 'NewsPaper/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-created_at')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class SearchList(ListView):
    model = Post
    template_name = 'NewsPaper/search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-created_at')
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    template_name = 'NewsPaper/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class Posts(View):
    def get(self, request):
        posts = Post.objects.order_by('-created_at')
        p = Paginator(posts, 10)
        posts = p.get_page(request.GET.get('page', 1))
        data = {
            'posts': posts,
        }
        return render(request, 'NewsPaper/posts.html', data)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'NewsPaper/post_create.html'
    form_class = PostForm
    permission_required = ('NewsPaper.add_post')

    """def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Проверяем, есть ли объект Author для текущего пользователя
        author, created = Author.objects.get_or_create(authorUser=user)
        # Устанавливаем автора поста
        form.instance.author = author
        return super().form_valid(form)
"""


class PostDetail(DetailView):
    model = Post
    template_name = 'NewsPaper/post.html'
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'NewsPaper/post_create.html'
    form_class = PostForm
    permission_required = ('NewsPaper.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'NewsPaper/post_delete.html'
    permission_required = 'NewsPaper.delete_post'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:posts')


class PostCategoryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'NewsPaper/category.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(categories=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['subscribe'] = True
        else:
            context['subscribe'] = False
        context['category'] = category
        return context


@login_required
def subscribe_to_category(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user.id)
        email = user.email
        html_content = render_to_string (
            'mail/subscribed.html',
            {
                'categories': category,
                'user' : user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'{category} subscribe',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email,], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        try:
            msg.send() # отсылаем
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_to_category_view(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)
    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))

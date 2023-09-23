from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': 'Блог'}


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'created_date')
    success_url = reverse_lazy('blog:list')


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров статьи"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

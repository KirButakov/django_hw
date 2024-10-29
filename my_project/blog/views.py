from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from django.urls import reverse_lazy

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_post_list.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_post_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']

    def get_success_url(self):
        return reverse_lazy('blog_post_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_post_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']

    def get_success_url(self):
        return reverse_lazy('blog_post_detail', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_post_confirm_delete.html'
    success_url = reverse_lazy('blog_post_list')

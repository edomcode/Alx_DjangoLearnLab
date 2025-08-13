from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm
from django.urls import reverse_lazy, reverse

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' 
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']  
    template_name = 'blog/post_form.html'  
    success_url = reverse_lazy('blog-home')  

    class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
    paginate_by = 5

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        form.instance.post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been posted.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated.')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()

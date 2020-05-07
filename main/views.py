from django.shortcuts import render,redirect,get_object_or_404
from . models import Post,Comment,PostLike
from . forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import Account
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

def about(request):
    return render(request, 'about.html')

# class CommentListView(ListView):
#     model = Comment
#     template_name = 'comment_list.html'
#     context_object_name = 'comments'
#     ordering = ['-date']
#     paginate_by = 3
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset = Comment.objects.all()
        
#         if queryset:
#             context['comments'] = queryset.filter(Post['post.pk'])
            # return context
class UserPostListView(ListView):
    model = Post
    template_name = 'user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(Account, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# def user_post_list(request, pk):
#     user  = get_object_or_404(Account,pk=pk) 
#     posts = Post.objects.filter(author=user).order_by('-date_posted')
#     paginator = Paginator(posts, 2) # Show 25 contacts per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'user_post.html',{'page_obj': page_obj})

def comment_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(post=post).order_by('-date')
    paginator = Paginator(comment, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'comment_list.html',{'page_obj': page_obj})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('/',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'post_form.html',{'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('post-detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'post_form.html',{'form':form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('home')
    else: 
        return redirect("post-detail", pk=post.pk)
    
class PostDetailView(DetailView):
    template_name = 'post_detail.html'  # <app>/<model>_<viewtype>.html
    model = Post

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    num_of_likes = PostLike.objects.filter(user=request.user, post=post).count()
    if num_of_likes > 0:
        already_like = PostLike.objects.get(post=post,user=request.user).delete()
    else:
        already_like = PostLike.objects.create(post=post,user=request.user)
    return redirect("/",pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post= post
            comment.author = request.user
            comment.save()
            return redirect('/', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_edit(request, pk):                        
    comment = get_object_or_404(Comment, pk=pk)
    if request.method=="POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request,'comment_form.html',{'form':form})

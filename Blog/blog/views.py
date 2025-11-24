from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator
# Create your views here.

def post_list(request):
    posts = Post.Published.all()
    paginator = Paginator(posts, 3)
    post_page = request.GET.get('page' , 1)
    posts = paginator.page(post_page)
    return render(request, 'blog/post/list.html' ,{'posts' : posts})


def post_detail(request , id):
    post = get_object_or_404(Post , id=id , status = Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html' , {'post':post})
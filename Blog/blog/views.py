from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.

def post_list(request):
    posts = Post.Published.all()
    paginator = Paginator(posts, 3)
    post_page = request.GET.get('page' , 1)
    try:
        posts = paginator.page(post_page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html' ,{'posts' : posts})


def post_detail(request , id):
    post = get_object_or_404(Post , id=id , status = Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html' , {'post':post})
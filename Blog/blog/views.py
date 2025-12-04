from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from .forms import EmailPostForm , CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

def post_list(request , tag_slug=None):
    posts = Post.Published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag , slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    post_page = request.GET.get('page' , 1)
    try:
        posts = paginator.page(post_page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html' ,{'posts' : posts , 'tag':tag})


def post_detail(request , id):
    post = get_object_or_404(Post , id=id , status = Post.Status.PUBLISHED)
    # retrieve all comments on the post
    comments = post.comments.filter(active=True)
    # form for users to comment
    form = CommentForm()

    # List of similar posts
    # retrieve all tags id and restore them in list
    post_tags_ids = post.tags.values_list('id' , flat=True)
    # retrieve all posts with list of tags and exclude the post tag
    similar_posts = Post.Published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # set the limit of object to 3 objects with two atribuites
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags' , '-publish')
    
    return render(request, 'blog/post/detail.html' , {'post':post ,'comments':comments , 'form':form,'similar_posts':similar_posts})


def post_share(request , post_id):
    send = False
    post = get_object_or_404(Post , id = post_id , status = Post.Status.PUBLISHED)
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments : {cd['comments']}"
            send_mail(subject, message, 'rashedkhalil442001@gmail.com', [cd['to']],fail_silently=False)
            send = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html' , {'form':form , 'post':post , 'send':send})

@require_POST
def post_comment(request , post_id):
    post = get_object_or_404(Post , id = post_id , status = Post.Status.PUBLISHED)

    comment = None

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)

        comment.post = post

        comment.save()
    return render(request, 'blog/post/comment.html' , {'form':form , 'comment':comment , 'post':post})




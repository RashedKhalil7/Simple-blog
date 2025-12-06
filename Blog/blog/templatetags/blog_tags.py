from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.Published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=1):
    latest_posts = Post.Published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}
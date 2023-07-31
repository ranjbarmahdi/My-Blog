from django import template
from ..models import Post, Category
from django.db.models import Count
from random import sample

register = template.Library()


# =====================================<< Last Posts Tag >>=====================================
@register.simple_tag()
def last_posts(count=4):
    posts = Post.published.order_by('-publish')[:count]
    return posts


# =====================================<< Popular Tags Tag >>=====================================
@register.simple_tag()
def popular_tags(count=5):
    tags = Category.objects.annotate(posts_count=Count('posts')).order_by('-posts_count', 'name')[:count]
    return tags


# =====================================<< Related Posts >>=====================================
@register.simple_tag()
def related_posts(post: Post, count=4):
    posts = Post.published.filter(title__contains=post.title)
    for cat in post.category.all():
        posts |= cat.posts.all()
    posts = posts.distinct()
    return sample(list(posts), l if (l := len(posts)) < count else count)


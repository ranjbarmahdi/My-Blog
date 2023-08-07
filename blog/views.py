from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketForm, CommentForm, SearchForm, CreatePostForm
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity, SearchRank, SearchQuery, SearchVector


# =====================================<< Index View >>=====================================
def index(request):
    return render(request, 'blog/index.html', {})


# =====================================<< Post List View >>=====================================
def post_list(request, category=None):
    posts = Post.published.all()

    if category:
        posts = posts.filter(category__slug=category)

    print(category)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, 'blog/list.html', context)


# =====================================<< Post Detail View >>=====================================
def post_detail(request, id):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=id)
    comments = post.comments.filter(active=True)

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


# =====================================<< Post Search View >>=====================================
def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_query = SearchQuery(query)
            search_vector = SearchVector('title', 'description')
            search_rank = SearchRank(search_vector, search_query)
            results = Post.published.annotate(search=search_vector, rank=search_rank)\
                .filter(search=search_query).order_by('-rank')

            # results_1 = Post.published.annotate(similarity=TrigramSimilarity('title', query))\
            #     .filter(similarity__gte=0.1)
            # results_2 = Post.published.annotate(similarity=TrigramSimilarity('description', query))\
            #     .filter(similarity__gte=0.1)
            # results = (results_1 | results_2).order_by('-similarity')

    paginator = Paginator(results, 6)
    page_number = request.GET.get('page', 1)
    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        'query': query,
        'posts': results,
    }
    return render(request, 'blog/list.html', context)


# =====================================<< Profile View >>=====================================
def profile_posts(request):
    user = request.user
    posts = Post.published.filter(auther=user)
    context = {
        'posts': posts
    }

    return render(request, 'blog/profile-posts.html', context)


# =====================================<< Create Post View >>=====================================
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.auther = request.user
            post.save()

            if file := cd['image1']:
                Image.objects.create(post=post, image_file=file)

            if file := cd['image2']:
                Image.objects.create(post=post, image_file=file)
    else:
        form = CreatePostForm()

    return render(request, 'blog/create-post.html', {'form': form})


# =====================================<< Ticket View >>=====================================
def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
                message=cd['message']
            )
            # redirect('blog:post_list')
    else:
        form = TicketForm()
    context = {
        'form': form
    }
    return render(request, 'blog/contact-us.html', context)


# =====================================<< Comment View >>=====================================
@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post.id)

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)

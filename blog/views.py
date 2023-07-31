from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketForm


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
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


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
            redirect('blog:post_list')
    else:
        form = TicketForm()
    context = {
        'form': form
    }
    return render(request, 'blog/contact-us.html', context)

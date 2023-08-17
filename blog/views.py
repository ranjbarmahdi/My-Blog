import django.forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity, SearchRank, SearchQuery, SearchVector
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import password_validation, update_session_auth_hash


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


# =====================================<< Profile Posts View >>=====================================
def profile_posts(request):
    user = request.user
    posts = Post.objects.filter(auther=user)
    context = {
        'posts': posts
    }

    return render(request, 'blog/profile-posts.html', context)


# =====================================<< Edit Personal Detail View >>=====================================
def edit_personal_detail(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        account_from = AccountEditForm(request.POST, files=request.FILES, instance=request.user.account)
        print(user_form.is_valid(), account_from.is_valid())
        if user_form.is_valid() and account_from.is_valid():

            if request.FILES['image']:
                old_image = request.user.account.image
                storage, path = old_image.storage, old_image.path
                storage.delete(path)
                print(old_image)

            user_form.save(commit=True)
            account_from.save(commit=True)
            return redirect('blog:personal_detail')
    else:
        user_form = UserEditForm(instance=request.user)
        account_from = AccountEditForm(instance=request.user.account)

    return render(request, 'forms/edit_personal_detail.html', {})


# =====================================<< Logout View >>=====================================
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            password = cd['password']
            new_password = cd['new_password']
            confirm_password = cd['confirm_password']
            if user.check_password(password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                user.save()
                print("با موفقیت عوض شد")
            else:
                return HttpResponse("رمز فعلی را اشتباه وارد کردید.")
    else:
        form = ChangePasswordForm()

    return render(request, 'forms/change_password.html', {})


# =====================================<< Profile Personal Detail View >>=====================================
def personal_detail(request):
    return render(request, 'blog/profile-personal.html', {})


# =====================================<< Login View >>=====================================
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            username = User.objects.get(email=cd['email'].lower()).username
            print(username)
            user = authenticate(request, username=username, password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:profile_posts')
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse('User Not Found.(user or pass is wrong)')
    else:
        form = LoginForm()

    return render(request, 'forms/login.html', {'form': form})


# =====================================<< Logout View >>=====================================
def logout_user(request):
    logout(request)
    return redirect('blog:post_list')


# =====================================<< Login View >>=====================================
def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password'])
            user.save()
            Account.objects.create(user=user)

            return redirect('blog:login')
    else:
        form = RegisterForm(request.POST)

    return render(request, 'forms/register.html', {'form': form})


# =====================================<< Create Post View >>=====================================
def create_post(request):
    categories = Category.objects.all()

    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            # print(cd)

            post = form.save(commit=False)
            post.auther = request.user
            post.category = Category.objects.get(name=cd['category'])
            post.save()

            if file := cd['image1']:
                Image.objects.create(post=post, image_file=file)

            if file := cd['image2']:
                Image.objects.create(post=post, image_file=file)

    else:
        form = CreatePostForm()

    return render(request, 'blog/create-post.html', {'form': form, 'categories': categories})


# =====================================<< Edit Post View >>=====================================
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.all()
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
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
        form = CreatePostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'categories': categories
    }

    return render(request, 'blog/create-post.html', context)


# =====================================<< Delete Post View >>=====================================
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()

    posts = Post.published.filter(auther=request.user)
    context = {
        'posts': posts
    }

    print(posts)
    if not post.id:
        return redirect('blog:profile_posts')

    return render(request, 'blog/profile-posts.html', context)


# =====================================<< Delete Image View >>=====================================
def delete_image(request, image_id):

    image = get_object_or_404(Image, id=image_id)
    post_id = image.post.id
    image.delete()

    return redirect('blog:edit_post', post_id)


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

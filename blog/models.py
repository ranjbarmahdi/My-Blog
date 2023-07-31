from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse


# =====================================<< Category Model >>=====================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='دسته بندی')
    slug = models.SlugField(max_length=250, verbose_name='اسلاگ')

    # ----------------------------------------------------
    objects = jmodels.jManager()

    # ----------------------------------------------------
    class Meta:
        ordering = ['name']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    # ----------------------------------------------------
    def __str__(self):
        return self.name


# =====================================<< Post Model >>=====================================
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    # ----------------------------------------------------
    class Status(models.TextChoices):
        DRAFTED = 'DF', 'Drafted'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    # ----------------------------------------------------
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name='نویسنده')
    category = models.ManyToManyField(Category, related_name='posts', verbose_name='دسته بندی')

    # ----------------------------------------------------
    title = models.CharField(max_length=250, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=250, verbose_name='اسلاگ')
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')

    # ----------------------------------------------------
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    create = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)

    # ----------------------------------------------------
    status = models.TextField(max_length=2, choices=Status.choices, default=Status.DRAFTED, verbose_name='وضعیت')

    # ----------------------------------------------------
    # objects = models.Manager()
    objects = jmodels.jManager()
    published = PublishedManager()

    # ----------------------------------------------------
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = 'پست ها'

    # ----------------------------------------------------
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    # ----------------------------------------------------
    def __str__(self):
        return self.title


# =====================================<< Ticket Model >>=====================================
class Ticket(models.Model):

    # ----------------------------------------------------
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(max_length=250, verbose_name='ایمیل')
    phone = models.CharField(max_length=12, verbose_name='شماره تماس')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')

    seen = models.BooleanField(default=False, verbose_name='دیده شده')

    # ----------------------------------------------------
    objects = jmodels.jManager()

    # ----------------------------------------------------
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    # ----------------------------------------------------
    def __str__(self):
        return self.subject

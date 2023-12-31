from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField


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
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, verbose_name='دسته بندی')

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

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            storage, path = image.image_file.storage, image.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    # ----------------------------------------------------
    def __str__(self):
        return self.title


# =====================================<< Account Model >>=====================================
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', verbose_name='اکانت')
    date_of_birth = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    bio = models.TextField(verbose_name='بایو')
    image = ResizedImageField(upload_to='profile_images/', quality=60, size=[500, 500], crop=['middle', 'center'],
                              verbose_name='تصویر', null=True, blank=True)
    job = models.CharField(max_length=250, verbose_name='شغل', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name= "اکانت"
        verbose_name_plural= "اکانت ها"


# =====================================<< Image Model >>=====================================
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_file = ResizedImageField(upload_to="post_images/", verbose_name='فایل عکس')
    title = models.CharField(null=True, blank=True, max_length=250, verbose_name='عنوان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    create = jmodels.jDateTimeField(auto_now_add=True)

    # ----------------------------------------------------
    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویرها"

    # ----------------------------------------------------
    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    # ----------------------------------------------------
    def __str__(self):
        return self.title if self.title else "None"


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


# =====================================<< Comment Model >>=====================================
class Comment(models.Model):

    # ----------------------------------------------------
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')

    # ----------------------------------------------------
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(max_length=250, verbose_name='ایمیل')
    body = models.TextField(verbose_name='پیام')

    create = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ویرایش')

    send_mail = models.BooleanField(default=False, verbose_name='ارسال ایمیل')

    active = models.BooleanField(default=False, verbose_name='وضعیت')

    # ----------------------------------------------------
    objects = jmodels.jManager()

    # ----------------------------------------------------
    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    # ----------------------------------------------------
    def __str__(self):
        return f"{self.name}:{self.post}"









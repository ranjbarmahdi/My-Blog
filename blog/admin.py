from django.contrib import admin
from .models import *
import django_jalali.admin as jadimn
from django_jalali.admin.filters import JDateFieldListFilter


# =====================================<< Post Admin >>=====================================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'auther', 'publish', 'status']
    list_display_links = ['id', 'title']
    list_filter = ['category', 'auther', 'status', ('publish', JDateFieldListFilter)]
    list_editable = ['status']
    raw_id_fields = ['auther', 'category']
    date_hierarchy = 'publish'
    ordering = ['-publish', 'title']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}


# =====================================<< Category Admin >>=====================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_filter = ['name']
    ordering = ['name']
    search_fields = ['name']


# =====================================<< Ticket Admin >>=====================================
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'phone', 'seen']
    list_display_links = ['id', 'name']
    # list_editable = ['seen']



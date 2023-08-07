from django import forms
from .models import Post, Comment


# =====================================<< Ticket Form >>=====================================
class TicketForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


# =====================================<< Comment Form >>=====================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'send_mail']


# =====================================<< Search Form >>=====================================
class SearchForm(forms.Form):
    query = forms.CharField()


# =====================================<< Create Post Form >>=====================================
class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']

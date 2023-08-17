from django import forms
from .models import Post, Comment, User, Account


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
    category = forms.CharField(max_length=250)

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']


# =====================================<< Login Form >>=====================================
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


# =====================================<< User Edit Form >>=====================================
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# =====================================<< Account Edit Form >>=====================================
class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['job', 'bio', 'date_of_birth', 'image']


# =====================================<< Change Password Form >>=====================================
class ChangePasswordForm(forms.Form):
    password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    # def clean_new_password(self):
    #     cd = self.cleaned_data
    #     if cd['new_password'] != cd['confirm_password']:
    #         raise forms.ValidationError("رمز ها تطابق ندارند")
    #     else:
    #         return cd['new_password']


# =====================================<< Register Form >>=====================================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # username = forms.CharField(max_length=100, required=True)
    # first_name = forms.CharField(max_length=250, required=True)
    # last_name = forms.CharField(max_length=250, required=True)
    # email = forms.EmailField(max_length=250, required=True)


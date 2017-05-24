from django import forms
from blog.models import Article, BlogComment, Contact


class BlogCommentForm(forms.ModelForm):

    class Meta:

        model = BlogComment
        fields = ['user_name', 'user_email', 'body']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'id': 'id_name',
                'class': 'form-control',
                'placeholder': '请输入昵称',
                'aria-describedby': 'sizing-addon1',
            }),
            'user_email': forms.TextInput(attrs={
                'id': 'id_email',
                'class': 'form-control',
                'placeholder': '请输入邮箱',
                'aria-describedby': 'sizing-addon1',
            }),
            'body': forms.Textarea(attrs={
                'id': 'id_text',
                'class': 'from-control',

                'placeholder': '说几句吧~',
            }),
        }

class ContactForm(forms.ModelForm):

    class Meta:

        model = Contact
        fields = ['user_name', 'user_email', 'title', 'body']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'user_email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'placeholder': 'Your Message'})
        }
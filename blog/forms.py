from django import forms
from blog.models import BlogComment, Contact
from haystack.forms import ModelSearchForm
from django.utils.translation import ugettext_lazy


class BlogCommentForm(forms.ModelForm):

    class Meta:

        model = BlogComment
        fields = ['user_name', 'user_email', 'body']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'id': 'id_name',
                'class': 'form-control',
                #'placeholder': '请输入昵称',
                'aria-describedby': 'sizing-addon1',
            }),
            'user_email': forms.TextInput(attrs={
                'id': 'id_email',
                'class': 'form-control',
                #'placeholder': '请输入邮箱',
                'aria-describedby': 'sizing-addon1',
            }),
            'body': forms.Textarea(attrs={
                'id': 'id_text',
                'class': 'from-control',

                #'placeholder': '说几句吧~',
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

class SearchForm(ModelSearchForm):

    # 重写搜索框属性，添加 placeholder
    q = forms.CharField(required=False, label=ugettext_lazy('Search'),
                        widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Search'}))

class UploadFileForm(forms.Form):

    file = forms.FileField()
import re

from django import forms
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ValidationError
from haystack.forms import ModelSearchForm

from blog.models import BlogComment, Contact


def validators_username(user_name):
    # 使用正则匹配验证用户名是否合法
    if re.findall('^[A-Za-z][A-Za-z0-9_.]*$', user_name) == []:
        raise ValidationError('名字只能包含字母大小写、数字、点及下划线且以字母开头')

class BlogCommentForm(forms.ModelForm):

    # 添加字段验证需要显示的定义字段属性，否则会被忽略
    user_name = forms.CharField(validators=[validators_username], widget=forms.TextInput(attrs={
        'id': 'id_name', 'class': 'form-control', 'aria-describedby': 'sizing-addon1'
    }))

    class Meta:

        model = BlogComment
        fields = ['user_name', 'user_email', 'body']

        widgets = {
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

    user_name = forms.CharField(validators=[validators_username], widget=forms.TextInput(attrs={
        'placeholder':'Name'
    }))

    class Meta:

        model = Contact
        fields = ['user_name', 'user_email', 'title', 'body']
        widgets = {
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
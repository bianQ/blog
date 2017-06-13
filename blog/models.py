from collections import defaultdict
import re

from django.db import models
from django.core.urlresolvers import reverse
import markdown2


class ArticleManage(models.Manager):

    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)

class Article(models.Model):

    STATUS_CHOICES = (
        # 草稿
        ('d', 'Draft'),
        # 已发表
        ('p', 'Published'),
    )

    objects = ArticleManage()

    title = models.CharField('标题', max_length=70)
    author = models.CharField('作者', max_length=30, default='an')
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True )
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified_time', '-created_time']

    def get_absolute_url(self):
        return reverse('detail', kwargs={'article_id': self.pk})

    def mk_body(self):
        return markdown2.markdown(self.body, extras=['fenced-code-blocks'],)

    def abstract(self):
        pattern = re.compile(r'<.*?>')
        return pattern.sub('', self.mk_body())

class Category(models.Model):

    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class BlogComment(models.Model):

    user_name = models.CharField('评论者名字', max_length=200)
    user_email = models.EmailField('评论者邮箱', max_length=200)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章',on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]

class Contact(models.Model):

    user_name = models.CharField('联系者名字', max_length=200)
    user_email = models.EmailField('联系者邮箱', max_length=200)
    title = models.CharField('标题', max_length=60)
    body = models.TextField('内容')

    def __str__(self):
        return self.title
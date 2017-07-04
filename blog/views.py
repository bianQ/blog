import datetime
import os
import base64
import json
import random
import string
import re
import io

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.datastructures import MultiValueDictKeyError
from haystack.views import SearchView
#from haystack.forms import ModelSearchForm

from blog.models import Article, Category, Tag, SecondComment, BlogComment
from blog.forms import BlogCommentForm, ContactForm, SearchForm
from blog.templatetags.paginate_tags import get_left, get_right
from blog.mail import mail
from PIL import Image


def page_not_found(request):
    return render(request, 'blog/404.html')

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        # 文章列表按照创建时间排序
        article_list = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        # 最新发布按照最近修改时间排序
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(IndexView, self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.views += 1
        obj.save(update_fields=['views'])

        return obj

    def get_context_data(self, **kwargs):
        kwargs['article_tags'] = Tag.objects.filter(article=self.kwargs['article_id'])
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        # 侧边栏显示数据
        # 客户端 IP
        #kwargs['ip'] = self.request.META['REMOTE_ADDR']
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(ArticleDetailView, self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs['cate_id'])
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p').order_by(Article._meta.ordering[1])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(CategoryView, self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p').order_by(Article._meta.ordering[1])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(TagView, self).get_context_data(**kwargs)

class ArchiveView(ListView):

    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month).order_by(Article._meta.ordering[1])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(ArchiveView, self).get_context_data(**kwargs)

class CommentPostView(FormView):

    form_class = BlogCommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        # 原邮箱 validators 的报错为英文，为了汉化，对其重新赋值
        if 'user_email' in form.errors:
            form.errors['user_email'] = '<ul class="errorlist"><li>邮箱格式错误</li></ul>'

        article_tags = Tag.objects.filter(article=self.kwargs['article_id'])
        search_form = SearchForm()
        category_list = Category.objects.all().order_by('name')
        tag_list = Tag.objects.all().order_by('name')
        date_archive = Article.objects.archive()
        recent_posts = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]

        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html',{
            'form': form,
            # 将 form.errors 对象传递到前端渲染
            'form_errors': form.errors,
            'article': target_article,
            'article_tags': article_tags,
            'comment_list': target_article.blogcomment_set.all(),
            'search_form': search_form,
            'category_list': category_list,
            'tag_list': tag_list,
            'date_archive': date_archive,
            'recent_posts': recent_posts
        })

def SecondCommentView(request):
    if request.method == 'POST':
        # 获取评论属性
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        body = request.POST['body']
        # 父评论
        father_comment_id = request.POST['commentId']
        # 被评论
        commented_id = request.POST['commentedId']
        # 生成子评论对象并关联父评论及被评论对象
        father_comment = get_object_or_404(BlogComment, pk=father_comment_id)
        comment = SecondComment(user_name=user_name, user_email=user_email, body=body)
        comment.father_comment = father_comment
        # 当父评论作为被评论对象事，值为空，否则关联对应对象
        if commented_id:
            commented = get_object_or_404(SecondComment, pk=commented_id)
            comment.commented = commented
        comment.save()
        # 给被评论者发送邮件提醒
        mail.comment_mail(comment)
        # 返回请求状态码
        content = json.dumps({'status': 200})
        return HttpResponse(content)

def About(request):
    if request.method == 'GET':
        return render(request, 'blog/about.html')

class ContactPostView(FormView):

    form_class = ContactForm
    template_name = 'blog/contact.html'

    def form_valid(self, form):
        form.save()
        new_form = ContactForm()
        # 用于提交成功后的弹窗提示
        message = '感谢您的来信'
        # 设置管理员邮箱，接收来信提醒
        to_addr = ['vagaab@foxmail.com', '1126166129@qq.com']
        mail.contact_mail(to_addr)
        return render(self.request, 'blog/contact.html', {'form': new_form, 'message':message})

    def form_invalid(self, form):
        if 'user_email' in form.errors:
            form.errors['user_email'] = '<ul class="errorlist"><li>邮箱格式错误</li></ul>'

        return render(self.request, 'blog/contact.html', {'form': form, 'form_errors':form.errors})

class AuthorView(ListView):

    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        author = self.kwargs['author']
        article_list = Article.objects.filter(author=author, status='p').order_by(Article._meta.ordering[1])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return super(AuthorView, self).get_context_data(**kwargs)

def Agree(request, article_id):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=article_id)
        agree = request.GET['agree']
        article.likes += int(agree)
        article.save(update_fields=['likes'])
        '''
        获取客户端 IP
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        '''
        return HttpResponse(article.likes)

class Search(SearchView):
    '''
    extra_context 可以添加想要的数据，用于前段渲染
    '''

    def extra_context(self):
        extra = super(Search, self).extra_context()
        extra['search_form'] = SearchForm()
        extra['category_list'] = Category.objects.all().order_by('name')
        extra['tag_list'] = Tag.objects.all().order_by('name')
        extra['date_archive'] = Article.objects.archive()
        extra['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[0])[:3]
        return extra

    #为统一分页样式，重写 get_context, 增加页面相关属性

    def get_context(self):
        context = super(Search, self).get_context()

        #计算需要显示的页码列表
        pages = get_left(context['page'].number, 3, context['page'].paginator.num_pages) + get_right(context['page'].number, 3, context['page'].paginator.num_pages)

        context['pages'] = pages
        context['current_page'] = context['page'].number
        context['last_page'] = context['page'].paginator.num_pages
        #这里直接复制 paginate_tags.py 里面的部分代码
        try:
            context['pages_first'] = pages[0]
            context['pages_last'] = pages[-1] + 1
        except IndexError:
            context['pages_first'] = 1
            context['pages_last'] = 2

        return context

def Upload(request):
    '''
    接收手动上传，与粘贴的图片
    :param request:
    :return:
    '''
    if request.method == 'POST':
        # 获取图片对象，生成图片保存路径  app/static/media/upload_date/image_name
        # 生成图片 url 返回给前端   /static/media/upload_date/image_name
        date = datetime.datetime.now().strftime('%Y%m%d')
        # 本地图片保存目录
        img_dir = os.path.join(settings.MEDIA_ROOT, date)
        # 判断目标目录是否存在，否则创建目录，如使用 Django 的文件存储工具，则可省略这一步
        # 由于使用 PIL 导致图片不能使用 Django 提供的工具保存，所以需要额外判断目录是否存在
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        try:
            image = request.FILES['files']
            filename = image.name
            img_save_path = os.path.join(img_dir, filename)
            # 获取图片尺寸
            img = Image.open(image)
            # 如果图片宽大于 700px 则，等比缩小保存
            if img.width > 700:
                width = 700
                height = int(img.height / (img.width / 700))
                img = img.resize((width, height), Image.ANTIALIAS)
                img.save(img_save_path)
            else:
                img.save(img_save_path)
                #default_storage.save(img_save_path, ContentFile(image.read()))

        except KeyError:
            # 粘贴接收的图片，为 base64 编码格式，还带有描述用的前缀
            head, image = request.POST['image'].split(',')
            # 用正则从前缀中匹配文件的类型
            image_type = re.findall(r'image/(\w+);', head)[0]
            image = base64.b64decode(image)
            # 因为没有获取文件名，所以需要随机生成一个
            # 生成由大小写字母与数字组合的字符串
            strs = string.ascii_letters + string.digits
            # 随机生成 8 位字符串
            filename = ''.join(random.sample(strs, 8)) + '.' + image_type
            img_save_path = os.path.join(img_dir, filename)

            # 获取图片尺寸
            steam = io.BytesIO(image)
            img = Image.open(steam)
            # 如果图片宽大于 700px 则，等比缩小保存
            if img.width > 700:
                width = 700
                height = int(img.height / (img.width / 700))
                img = img.resize((width, height), Image.ANTIALIAS)
                img.save(img_save_path)
            else:
                img.save(img_save_path)
                #default_storage.save(img_save_path, ContentFile(image))

        # 客户端图片访问路径
        img_path = os.path.join(os.path.join(settings.MEDIA_URL, date), filename)

        content = json.dumps({'status': 200, 'store_path': img_path})
        return HttpResponse(content)
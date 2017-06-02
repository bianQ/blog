from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Article, Category, Tag
from django.views.generic.edit import FormView
from blog.forms import BlogCommentForm, ContactForm, SearchForm
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, HttpResponse
import markdown2
from haystack.views import SearchView
#from haystack.forms import ModelSearchForm
from blog.templatetags.paginate_tags import get_left, get_right


class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
        return super(IndexView, self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
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
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
        return super(ArticleDetailView, self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
        return super(CategoryView, self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
        return super(TagView, self).get_context_data(**kwargs)

class ArchiveView(ListView):

    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
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
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html',{
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })

def About(request):
    if request.method == 'GET':
        return render(request, 'blog/about.html')

class ContactPostView(FormView):

    form_class = ContactForm
    template_name = 'blog/contact.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('blog/contact.html')

    def form_invalid(self, form):
        return render(self.request, 'blog/contact.html', {'form': form})

class AuthorView(ListView):

    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        author = self.kwargs['author']
        article_list = Article.objects.filter(author=author, status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
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
        extra['recent_posts'] = Article.objects.filter(status='p').order_by(Article._meta.ordering[1])[:3]
        return extra

    #为统一分页样式，重写 get_context, 增加页面相关属性

    def get_context(self):
        (paginator, page) = self.build_page()

        #计算需要显示的页码列表
        pages = get_left(page.number, 3, page.paginator.num_pages) + get_right(page.number, 3, page.paginator.num_pages)

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context['pages'] = pages
        context['current_page'] = page.number
        context['last_page'] = page.paginator.num_pages
        #这里直接复制 paginate_tags.py 里面的部分代码
        try:
            context['pages_first'] = pages[0]
            context['pages_last'] = pages[-1] + 1
        except IndexError:
            context['pages_first'] = 1
            context['pages_last'] = 2

        context.update(self.extra_context())

        return context
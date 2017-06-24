"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from blog import views
from blog.api.serializer import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view=views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$', view=views.ArticleDetailView.as_view(), name='detail'),
    url(r'^category/(?P<cate_id>\d+)$', view=views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', view=views.TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', view=views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)/comment/$', view=views.CommentPostView.as_view(), name='comment'),
    url(r'^about/$', view=views.About, name='about'),
    url(r'^contact/$', view=views.ContactPostView.as_view(), name='contact'),
    url(r'^author/(?P<author>\w+)/$', view=views.AuthorView.as_view(), name='author'),
    url(r'^article/(?P<article_id>\d+)/agree/$', view=views.Agree, name='agree'),
    # url(r'^search/', include('haystack.urls')),
    # ()不能去掉， 否则会报 'Search' object has no attribute 'get'
    url(r'^search/$', view=views.Search(), name='search'),
    url(r'^upload/$', view=views.Upload, name='upload'),
    # 添加 API 接口
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

handler404 = views.page_not_found
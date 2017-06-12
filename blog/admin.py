from django.contrib import admin

from blog.models import Article, Tag, Category, BlogComment, Contact


class ArticleAdmin(admin.ModelAdmin):

    change_form_template = 'blog/admin/change_form.html'

    list_display = ['title', 'author', 'status', 'topped','created_time', 'last_modified_time']
    search_fields = ['title', 'author']
    list_filter = ['created_time', 'last_modified_time']
    date_hierarchy = 'created_time'

class TagAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogComment, CommentAdmin)
admin.site.register(Contact, CommentAdmin)
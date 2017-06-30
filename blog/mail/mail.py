from django.core.mail import send_mail
from django.conf import settings


def contact_mail(to_addr):
    message = '''

    Admcenter 收到了一封来信，请登陆后台查收

    '''
    from_addr = settings.EMAIL_HOST_USER
    send_mail('Admcenter来信提醒', message, from_addr, to_addr)

def comment_mail(comment):
    # 获取被评论对象
    commented = comment.commented or comment.father_comment
    # 获取评论所属文章对象
    article = comment.father_comment.article
    to_addr = commented.user_email
    message = '''

    Dear {user}：

        您在文章 {title} 下的回复有了新的评论，点击 https://blog.admcenter.cn/article/{id} 查看

    '''.format(user=commented.user_name, title=article.title, id=article.pk)
    from_addr = settings.EMAIL_HOST_USER
    send_mail('Admcenter消息提醒', message, from_addr, to_addr)
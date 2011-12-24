from django.template import Library, TemplateSyntaxError, Variable, Node
from django.template.defaulttags import token_kwargs
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.conf import settings
from timezones.utils import adjust_datetime_to_timezone
from codrspace.models import Post, Setting

register = Library()


def localize_date(date, from_tz=None, to_tz=None):
    """
    Convert from one timezone to another
    """
    # set the defaults
    if from_tz is None:
        from_tz = settings.TIME_ZONE

    if to_tz is None:
        to_tz = "US/Central"

    return adjust_datetime_to_timezone(date, from_tz=from_tz, to_tz=to_tz)


@register.filter(name='localize')
def localize(dt, user):
    user_settings = Setting.objects.get(user=user)
    from_tz = settings.TIME_ZONE
    to_tz = user_settings.timezone

    return localize_date(dt, from_tz=from_tz, to_tz=to_tz)


class RandomBlogNode(Node):
    def render(self, context):
        random_user = User.objects.order_by('?')[0]
        return reverse('post_list', args=[random_user.username])


@register.tag
def random_blog(parser, token):
    """
    Get a random bloggers post list page
    {% random_blog %}
    """
    return RandomBlogNode()


@register.inclusion_tag("top_posters.html", takes_context=True)
def top_posters(context, amount):
    top_ps = Post.objects.raw("""
        SELECT id, author_id, count(*) as post_count
        FROM codrspace_post WHERE status='published'
        GROUP BY author_id, id ORDER BY post_count DESC
    """)
    if top_ps:
        top_ps = top_ps[:int(amount)]
    context.update({
        'top_ps': top_ps
    })
    return context


@register.inclusion_tag("lastest_posts.html", takes_context=True)
def latest_posts(context, amount):
    posts = Post.objects.filter(status="published").order_by('-publish_dt')
    if posts:
        posts = posts[:int(amount)]
    context.update({
        'posts': posts
    })
    return context


@register.inclusion_tag("recent_codrs.html", takes_context=True)
def recent_codrs(context, amount):
    codrs = User.objects.all().order_by('-last_login')
    if codrs:
        codrs = codrs[:int(amount)]
    context.update({
        'codrs': codrs
    })
    return context
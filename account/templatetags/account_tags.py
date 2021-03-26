from django import template
from articles.models import Article

register = template.Library()


@register.inclusion_tag("articles/article/articles.html")
def show_recommended_articles(count=3):
    # articles = Article.objects.all()[:count]
    # return {"articles": articles}
    pass


@register.inclusion_tag("articles/article/articles.html")
def show_recent_articles(count=10):
    pass


@register.inclusion_tag("places/place/places.html")
def show_most_popular_places(count=5):
    pass


@register.inclusion_tag("images/image/images.html")
def show_most_liked_photos(count=3):
    pass

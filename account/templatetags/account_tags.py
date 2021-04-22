from django import template

from articles.models import Article
from common.recommender import Counter, Recommender
from places.models import Place

register = template.Library()


@register.inclusion_tag("articles/article/articles.html")
def show_recommended_articles(username, count=3):
    article_ids = Recommender.get_recommendations("article", username, count)
    articles = list(Article.objects.filter(id__in=article_ids))
    articles.sort(key=lambda x: article_ids.index(x.id))
    return {"article_list": articles}


@register.inclusion_tag("places/place/places.html")
def show_most_popular_places(count=5):
    display_counter = Counter(":display_count")
    place_ids = display_counter.get_most_popular_objects("place", limit=count)
    places = list(Place.objects.filter(id__in=place_ids))
    places.sort(key=lambda x: place_ids.index(x.id))
    return {"place_list": places}


@register.inclusion_tag("articles/article/articles.html")
def show_most_popular_articles(count=5):
    display_counter = Counter(":display_count")
    article_ids = display_counter.get_most_popular_objects("article", limit=count)
    articles = list(Article.pub_objects.filter(id__in=article_ids))
    articles.sort(key=lambda x: article_ids.index(x.id))
    return {"article_list": articles}


@register.inclusion_tag("images/image/images.html")
def show_most_liked_photos(count=3):
    pass

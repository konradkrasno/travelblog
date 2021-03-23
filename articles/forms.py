from django import forms
from django.utils.text import slugify
from django.forms.models import inlineformset_factory

from .models import Article, ArticlePlace


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "publish"]

    def save(self, force_insert=False, force_update=False, commit=True):
        article = super().save(commit=False)
        article.slug = slugify(article.title)
        if commit:
            article.save()
        return article


class ArticlePlaceForm(forms.ModelForm):
    class Meta:
        model = ArticlePlace
        fields = ["place", "description"]

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["place"].required = False
        self.fields["description"].required = False
        if user_id:
            self.fields["place"].queryset = Place.objects.filter(author__id=user_id)


ArticlePlacesFormSet = inlineformset_factory(
    Article, ArticlePlace, form=ArticlePlaceForm, can_delete=False
)

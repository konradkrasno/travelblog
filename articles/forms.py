from django import forms
from django.forms.models import inlineformset_factory
from django.utils.text import slugify

from places.models import Place
from .models import Article, ArticlePlace, ArticleComment, SubComment


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ArticlePlaceForm, self).__init__(*args, **kwargs)
        self.fields["place"].queryset = Place.objects.filter(author=self.user)


BaseArticlePlacesFormSet = inlineformset_factory(
    Article, ArticlePlace, form=ArticlePlaceForm, can_delete=True
)


class ArticlePlacesFormSet(BaseArticlePlacesFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ArticlePlacesFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, *args, **kwargs):
        kwargs["user"] = self.user
        return super(ArticlePlacesFormSet, self)._construct_form(*args, **kwargs)


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["body"]


class SubCommentForm(forms.ModelForm):
    class Meta:
        model = SubComment
        fields = ["body", "main_comment"]
        widgets = {"main_comment": forms.HiddenInput}

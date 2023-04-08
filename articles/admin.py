from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        checked = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main') is True:
                checked += 1

            if checked == 0:
                raise ValidationError('Выберите основной раздел')

            if checked > 1:
                raise ValidationError('Основной раздел должен быть один')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

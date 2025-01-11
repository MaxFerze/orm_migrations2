from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        x = 0
        for form in self.forms:
            if self.deleted_forms and self._should_delete_form(form):
                continue
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data.get('is_main'):
                x += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if x != 1:
            raise ValidationError('Укажите один главный тег')
        return super().clean() # вызываем базовый код переопределяемого метода
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
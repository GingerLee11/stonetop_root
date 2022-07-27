from django.contrib import admin
from django import forms

from .models import (Campaign, 
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    CharacterClass, Character
    )

from ckeditor.widgets import CKEditorWidget


class BackgroundAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Background
        fields = ['character_class', 'background', 'description']

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    form = BackgroundAdminForm


admin.site.register(Campaign)
admin.site.register(AppearanceAttribute)
admin.site.register(Instinct)
admin.site.register(PlaceOfOrigin)
admin.site.register(CharacterClass)
admin.site.register(Character)
# admin.site.register(Background)
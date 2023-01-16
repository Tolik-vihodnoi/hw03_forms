from django import forms
from django.forms import ModelForm, Textarea

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 10}),
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError('Поле обязательно для заполнения')
        return data

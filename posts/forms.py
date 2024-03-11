from django import forms
from django.forms import ModelForm

from .models import Post, Comment, Reply


class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags')
        labels = {
            'image': 'Фото',
            'body': 'Текст',
            'tags': 'Категория'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Добавь запись...',
                'class': 'font1 text-2xl'
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
        labels = {
            'tags': 'Категория',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'class': 'font1 text-2xl'
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Оставь комментарий ...', }),
        }
        labels = {
            'body': '',
        }


class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('body', )
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Ответить на комментарий ...', 'class': '!text-sm'}),
        }
        labels = {
            'body': '',
        }
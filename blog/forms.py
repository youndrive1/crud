from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'body']

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='댓글', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['body']
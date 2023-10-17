from django import forms
from .models import Comment, Post

class CreatePostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ["title", "content", "status"]

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.status == 1:
            self.fields['title'].disabled = True
            self.fields['status'].disabled = True


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

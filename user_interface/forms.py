from django import forms
from django.forms import widgets
from .models import Post, PostComments


# class CreatePost(forms.Form):
#     body = forms.CharField(
#         max_length=255,
#         widget=forms.Textarea(attrs={'rows':4, 'cols': 5}),
#         label="Share something with your friends", 
#         required=False
#         )
#     image = forms.ImageField(label="", required=False)

class CreatePost(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "What's on your mind?"}))
    image = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'style': 'margin-bottom:1rem;'}), required=False)

    class Meta:
        model = Post
        fields = ['body', 'image']


class CreateComment(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'comment-section'}))

    class Meta:
        model = PostComments
        fields = ['comment']

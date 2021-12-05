from django import forms


class CreatePost(forms.Form):
    body = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'rows':4, 'cols': 5}),
        label="Share something with your friends", 
        required=False
        )
    image = forms.ImageField(label="", required=False)

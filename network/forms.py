from django import forms

class PostForm(forms.Form):
    message = forms.CharField(
        max_length=500,
        required=True,
        label=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
        })
    )
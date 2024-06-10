from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(max_length=1000, label="", widget=forms.Textarea(attrs={
        "id": "comment-text-form", "class": "comment-textarea", "placeholder": "Comment here"}))


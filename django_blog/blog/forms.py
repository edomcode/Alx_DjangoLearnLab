from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3
            }),
        }

   
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) == 0:
            raise forms.ValidationError("Comment cannot be empty.")
        return content

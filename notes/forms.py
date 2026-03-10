from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and updating notes with validation."""
    
    class Meta:
        model = Note
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title',
                'id': 'id_title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note description (at least 10 characters)',
                'rows': 5,
                'id': 'id_description'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description', '')
        
        if description and len(description) < 10:
            self.add_error('description', 'Description must be at least 10 characters long.')
        
        return cleaned_data

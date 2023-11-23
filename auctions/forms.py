from django import forms
from .models import Listing, Category, Comment


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'image', 'imageUrl',
                  'price', 'category',
                  ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Description'}),
            # 'image': forms.ImageField(attrs={'class': 'form-control'}),
            # 'imageUrl': forms.URLField(attrs={'class': 'form-control', 'placeholder': 'Type Image Url'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0.00 $'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Chose one'}),
        }


class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
        }
        labels = {
            'title': "Title"
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Write your comment..."})
        }

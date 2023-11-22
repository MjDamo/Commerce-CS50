from django import forms
from .models import Listing


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
            'image': forms.ImageField(attrs={'class': 'form-control', 'value': 'Upload Image'}),
            'imageUrl': forms.URLField(attrs={'class': 'form-control', 'placeholder': 'Type Image Url'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0.00 $'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Chose one'}),
        }


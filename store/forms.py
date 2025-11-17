from django import forms
from .models import ContactMessage, NewsletterSubscriber, Review


class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Your Phone'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'stext-111 cl2 plh3 size-120 p-lr-18 p-tb-3',
                'placeholder': 'Your Message',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['message'].required = True


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input1 bg-none plh1 stext-107 cl7',
                'placeholder': 'email@example.com'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed to our newsletter.")
        return email


class ReviewForm(forms.ModelForm):
    """Product review form"""
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Very Good'),
        (3, '3 - Good'),
        (2, '2 - Fair'),
        (1, '1 - Poor'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-input'})
    )

    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'stext-111 cl2 plh3 size-116 p-lr-18 p-tb-3',
                'placeholder': 'Your Email'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'stext-111 cl2 plh3 size-120 p-lr-18 p-tb-3',
                'placeholder': 'Your Review',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['rating'].required = True
        self.fields['comment'].required = True


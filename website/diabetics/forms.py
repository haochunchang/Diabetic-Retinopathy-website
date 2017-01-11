from django import forms

class ImageUploadForm(forms.Form):
    '''Image upload form.'''
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

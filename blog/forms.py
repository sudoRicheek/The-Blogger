from django import forms

class CreateBlogForm(forms.Form):
    blogTitle = forms.CharField(label='Blog Title', max_length=100)
    blogContent = forms.CharField(label='Your Awesome Article Goes Here', widget=forms.Textarea)

class EditBlogForm(forms.Form):
    blogTitle = forms.CharField(label='Blog Title', max_length=100)
    blogContent = forms.CharField(label='Edit Your Awesome Article Here', widget=forms.Textarea)

class DeleteConfirmationForm(forms.Form):
    CHOICES = [('1', 'YES'),('2', 'NO')]
    Choose = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

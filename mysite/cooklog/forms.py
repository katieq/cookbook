from django import forms
from cooklog.models import Dish_Photo, Dish, Ingredient, Chef_Dish_Comments, Likes

#class ChefEntryForm(forms.Form):
#    first_name = forms.CharField()
#    last_name = forms.CharField()
#    email_address = forms.EmailField(required=False)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Dish_Photo
        fields = ['dish_id', 'dish_image', 'photo_comment', 'date_created']
    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['dish_id'].widget.attrs['size']= 20
        for key in self.fields:
            self.fields[key].required = False

class NewDishForm(forms.ModelForm):
    #class Meta:
    #    model = Dish
    #    fields = ['dish_name', 'recipe_id', 'dish_method', 'dish_rating',
    #              'dish_comments', 'ingredient_id', 'date_created']
    #long_desc = forms.CharField(widget=forms.Textarea)
    #short_desc = forms.CharField(widget=forms.Textarea)
    dish_name = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    photo_comment = forms.CharField(widget=forms.Textarea)
    ingredient_id = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.SelectMultiple) # or CheckboxSelectMultiple
    #date_created = forms.DateField(widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    class Meta:
        model = Dish
        fields = ['dish_name', 'chef_id', 'recipe_id', 'dish_status', 'date_scheduled',
                  'date_created', 'dish_source', 'dish_method', 'dish_rating',
                  'dish_comments', 'dish_image','photo_comment', 'ingredient_id']
    
    def __init__(self, *args, **kwargs):
        super(NewDishForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['rows'] = 5
        self.fields['dish_comments'].widget.attrs['cols'] = 80
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        self.fields['photo_comment'].widget.attrs['rows'] = 1
        self.fields['photo_comment'].widget.attrs['cols'] = 80
        self.fields['ingredient_id'].widget.attrs['size']= 30
        for key in self.fields:
            self.fields[key].required = False

class UpdateDishForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    photo_comment = forms.CharField(widget=forms.Textarea)
    ingredient_id = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                   widget=forms.SelectMultiple) # or CheckboxSelectMultiple
    class Meta:
        model = Dish
        fields = ['dish_name', 'chef_id', 'recipe_id', 'dish_status', 'date_scheduled', 'date_created',
                    'dish_source', 'dish_method', 'dish_rating','dish_comments',
                  'dish_image', 'photo_comment', 'ingredient_id']

    def __init__(self, *args, **kwargs):
        super(UpdateDishForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['rows'] = 5
        self.fields['dish_comments'].widget.attrs['cols'] = 80
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        self.fields['photo_comment'].widget.attrs['rows'] = 1
        self.fields['photo_comment'].widget.attrs['cols'] = 80
        self.fields['ingredient_id'].widget.attrs['size']= 30
        for key in self.fields:
            self.fields[key].required = False

class NewLikeForm(forms.ModelForm):
    next = forms.CharField(required=False)
    class Meta:
        model = Likes
        fields = ['dish_id', 'chef_id']
    def __init__(self, *args, **kwargs):
        super(NewLikeForm, self).__init__(*args, **kwargs)
        self.fields['dish_id'].widget = forms.HiddenInput()
        self.fields['next'].widget = forms.HiddenInput()
        self.fields['chef_id'].widget = forms.HiddenInput()
        for key in self.fields:
            self.fields[key].required = False

class NewCommentForm(forms.ModelForm):
    next = forms.CharField(required=False)
    class Meta:
        model = Chef_Dish_Comments
        exclude = tuple()
        fields = ['dish_id', 'chef_id', 'chef_dish_comment']
    def __init__(self, *args, **kwargs):
        super(NewCommentForm, self).__init__(*args, **kwargs)
        self.fields['dish_id'].widget = forms.HiddenInput()
        self.fields['next'].widget = forms.HiddenInput()
        self.fields['chef_id'].widget = forms.HiddenInput()
        for key in self.fields:
            self.fields[key].required = False

# may be able to delete ALL of this.
class CommentDeleteForm(forms.ModelForm):
    next = forms.CharField(required=False)
    class Meta:
        model = Chef_Dish_Comments
        exclude = tuple()
    def __init__(self, *args, **kwargs):
        super(NewCommentForm, self).__init__(*args, **kwargs)
        self.fields['next'].widget = forms.HiddenInput()
        for key in self.fields:
            self.fields[key].required = False



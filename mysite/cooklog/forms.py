from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from cooklog.models import Chef, Dish, Recipe, Ingredient, Chef_Dish_Comments, ChefFollows ##Likes,
from datetime import datetime
import calendar
from dal import autocomplete
from itertools import chain

# from django.forms import inlineformset_factory

#from mentions.forms import MentionTextarea

#class ChefEntryForm(forms.Form):
#    first_name = forms.CharField()
#    last_name = forms.CharField()
#    email_address = forms.EmailField(required=False)

#class UploadImageForm(forms.ModelForm):
#    class Meta:
#        model = Dish_Photo
#        fields = ['dish_id', 'dish_image', 'photo_comment', 'date_created']
#    def __init__(self, *args, **kwargs):
#        super(UploadImageForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
#        self.fields['dish_id'].widget.attrs['size']= 20
#        for key in self.fields:
#            self.fields[key].required = False


class NewDishQuickForm(forms.ModelForm):

    if datetime.now().hour < 10:
        initial_dish_name = calendar.day_name[datetime.today().weekday()] + ' Breakfast'
    elif datetime.now().hour < 14:
        initial_dish_name = calendar.day_name[datetime.today().weekday()] + ' Lunch'
    elif datetime.now().hour < 17:
        initial_dish_name = calendar.day_name[datetime.today().weekday()] + ' Afternoon Tea'
    else:
        initial_dish_name = calendar.day_name[datetime.today().weekday()] + ' Dinner'

    dish_name = forms.CharField(initial= initial_dish_name)
    # dish_rating = forms.IntegerField(initial = 3)
    dish_rating = forms.ChoiceField(required=False,widget=forms.RadioSelect,choices=((1,1),(2,2),(3,3),(4,4),(5,5)),)
    
    class Meta:
        model = Dish
        fields = ['recipe_id', 'chef_id', 'dish_status',
                  'date_created', 'dish_image', 'dish_name', 'dish_rating', 'tags']
    
    def __init__(self, *args, **kwargs):
        super(NewDishQuickForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['dish_status'].widget = forms.HiddenInput()
        self.fields['date_created'].widget = forms.HiddenInput()
        self.fields['recipe_id'].widget = forms.HiddenInput() # Default to 1 = "None"
        
        self.fields['dish_name'].label = "Dish name"
        # self.fields['dish_rating'].label = "Rating (/5)"
        self.fields['dish_image'].label = "Upload/take photo"

        for key in self.fields:
            self.fields[key].required = False


class NewDishShortForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea) #MentionTextarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    date_created = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(2015, 2027)),
                                   initial=datetime.now())
#    NOT WORKING!! recipe_id = forms.ModelChoiceField(queryset=Recipe.objects.all(),
#                                       widget=autocomplete.ModelSelect2(url='recipe-autocomplete'))
    class Meta:
        model = Dish
        fields = ['chef_id', 'dish_status', 'recipe_id', 'date_created', 'dish_name',
                  'tags', 'dish_image', 'dish_method',
                  'dish_comments', 'dish_rating'] #, 'dish_diagram_image']
#        widgets = {
#            'recipe_id': autocomplete.ModelSelect2(url='recipe-autocomplete',
#                                                   attrs={
#                                                   'data-placeholder': 'Autocomplete ...',
#                                                   'data-minimum-input-length': 3,
#                                                   },)
#        }
    def __init__(self, *args, **kwargs):
        super(NewDishShortForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['dish_status'].widget = forms.HiddenInput()
        # self.fields['date_created'].widget = forms.HiddenInput()
        
        self.fields['recipe_id'].label = "Recipe"
        self.fields['dish_name'].label = "Dish name"
        self.fields['dish_method'].label = "Method (or changes from recipe)"
        self.fields['dish_comments'].label = "Review/notes"
        self.fields['dish_rating'].label = "Rating (/5)"
        self.fields['dish_image'].label = "Photo"
        # self.fields['dish_diagram_image'].label = "(diagram)"

        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 50
        self.fields['dish_method'].widget.attrs['cols'] = 50
        self.fields['dish_method'].widget.attrs['rows'] = 5
        self.fields['dish_comments'].widget.attrs['cols'] = 50
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        for key in self.fields:
            self.fields[key].required = False

class NewDishTodoForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea)
    date_scheduled = forms.DateField(widget = SelectDateWidget(empty_label="Nothing"),initial=datetime.now())
    class Meta:
        model = Dish
        fields = ['chef_id', 'dish_status', 'recipe_id',
                  'date_created', 'date_scheduled', 'dish_name',
                  'tags', 'dish_source',
                  'dish_method', 'dish_comments']
    
    def __init__(self, *args, **kwargs):
        super(NewDishTodoForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['dish_status'].widget = forms.HiddenInput()
        self.fields['date_created'].widget = forms.HiddenInput()
        
        self.fields['recipe_id'].label = "Recipe"
        self.fields['dish_name'].label = "Dish name"
        self.fields['dish_comments'].label = "Review/notes"
        self.fields['date_scheduled'].label = "When to cook"
        self.fields['dish_source'].label = "Recipe source (optional)"
        self.fields['dish_method'].label = "Method (or changes from recipe)"
        
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 50
        self.fields['dish_comments'].widget.attrs['cols'] = 50
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        self.fields['dish_method'].widget.attrs['cols'] = 50
        self.fields['dish_method'].widget.attrs['rows'] = 5
        for key in self.fields:
            self.fields[key].required = False

# CURRENTLY NOT USED!
class NewDishTodoQuickForm(forms.ModelForm):
    date_scheduled = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"), initial=datetime.now())

    class Meta:
        model = Dish
        fields = ['recipe_id', 'dish_name', 'chef_id', 'dish_status', 'date_scheduled', 'tags']

    def __init__(self, *args, **kwargs):
        super(NewDishTodoQuickForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['dish_status'].widget = forms.HiddenInput()
        self.fields['recipe_id'].widget = forms.HiddenInput()

        self.fields['dish_name'].label = "Dish name"
        self.fields['date_scheduled'].label = "When to cook"

        for key in self.fields:
            self.fields[key].required = False


class NewDishLongForm(forms.ModelForm):
    #class Meta:
    #    model = Dish
    #    fields = ['dish_name', 'recipe_id', 'dish_method', 'dish_rating',
    #              'dish_comments', 'ingredient_id', 'date_created']
    #long_desc = forms.CharField(widget=forms.Textarea)
    #short_desc = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    # photo_comment = forms.CharField(widget=forms.Textarea)
    # ingredient_id = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.SelectMultiple) # or CheckboxSelectMultiple
    #date_created = forms.DateField(widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    #date_scheduled = forms.DateField(widget = SelectDateWidget(empty_label="Nothing"),initial=datetime.now())
    date_created = forms.DateField(widget = SelectDateWidget(empty_label="Nothing",years=range(2015, 2027)),initial=datetime.now())
    class Meta:
        model = Dish
        fields = ['recipe_id', 'dish_name', 'chef_id', 'dish_status', 'date_scheduled',
                  'date_created', 'tags', 'dish_source', 'dish_method', 'dish_rating',
                  'dish_comments', 'dish_image'] #, 'dish_diagram_image'] #'photo_comment', 'ingredient_id'
    
    def __init__(self, *args, **kwargs):
        super(NewDishLongForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        
        self.fields['recipe_id'].label = "Recipe"
        self.fields['dish_name'].label = "Dish name"
        self.fields['dish_method'].label = "Method (or changes from recipe)"
        self.fields['dish_comments'].label = "Review/notes"
        self.fields['dish_rating'].label = "Rating (/5)"
        self.fields['dish_image'].label = "Photo"
        #self.fields['dish_diagram_image'].label = "(diagram)"

        self.fields['dish_method'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['rows'] = 5
        self.fields['dish_comments'].widget.attrs['cols'] = 80
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        # self.fields['photo_comment'].widget.attrs['rows'] = 1
        # self.fields['photo_comment'].widget.attrs['cols'] = 80
        # self.fields['ingredient_id'].widget.attrs['size']= 10
        for key in self.fields:
            self.fields[key].required = False

class UpdateDishForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    dish_method = forms.CharField(widget=forms.Textarea)
    dish_comments = forms.CharField(widget=forms.Textarea)
    # photo_comment = forms.CharField(widget=forms.Textarea)
    date_created = forms.DateField(widget = SelectDateWidget(empty_label="Nothing",years=range(2015, 2027)),initial=datetime.now())
    # ingredient_id = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
    #                                                widget=forms.SelectMultiple) # or CheckboxSelectMultiple
    class Meta:
        model = Dish
        fields = ['dish_name', 'chef_id', 'recipe_id', 'dish_status', 'date_scheduled', 'date_created', 'tags',
                    'dish_source', 'dish_method', 'dish_rating','dish_comments',
                  'dish_image'] #, 'dish_diagram_image'] # NOT diagram_text because this form doesn't render., 'dish_diagram_text'] #, 'photo_comment', 'ingredient_id'

    def __init__(self, *args, **kwargs):
        super(UpdateDishForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['cols'] = 80
        self.fields['dish_method'].widget.attrs['rows'] = 5
        self.fields['dish_comments'].widget.attrs['cols'] = 80
        self.fields['dish_comments'].widget.attrs['rows'] = 5
        # self.fields['photo_comment'].widget.attrs['rows'] = 1
        # self.fields['photo_comment'].widget.attrs['cols'] = 80
        # self.fields['ingredient_id'].widget.attrs['size']= 10
        for key in self.fields:
            self.fields[key].required = False

class UpdateDishDiagramForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Dish
        fields = ['dish_name', 'dish_diagram_text']
    def __init__(self, *args, **kwargs):
        super(UpdateDishDiagramForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 80
        self.fields['dish_diagram_text'].widget.attrs['cols'] = 80
        self.fields['dish_diagram_text'].widget.attrs['rows'] = 15
        for key in self.fields:
            self.fields[key].required = False


class UpdateDishPhotoForm(forms.ModelForm):
    dish_name = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Dish
        fields = ['dish_name', 'dish_image'] #, 'photo_comment']
    def __init__(self, *args, **kwargs):
        super(UpdateDishPhotoForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['dish_name'].widget.attrs['rows'] = 1
        self.fields['dish_name'].widget.attrs['cols'] = 80
        for key in self.fields:
            self.fields[key].required = False


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'recipecategory_id', 'tags', 'recipe_source', 'recipe_method',
                  'recipe_comments', 'recipe_image', 'chef_id','date_created']
    def __init__(self, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['chef_id'].widget = forms.HiddenInput()
        self.fields['recipecategory_id'].label = "Recipe category"
        self.fields['recipe_source'].label = "Source (book/url/you)"
        self.fields['recipe_method'].label = "Ingr/Method"
        self.fields['recipe_comments'].label = "Notes"
        self.fields['recipe_image'].label = "Upload/take photo"
        for key in self.fields:
            self.fields[key].required = False

class UpdateChefFollowsForm(forms.ModelForm):
    class Meta:
        model = ChefFollows
        fields = ['follower_id', 'chef_id', 'date_created']
    def __init__(self, *args, **kwargs):
        super(UpdateChefFollowsForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['follower_id'].widget = forms.HiddenInput()
        self.fields['chef_id'].widget.attrs['size']= 10
        for key in self.fields:
            self.fields[key].required = False



#class NewLikeForm(forms.ModelForm):
#    next = forms.CharField(required=False)
#    class Meta:
#        model = Likes
#        fields = ['dish_id', 'chef_id']
#    def __init__(self, *args, **kwargs):
#        super(NewLikeForm, self).__init__(*args, **kwargs)
#        self.fields['dish_id'].widget = forms.HiddenInput()
#        self.fields['next'].widget = forms.HiddenInput()
#        self.fields['chef_id'].widget = forms.HiddenInput()
#        for key in self.fields:
#            self.fields[key].required = False

class NewCommentForm(forms.ModelForm):
    chef_dish_comment = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                    'autocomplete': 'off',
                                                    'size': '15',
                                                    'class': 'add-comment',}))
    class Meta:
        model = Chef_Dish_Comments
        exclude = tuple()
        fields = ['dish_id', 'chef_id', 'chef_dish_comment']
    def __init__(self, *args, **kwargs):
        super(NewCommentForm, self).__init__(*args, **kwargs)
        self.fields['dish_id'].widget = forms.HiddenInput()
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



class RecipeChooseForm(forms.ModelForm):
    next = forms.CharField(required=False)
    class Meta:
        model = Dish
        exclude = tuple()
        fields = ['dish_id', 'recipe_id']
    def __init__(self, *args, **kwargs):
        super(RecipeChooseForm, self).__init__(*args, **kwargs)
        self.fields['recipe_id'].widget = forms.HiddenInput()
        self.fields['next'].widget = forms.HiddenInput()
        for key in self.fields:
            self.fields[key].required = False

class NewLikeForm(forms.ModelForm):
    dish_id = forms.CharField(widget=forms.Textarea)
    like_chef_id = forms.ModelMultipleChoiceField(queryset=Chef.objects.all(), widget=forms.SelectMultiple)
    class Meta:
        model = Dish
        exclude = tuple()
        fields = ['dish_id', 'like_chef_id']
    def __init__(self, *args, **kwargs):
        super(NewLikeForm, self).__init__(*args, **kwargs)
        # self.fields['dish_id'].widget = forms.HiddenInput()
        # self.fields['like_chef_id'].widget = forms.HiddenInput()
        for key in self.fields:
            self.fields[key].required = False
    # def clean_like_chef_id(self):
    #     data = list(chain(self.cleaned_data['like_chef_id'], self.object.like_chef_id.all())) #Chef.objects.all()))
    #     # data = list(chain(self.object.like_chef_id.all(),
    #     #                   Chef.objects.filter(chef_id=self.request.user.id).all()))
    #     return data

# # not used: attempted to use this to update method on dish detail (now, if want to, know how to use "html" to do it)
# class UpdateDishMethodForm(forms.ModelForm):
#     dish_method = forms.CharField(label="",
#                              widget=forms.Textarea(attrs={'autofocus': 'autofocus',
#                                                     'autocomplete': 'off',
#                                                     'cols': '65',
#                                                     'rows': '10',
#                                                     'class': 'edit-method',
#                                                     }))
#     class Meta:
#         model = Dish
#         exclude = tuple()
#         fields = ['dish_method'] #dish_id', 'dish_method']
#     def __init__(self, *args, **kwargs):
#         super(UpdateDishMethodForm, self).__init__(*args, **kwargs)
#         # self.fields['dish_id'].widget = forms.HiddenInput()
#         for key in self.fields:
#             self.fields[key].required = False
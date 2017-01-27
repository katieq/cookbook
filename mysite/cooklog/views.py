from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from cooklog.models import Dish, Chef, Recipe, Ingredient, Dish_Photo
#from cooklog.forms import ChefEntryForm
#from django.views.generic import CreateView
from cooklog.forms import UploadImageForm, NewDishForm
from django import forms


# Create your views here.
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            dishs = Dish.objects.filter(dish_name__icontains=q)
            return render(request, 'search_results.html',
                          {'dishs': dishs, 'query': q})
    return render(request, 'search_form.html', {'errors': errors})

class ChefList(ListView):
    model = Chef
    context_object_name = 'all_chefs'

class RecipeList(ListView):
    model = Recipe
    context_object_name = 'all_recipes'

class DishList(ListView):
    model = Dish
    context_object_name = 'all_dishes'
    # ideally: send all photos in here too. maybe requires other than ListView

class IngredientList(ListView):
    model = Ingredient
    context_object_name = 'all_ingredients'

class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_dishs'] = Dish.objects.order_by("-date_created").all()[:5]
        context['latest_photos'] = Dish_Photo.objects.filter(dish_id = context['latest_dishs'])
        context['latest_recipes'] = Recipe.objects.filter(dish = context['latest_dishs'])
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView,
                        self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(recipe_id=self.object.recipe_id)
        context['photos'] = Dish_Photo.objects.filter(dish_id = context['dishes'])
        context['now'] = timezone.now()
        return context

class DishDetailView(DetailView):
    model = Dish
    def get_context_data(self, **kwargs):
        context = super(DishDetailView,
                        self).get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(recipe_id = self.object.recipe_id_id)
        try:
            context['photo'] = Dish_Photo.objects.get(dish_id=self.object.dish_id)  #only allows 1photo per dish
        except:
            context['photo'] = Dish_Photo.objects.none() # fake for now.
        return context

class ChefDetailView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefDetailView, self).get_context_data(**kwargs)
        context['latest_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).order_by("-date_created").all()[:3]
        context['latest_photos'] = Dish_Photo.objects.filter(dish_id = context['latest_dishes'])
        context['best_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).order_by("-dish_rating").all()[:3]
        context['best_photos'] = Dish_Photo.objects.filter(dish_id = context['best_dishes'])
        return context

class IngredientDetailView(DetailView):
    model = Ingredient
    def get_context_data(self, **kwargs):
        context = super(IngredientDetailView, self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(ingredient_id = self.object.ingredient_id)
        return context

class RecipeCreate(CreateView):
    model = Recipe
    fields = ['recipe_name', 'recipe_source', 'recipe_type', 'chef_id', 'date_created']

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['recipe_name', 'recipe_source', 'recipe_type', 'chef_id', 'date_created']

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')

class ChefCreate(CreateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created'] #..now! (or default=now)

class ChefUpdate(UpdateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created']

class DishCreate(CreateView):
    form_class = NewDishForm
    template_name = 'new_dish_form.html'
    success_url = '/cooklog/dishes/'
    #model = Dish
    #fields = ['dish_name', 'recipe_id', 'dish_method', 'dish_rating',
#          'dish_comments', 'ingredient_id', 'date_created']

class DishUpdate(UpdateView):
    model = Dish
    fields = ['dish_name', 'chef_id', 'recipe_id', 'dish_method', 'dish_rating',
              'dish_comments', 'ingredient_id', 'date_created']

class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['ingredient_name', 'ingredient_type', 'date_created']

class IngredientUpdate(UpdateView):
    model = Ingredient
    fields = ['ingredient_name', 'ingredient_type', 'date_created']

def my_image(request):
    image_data = open("/Users/katiequinn/Documents/parkrun_barcode.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")


class UploadImageView(CreateView):
    form_class = UploadImageForm
    template_name = 'upload.html'
    success_url = '/cooklog/dishes/'


from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from cooklog.models import Dish, Chef, Recipe, Ingredient, Dish_Photo, Chef_Dish_Comments, Likes
#from cooklog.forms import ChefEntryForm
#from django.views.generic import CreateView
from cooklog.forms import UploadImageForm, NewDishForm, NewLikeForm, NewCommentForm, CommentDeleteForm
from cooklog.forms import UpdateDishForm
from django import forms
from django.contrib.auth.models import User


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

def search(request): # this still works for searching dish names!
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 40:
            errors.append('Please enter at most 40 characters.')
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
        context['latest_dishs'] = Dish.objects.filter(dish_status = 1).order_by("-date_created").all()[:10]
        #context['latest_photos'] = Dish_Photo.objects.filter(dish_id = context['latest_dishs'])
        #context['latest_recipes'] = Recipe.objects.filter(dish = context['latest_dishs'])
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView,
                        self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).order_by("-date_created")
        #context['photos'] = Dish_Photo.objects.filter(dish_id = context['dishes']) # hm, only returns for first one?!
        #context['now'] = timezone.now()
        return context

class DishDetailView(DetailView):
    model = Dish
    def get_context_data(self, **kwargs):
        context = super(DishDetailView,
                        self).get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(recipe_id = self.object.recipe_id_id)
        #context['photos'] = Dish_Photo.objects.filter(dish_id = self.object.dish_id)
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id = self.object.dish_id)
        context['likes'] = Likes.objects.filter(dish_id = self.object.dish_id)
        return context

class ChefDetailView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefDetailView, self).get_context_data(**kwargs)
        context['latest_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).order_by("-date_created").all()[:5]
        context['best_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).order_by("-dish_rating").all()[:3]
        context['all_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).order_by("-date_created").all()[6:]
        context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 2).order_by("-date_created").all()
        return context

class ChefScheduleView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefScheduleView, self).get_context_data(**kwargs)
        context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 2).order_by("date_scheduled").all()
        return context

class ChefBriefView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefBriefView, self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).order_by("-date_created").all()
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
    success_url = "/cooklog/recipes/" # todo maybe later to that recipe's page? (itd be maximum recipe_id?)

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['recipe_name', 'recipe_source', 'recipe_type', 'chef_id', 'date_created']

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')

class ChefCreate(CreateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created', 'chef_to_user_id'] #..now! (or default=now)
    def get_success_url(self):
        return '/cooklog/chef/' + str(self.object.chef_id) + '/'


class ChefUpdate(UpdateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created']

class DishCreate(CreateView):
    form_class = NewDishForm
    template_name = 'new_dish_form.html'
    #success_url = '/cooklog/dishes/'
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'


    #model = Dish
    #fields = ['dish_name', 'recipe_id', 'dish_method', 'dish_rating',
#          'dish_comments', 'ingredient_id', 'date_created']

class DishUpdate(UpdateView):
    #model = Dish
    template_name = 'update_dish_form.html'
    form_class = UpdateDishForm
    def get_queryset(self):
        return Dish.objects.filter(dish_id=self.kwargs.get("pk", None))
        #fields = ['dish_name', 'chef_id', 'recipe_id', 'dish_status', 'date_scheduled',
        #      'date_created', 'dish_source', 'dish_method', 'dish_rating',
        #      'dish_comments', 'ingredient_id', 'dish_image', 'photo_comment']
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'



class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['ingredient_name', 'ingredient_type', 'date_created']
    success_url = '/cooklog/ingredients/' # maybe later to that ingredient's page?

class IngredientUpdate(UpdateView):
    model = Ingredient
    fields = ['ingredient_name', 'ingredient_type', 'date_created']

def my_image(request):
    image_data = open("/Users/katiequinn/Documents/parkrun_barcode.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")


class UploadImageView(CreateView):
    form_class = UploadImageForm
    template_name = 'upload.html'
    success_url = '/cooklog/dishes/' # ideally it would be that dish!!

class NewCommentView(CreateView):
    form_class = NewCommentForm
    template_name = 'new_comment_form.html'
    #success_url = '/cooklog/dishes/'  # ideally goes to that dish!
    def get_initial(self):
        return {'dish_id' : self.request.GET.get('next') }
    def get_form_kwargs(self, **kwargs):
        kwargs = super(NewCommentView, self).get_form_kwargs()
        redirect = self.request.GET.get('next')   # these 3 "next" necessary for next charfield to be next=..
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs
    def form_invalid(self, form):
        import pdb;pdb.set_trace()  # debug example
        # inspect the errors by typing the variable form.errors
        # in your command line debugger. See the pdb package for
        # more useful keystrokes
        return super(NewCommentView, self).form_invalid(form)
    def form_valid(self, form):
        redirect = form.cleaned_data.get('next')   # this necessary as next after submit
        if redirect:
            self.success_url = '/cooklog/dish/' + redirect + '/' # hardcodes url, oh well.
        return super(NewCommentView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(NewCommentView, self).get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(dish_id = self.request.GET.get('next'))
        return context

class NewLikeView(CreateView):
    form_class = NewLikeForm
    template_name = 'new_like_form.html'
    #success_url = '/cooklog/dishes/' # ideally goes to that dish!
    def get_initial(self):
        return {'dish_id' : self.request.GET.get('next') }
    def get_form_kwargs(self, **kwargs):
        kwargs = super(NewLikeView, self).get_form_kwargs()
        redirect = self.request.GET.get('next')
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs
    def form_invalid(self, form):
        import pdb;pdb.set_trace()  # debug example
        # inspect the errors by typing the variable form.errors
        # in your command line debugger. See the pdb package for
        # more useful keystrokes
        return super(NewLikeView, self).form_invalid(form)
    def form_valid(self, form):
        redirect = form.cleaned_data.get('next')   # this necessary as next after submit
        if redirect:
            self.success_url = '/cooklog/dish/' + redirect + '/' # hardcodes url, oh well.
        return super(NewLikeView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(NewLikeView, self).get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(dish_id = self.request.GET.get('next'))
        return context


class CommentDeleteView(DeleteView):
    model = Chef_Dish_Comments
    form_class = CommentDeleteForm
    template_name = 'cooklog/comment_confirm_delete.html'
    #success_url = '/cooklog/dishes/' # later send it back using "next"
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Dish in your model
        #dish_id = self.object.dish_id
        return '/cooklog/dish/' + str(self.request.GET.get('next')) + '/'





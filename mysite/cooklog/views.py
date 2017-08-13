from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from cooklog.models import Dish, Chef, Recipe, Ingredient, Chef_Dish_Comments, ChefFollows, RecipeCategory, Bugs #Dish_Photo
#from cooklog.forms import ChefEntryForm
#from django.views.generic import CreateView
from cooklog.forms import NewDishShortForm, NewDishQuickForm, NewDishTodoForm, NewDishLongForm, NewCommentForm, CommentDeleteForm, NewRecipeForm, UpdateChefFollowsForm, NewLikeForm # UploadImageForm,
from cooklog.forms import RecipeChooseForm
from cooklog.forms import UpdateDishForm, UpdateDishPhotoForm #, NewDishWeekTodoForm
from django import forms
from django.forms.formsets import formset_factory
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import timedelta
from django.db.models import Q
from functools import reduce
#from nltk.corpus import stopwords # <- used for "search match" of existing recipe name to dish name,
from stop_words import get_stop_words
import string
from dal import autocomplete
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormMixin

#from django.views.decorators.http import require_POST
#try:
#    from django.utils import simplejson as json
#except ImportError:
#    import json


#@login_required
#@require_POST
#def like(request):
#    if request.method == 'POST':
#        user = request.user
#        dish = Dish.objects.filter(dish_id = request.GET['d'])
#        
#        if dish.like_chef_id.filter(id=user.id).exists():
#            # user has already liked this company
#            # remove like/user
#            dish.likes.remove(user)
#            message = 'You disliked this'
#        else:
#            # add a new like for a company
#            dish.like_chef_id.add(user)
#            message = 'You liked this'
#    ctx = {'likes_count': dish.likes.count(), 'message': message}
#    # use mimetype instead of content_type if django < 5
#    return HttpResponse(json.dumps(ctx), content_type='application/json')


class RecipeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Recipe.objects.none()
        qs = Recipe.objects.all()
        if self.q:
            qs = qs.filter(recipe_name__icontains=self.q)
        return qs

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
            #dishes = Dish.objects.filter(dish_method__icontains=q).order_by("date_created").all()
            dishes = Dish.objects.filter(Q(dish_method__icontains=q) | Q(dish_name__icontains=q)).order_by("date_created").all()[:10]
            recipes = Recipe.objects.filter(recipe_name__icontains=q).order_by("date_created").all()[:10]
            chefs = Chef.objects.filter(first_name__icontains=q).all()[:10]
            ingredients = Ingredient.objects.filter(ingredient_name__icontains=q).all()[:10]
            return render(request, 'search_results.html',
                          {'dishes': dishes, 'recipes': recipes, 'chefs': chefs,
                          'ingredients': ingredients, 'query': q})
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

class RecipeCategoryList(ListView):
    model = RecipeCategory
    context_object_name = 'all_recipe_categories'

class IngredientList(ListView):
    model = Ingredient
    context_object_name = 'all_ingredients'

class HomePageView(TemplateView):
    template_name = "home.html"
#    def get_context_data(self, **kwargs):
#        context = super(HomePageView, self).get_context_data(**kwargs)
#        context['latest_dishs'] = Dish.objects.filter(dish_status=1, \
#                                                      chef_id__followed_by = self.request.user.id). \
#            order_by("-date_created").all()[:15]
#        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['latest_dishs'])
#        return context
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        dish_list = Dish.objects.filter(dish_status=1, chef_id__followed_by = self.request.user.id).order_by("-date_created").all()
        paginator = Paginator(dish_list, 15) # 15 per page
        page = self.request.GET.get('page')
        try:
            context['page_dishes'] = paginator.page(page)
        except PageNotAnInteger:
            context['page_dishes'] = paginator.page(1)
        except EmptyPage:
            context['page_dishes'] = paginator.page(paginator.num_pages)
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['page_dishes'])
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView,
                        self).get_context_data(**kwargs)
        if (self.object.recipe_id != 1):
            context['dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).order_by("-date_created")
        return context

class RecipeCategoryDetailView(DetailView):
    model = RecipeCategory
    def get_context_data(self, **kwargs):
        context = super(RecipeCategoryDetailView, self).get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(recipecategory_id = self.object.recipecategory_id).order_by("-date_created")
        return context

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


#class DishDetailView(DetailView):
#    model = Dish
#    def get_context_data(self, **kwargs):
#        context = super(DishDetailView, self).get_context_data(**kwargs)
#        exclude = set(string.punctuation)
#        s = ''.join(ch for ch in self.object.dish_name.replace('-', ' ') if ch not in exclude)
#        go_words = [word for word in s.lower().split() if word not in get_stop_words('en')]
#            #+ [word for word in self.object.dish_method.lower().split() if word not in get_stop_words('en')]
#        
#        context['recipe_matcher'] = go_words #self.object.dish_name.split() # <- temporary!
#        #context['recipe_match'] = Recipe.objects.filter(recipe_name__contains=self.object.dish_name.split())
#        #context['recipe_match'] = Recipe.objects.filter(reduce(lambda x, y: x | y, [Q(recipe_name__contains=word) for word in go_words]))
#        context['recipe_match'] = Recipe.objects.filter(reduce(lambda x, y: x | y, [Q(recipe_name__contains=word) for word in go_words]))
#        
#        context['recipe'] = Recipe.objects.get(recipe_id = self.object.recipe_id_id)
#        context['user_chef_like'] = Dish.objects.filter(dish_id = self.object.dish_id, like_chef_id = self.request.user.id)
#        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id = self.object.dish_id)
#        if (self.object.recipe_id_id != 1):
#            context['recipe_dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).exclude(dish_id = self.object.dish_id).order_by("-date_created").all()[:10] # 10 most recent version of the recipe...
#        return context


class DishDetailView(FormMixin, DetailView):
    model = Dish
    form_class = NewCommentForm
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) #reverse('cooklog/dish/', kwargs={'slug': self.object.slug})
    def get_context_data(self, **kwargs):
        context = super(DishDetailView, self).get_context_data(**kwargs)
        
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in self.object.dish_name.replace('-', ' ') if ch not in exclude)
        go_words = [word for word in s.lower().split() if word not in get_stop_words('en')]
        context['recipe_matcher'] = go_words
        context['recipe_match'] = Recipe.objects.filter(reduce(lambda x, y: x | y, [Q(recipe_name__contains=word) for word in go_words]))


        context['add_comment_form'] = NewCommentForm(initial={'dish_id': self.object})
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id = self.object.dish_id)
        
        context['recipe'] = Recipe.objects.get(recipe_id = self.object.recipe_id_id)
        if (self.object.recipe_id_id != 1):
            context['recipe_dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).exclude(dish_id = self.object.dish_id).order_by("-date_created").all()[:10] # 10 most recent version of the recipe...
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        form.save()
        return super(DishDetailView, self).form_valid(form)


class ChefDetailView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefDetailView, self).get_context_data(**kwargs)
        dish_list = Dish.objects.filter(chef_id = self.object.chef_id, dish_status = 1, chef_id__followed_by = self.request.user.id).order_by("-date_created").all()
        paginator = Paginator(dish_list, 6) # 6 per page
        page = self.request.GET.get('page')
        try:
            context['page_dishes'] = paginator.page(page)
        except PageNotAnInteger:
            context['page_dishes'] = paginator.page(1)
        except EmptyPage:
            context['page_dishes'] = paginator.page(paginator.num_pages)

        context['best_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id, chef_id__followed_by = self.request.user.id).order_by("-dish_rating","-date_created").all()[:4]
        context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id, dish_status = 2, chef_id__followed_by = self.request.user.id).order_by("-date_scheduled").all()
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['page_dishes'])
        context['best_chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['best_dishes'])
        context['todo_chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['todo_dishes'])
        return context


class ChefScheduleView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefScheduleView, self).get_context_data(**kwargs)
        context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 2).filter(date_scheduled__gte=datetime.now()).order_by("date_scheduled").all()
        context['archive_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 2).filter(date_scheduled__lt=datetime.now()).order_by("date_scheduled").all()
        return context

class ChefWeekScheduleView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefWeekScheduleView, self).get_context_data(**kwargs)
        context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 2).filter(date_scheduled__range=[datetime.now(),datetime.now()+timedelta(days=6)]).order_by("date_scheduled").all()
        return context

class ChefBriefView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefBriefView, self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).order_by("-date_created").all()
        return context

class ChefAlbumView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefAlbumView, self).get_context_data(**kwargs)
        dish_list = Dish.objects.filter(chef_id = self.object.chef_id, dish_status=1, chef_id__followed_by = self.request.user.id).order_by("-date_created").all()
        paginator = Paginator(dish_list, 12) # 12 per page
        page = self.request.GET.get('page')
        try:
            context['page_dishes'] = paginator.page(page)
        except PageNotAnInteger:
            context['page_dishes'] = paginator.page(1)
        except EmptyPage:
            context['page_dishes'] = paginator.page(paginator.num_pages)
        return context

class HomeAlbumView(TemplateView):
    template_name = "home_album.html"
    def get_context_data(self, **kwargs):
        context = super(HomeAlbumView, self).get_context_data(**kwargs)
        dish_list = Dish.objects.filter(dish_status=1,chef_id__followed_by = self.request.user.id).order_by("-date_created").all()
        paginator = Paginator(dish_list, 12) # 12 per page
        page = self.request.GET.get('page')
        try:
            context['page_dishes'] = paginator.page(page)
        except PageNotAnInteger:
            context['page_dishes'] = paginator.page(1)
        except EmptyPage:
            context['page_dishes'] = paginator.page(paginator.num_pages)
        return context


class IngredientDetailView(DetailView):
    model = Ingredient
    def get_context_data(self, **kwargs):
        context = super(IngredientDetailView, self).get_context_data(**kwargs)
        context['dishes'] = Dish.objects.filter(ingredient_id = self.object.ingredient_id)
        return context

class IngredientAlbumView(TemplateView):
    template_name = "ingredient_album.html"
    def get_context_data(self, **kwargs):
        context = super(IngredientAlbumView, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.order_by("ingredient_name").all()[:30]
        return context

class RecipeCreate(CreateView):
    #model = Recipe
    #fields = ['recipe_name', 'recipe_source', 'recipe_type', 'chef_id', 'date_created']
    #success_url = "/cooklog/recipes/"
    form_class = NewRecipeForm
    template_name = 'cooklog/recipe_form.html'
    def get_initial(self):
        return {'chef_id' : self.request.user.id } #self.request.GET.get('u') }
    def get_success_url(self):
        if self.request.GET.get('next'):
            return '/cooklog/dish/recipe_choose/' + self.request.GET.get('next') + '/?next=' + str(self.object.recipe_id)
        else:
            return '/cooklog/recipe/' + str(self.object.recipe_id) + '/'


class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['recipe_name', 'recipecategory_id', 'recipe_source', 'recipe_method','recipe_comments',
              'recipe_image', 'chef_id', 'date_created']
    def get_success_url(self):
        return '/cooklog/recipe/' + str(self.object.recipe_id) + '/'



class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')

class ChefCreate(CreateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created', 'chef_to_user_id'] #..now! (or default=now)
    def get_success_url(self):
        return '/cooklog/chef/' + str(self.object.chef_id) + '/'

class ChefFollowsUpdate(UpdateView):
    form_class = UpdateChefFollowsForm
    template_name = 'update_chef_follow_form.html'
    def get_queryset(self):
        return ChefFollows.objects.filter(follower_id=self.kwargs.get("pk", None))
    #def get_initial(self):
    #    return {'follower_id' : self.request.user.id }
    #model = ChefFollows
    #fields = ['follower_id', 'chef_id']
    def get_success_url(self):
        return '/cooklog/' # not: chef/' + str(self.request.user.id) + '/'


class ChefUpdate(UpdateView):
    model = Chef
    fields = ['first_name', 'last_name', 'email', 'date_created']

class DishCreate(CreateView):
    form_class = NewDishShortForm
    template_name = 'new_dish_form.html'
    def get_initial(self):
        if self.request.GET.get('next'):
            return {'chef_id' : self.request.user.id , 'recipe_id' : self.request.GET.get('next') }
        else :
            return {'chef_id' : self.request.user.id } 
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'

class DishQuickCreate(CreateView):
    form_class = NewDishQuickForm
    template_name = 'new_dish_quick_form.html'
    def get_initial(self):
        return {'chef_id' : self.request.user.id, 'recipe_id': 1 } # default: None.
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'

class DishTodoCreate(CreateView):
    form_class = NewDishTodoForm
    template_name = 'new_dish_form.html'
    #success_url = '/cooklog/dishes/'
    def get_initial(self):
        return {'chef_id' : self.request.user.id, 'dish_status': 2, 'recipe_id' : self.request.GET.get('next') } #self.request.GET.get('u') }
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'

#class DishWeekTodoCreate(CreateView):
#    form_class = NewDishWeekTodoForm
#    template_name = 'new_dishweek_form.html'
#    #success_url = '/cooklog/dishes/'
#    def get_initial(self):
#        return {'chef_id' : self.request.user.id, 'dish_status': 2 } #self.request.GET.get('u') }
#    def get_success_url(self):
#        return '/cooklog/dish/' + str(self.object.dish_id) + '/'


class DishLongCreate(CreateView):
    form_class = NewDishLongForm
    template_name = 'new_dish_form.html'
    #success_url = '/cooklog/dishes/'
    def get_initial(self):
        return {'chef_id' : self.request.user.id } #self.request.GET.get('u') }
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'

class DishPhotoUpdate(UpdateView):
    template_name = 'update_dish_photo_form.html'
    form_class = UpdateDishPhotoForm
    def get_queryset(self):
        return Dish.objects.filter(dish_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        if self.request.GET.get('next'):
            if (str(self.request.GET.get('next'))=="0"):
                return '/cooklog/'
            else:
                return '/cooklog/chef/' + str(self.request.GET.get('next')) + '/'
        else:
            return '/cooklog/dish/' + str(self.object.dish_id) + '/'

class ChefWeekCountView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefWeekCountView, self).get_context_data(**kwargs)
        context['week_dish'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=7), datetime.now()])
        context['week_rating_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=7), datetime.now()]).values('dish_rating').annotate(Count('dish_id'))
        context['week_recipe_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=7), datetime.now()]).values('recipe_id').annotate(Count('recipe_id'))
#        context['week_dishtype_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=7), datetime.now()]).values('dishtype_id').annotate(Count('dishtype_id'))

        context['month_dish'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=30), datetime.now()])
        context['month_rating_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=30), datetime.now()]).values('dish_rating').annotate(Count('dish_id'))
        context['month_recipe_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=30), datetime.now()]).values('recipe_id').annotate(Count('dish_id'))
#        context['month_dishtype_count'] = Dish.objects.filter(chef_id = self.object.chef_id).filter(dish_status = 1).filter(date_created__range=[datetime.now()-timedelta(days=30), datetime.now()]).values('dishtype_id').annotate(Count('dish_id'))
        return context

class IngredientCreate(CreateView):
    model = Ingredient
    template_name = 'new_ingredient_form.html'
    fields = ['ingredient_name', 'ingredient_type_id', 'ingredient_type_detail',
              'maker_id','ingredient_url','ingredient_image',
              'date_created']
    def get_queryset(self):
        return Ingredient.objects.filter(ingredient_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        return '/cooklog/ingredient/' + str(self.object.ingredient_id) + '/'
#success_url = '/cooklog/ingredients/' # maybe later to that ingredient's page?

class IngredientUpdate(UpdateView):
    model = Ingredient
    template_name = 'update_ingredient_form.html'
    fields = ['ingredient_name', 'ingredient_type_id', 'ingredient_type_detail',
              'maker_id','ingredient_url','ingredient_image',
              'date_created']
    def get_queryset(self):
        return Ingredient.objects.filter(ingredient_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        return '/cooklog/ingredient/' + str(self.object.ingredient_id) + '/'

# def my_image(request):
#     image_data = open("/Users/katiequinn/Documents/parkrun_barcode.png", "rb").read()
#     return HttpResponse(image_data, content_type="image/png")


#class UploadImageView(CreateView):
#    form_class = UploadImageForm
#    template_name = 'upload.html'
#    success_url = '/cooklog/dishes/' # ideally it would be that dish!!

class NewCommentView(CreateView):
    form_class = NewCommentForm #(initial={'chef_id': 3}) #user = request.user) #, initial={'chef_id': user.id})
    template_name = 'new_comment_form.html'
    #success_url = '/cooklog/dishes/'  # ideally goes to that dish!
    def get_initial(self):
        return {'dish_id' : self.request.GET.get('next') , 'chef_id' : self.request.user.id }
    def get_success_url(self):
        return '/cooklog/dish/' + self.request.GET.get('next') + '/'
    def get_context_data(self, **kwargs):
        context = super(NewCommentView, self).get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(dish_id = self.request.GET.get('next'))
        return context

#class NewLikeView(CreateView):
#    form_class = NewLikeForm
#    template_name = 'new_like_form.html'
#    #success_url = '/cooklog/dishes/' # ideally goes to that dish!
#    def get_initial(self):
#        return {'dish_id' : self.request.GET.get('next') , 'chef_id' : self.request.user.id } #self.request.GET.get('u')}
#    def get_form_kwargs(self, **kwargs):
#        kwargs = super(NewLikeView, self).get_form_kwargs()
#        redirect = self.request.GET.get('next')
#        if redirect:
#            if 'initial' in kwargs.keys():
#                kwargs['initial'].update({'next': redirect})
#            else:
#                kwargs['initial'] = {'next': redirect}
#        return kwargs
#    def form_invalid(self, form):
#        import pdb;pdb.set_trace()  # debug example
#        # inspect the errors by typing the variable form.errors
#        # in your command line debugger. See the pdb package for
#        # more useful keystrokes
#        return super(NewLikeView, self).form_invalid(form)
#    def form_valid(self, form):
#        redirect = form.cleaned_data.get('next')   # this necessary as next after submit
#        if redirect:
#            self.success_url = '/cooklog/dish/' + redirect + '/' # hardcodes url, oh well.
#        return super(NewLikeView, self).form_valid(form)
#    def get_context_data(self, **kwargs):
#        context = super(NewLikeView, self).get_context_data(**kwargs)
#        context['dish'] = Dish.objects.get(dish_id = self.request.GET.get('next'))
#        #context['u'] = User.objects.get(id = self.request.GET.get('u'))
#        return context


class CommentDeleteView(DeleteView):
    model = Chef_Dish_Comments
    form_class = CommentDeleteForm
    template_name = 'cooklog/comment_confirm_delete.html'
    #success_url = '/cooklog/dishes/' # later send it back using "next"
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Dish in your model
        #dish_id = self.object.dish_id
        if self.request.GET.get('next'):
            return '/cooklog/dish/' + str(self.request.GET.get('next')) + '/'
        else:
            return '/cooklog/'



class RecipeChooseView(UpdateView): # <- "built" based on NewCommentView
    model = Dish
    form_class = RecipeChooseForm
    template_name = 'recipe_choose_form.html'
    #fields = ['dish_name', 'recipe_id']
    def get_queryset(self):
        return Dish.objects.filter(dish_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) + '/'
    def get_initial(self):
        return {'recipe_id' : self.request.GET.get('next') }

class NewLikeView(UpdateView): # <- "built" based on RecipeChooseView, but uses user..
    model = Dish
    form_class = NewLikeForm
    template_name = 'new_like_form.html'
    def get_queryset(self):
        return Dish.objects.filter(dish_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        if self.request.GET.get('next'):
            if (str(self.request.GET.get('next'))=="0"):    # <- HM MAYBE this is incorrect way to do it?
                return '/cooklog/'
            else:
                return '/cooklog/chef/' + str(self.request.GET.get('next')) + '/'
        else:
            return '/cooklog/dish/' + str(self.object.dish_id) + '/'
    def get_initial(self):
        return {'like_chef_id' : self.request.user.id }

class NewRecipeCategoryView(CreateView):
    model = RecipeCategory
    template_name = 'new_recipe_category_form.html'
    fields = ['recipecategory_name', 'date_created']
    def get_queryset(self):
        return RecipeCategory.objects.filter(recipecategory_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        return '/cooklog/recipecategories/'

class NewBugView(CreateView):
    model = Bugs
    template_name = 'new_bug_form.html'
    fields = ['bug_comment']
    def get_initial(self):
        return {'user_id' : self.request.user.id }
    def get_queryset(self):
        return Bugs.objects.filter(bug_id=self.kwargs.get("pk", None))
    def get_success_url(self):
        return '/cooklog/'


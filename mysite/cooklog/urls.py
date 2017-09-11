"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from cooklog import views
from cooklog.views import ChefList, RecipeList, DishList, IngredientList, RecipeCategoryList
from cooklog.views import HomePageView, RecipeDetailView, DishDetailView, ChefDetailView, IngredientDetailView, RecipeCategoryDetailView
from cooklog.views import ChefScheduleView, ChefWeekScheduleView, ChefBriefView, ChefFeedView
from cooklog.views import ChefAlbumView, ChefWeekCountView, HomeAlbumView, IngredientAlbumView
from cooklog.views import RecipeCreate, RecipeUpdate, RecipeDelete
from cooklog.views import ChefCreate, ChefUpdate, ChefFollowsUpdate
from cooklog.views import DishCreate, DishQuickCreate, DishTodoCreate, DishLongCreate, DishUpdate, DishPhotoUpdate #, DishWeekTodoCreate
from cooklog.views import IngredientCreate, IngredientUpdate #, IngredientDelete
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from cooklog.views import NewCommentView, CommentDeleteView, NewLikeView # UploadImageView, ,
from cooklog.views import RecipeChooseView, NewRecipeCategoryView, NewBugView
from cooklog.views import RecipeAutocomplete
from cooklog.views import NewEntryView, NewEntryDoneView, NewEntryTodoView, DishTodoQuickCreate
from cooklog.views import dish_diagram_view, DishDiagramUpdate, DishDiagramDetailView

urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^login/$', auth_views.login, name='login'),
               url(r'^logout/$', auth_views.logout, {'next_page': '/cooklog/login'}, name='logout'),
               url(r'^register/', CreateView.as_view(template_name='registration/register.html',
                                                     form_class=UserCreationForm,
                                                     success_url='/cooklog/login')),
               
               url(r'^search-form/$', views.search_form),
               url(r'^search/$', views.search, name='search_results'),
               url(r'^chefs/$', ChefList.as_view()),
               url(r'^recipes/$', RecipeList.as_view()),
               url(r'^dishes/$', DishList.as_view()),
               url(r'^recipecategories/$', RecipeCategoryList.as_view()),
               url(r'^ingredients/$', IngredientList.as_view()),
               url(r'^$', HomePageView.as_view(), name='home'),
               url(r'^album/$', HomeAlbumView.as_view(), name='home_album'),
               url(r'^ingredients/album/$', IngredientAlbumView.as_view(), name='ingredient_album'),
               url(r'^recipe/(?P<pk>\d+)/$', RecipeDetailView.as_view(), name='recipe_detail'),
               url(r'^recipecategory/(?P<pk>\d+)/$', RecipeCategoryDetailView.as_view(), name='recipecategory_detail'),
               url(r'^chef/(?P<pk>\d+)/$', ChefDetailView.as_view(), name='chef_detail'),
               url(r'^chef/feed/(?P<pk>\d+)/$', ChefFeedView.as_view(template_name="cooklog/chef_feed.html"), name='chef_feed'),
               url(r'^chef/todo/(?P<pk>\d+)/$', ChefScheduleView.as_view(template_name='cooklog/chef_todo.html'), name='chef_todo'),
               url(r'^chef/weektodo/(?P<pk>\d+)/$', ChefWeekScheduleView.as_view(template_name='cooklog/chef_weektodo.html'), name='chef_weektodo'),
               url(r'^chef/brief/(?P<pk>\d+)/$', ChefBriefView.as_view(template_name='cooklog/chef_brief.html'), name='chef_brief'),
               url(r'^chef/album/(?P<pk>\d+)/$', ChefAlbumView.as_view(template_name='cooklog/chef_album.html'), name='chef_album'),
               url(r'^chef/dishcount/(?P<pk>\d+)/$', ChefWeekCountView.as_view(template_name='cooklog/chef_dishcount.html'), name='chef_dishcount'),
               url(r'^dish/(?P<pk>\d+)/$', DishDetailView.as_view(), name='dish_detail'),
               url(r'^ingredient/(?P<pk>\d+)/$', IngredientDetailView.as_view(), name='ingredient_detail'),
               url(r'^recipe/add/$', RecipeCreate.as_view(), name='recipe_add'),
               url(r'^recipe/add/(?P<pk>[0-9]+)/$', RecipeUpdate.as_view(), name='recipe_update'),
               url(r'^recipe/delete/(?P<pk>[0-9]+)/$', RecipeDelete.as_view(), name='recipe_delete'),
               url(r'^chef/add/$', ChefCreate.as_view(), name='chef_add'),
               url(r'^chef/add/(?P<pk>[0-9]+)/$', ChefUpdate.as_view(), name='chef_update'),
               url(r'^cheffollow/add/(?P<pk>[0-9]+)/$', ChefFollowsUpdate.as_view(), name='chef_follow_update'),
               url(r'^dish/quick/$', DishQuickCreate.as_view(), name='dish_quick_add'),
               url(r'^dish/add/$', DishCreate.as_view(), name='dish_add'),
               url(r'^dish/quick-todo/$', DishTodoQuickCreate.as_view(), name='dish_quick_add_todo'),
               url(r'^dish/add-todo/$', DishTodoCreate.as_view(), name='dish_add_todo'),
               # url(r'^dish/add-weektodo/$', DishWeekTodoCreate.as_view(), name='dish_add_weektodo'),
               url(r'^dish/add-full/$', DishLongCreate.as_view(), name='dish_add_long'),
               url(r'^dish/add/(?P<pk>[0-9]+)/$', DishUpdate.as_view(), name='dish_update'),
               url(r'^dish/add-photo/(?P<pk>[0-9]+)/$', DishPhotoUpdate.as_view(), name='dish_photo_update'),
               url(r'^ingredient/add/$', IngredientCreate.as_view(), name='ingredient_add'),
               url(r'^ingredient/add/(?P<pk>[0-9]+)/$', IngredientUpdate.as_view(), name='ingredient_update'),
               # url(r'^my_image/$', my_image),
               #url(r'^upload/$', UploadImageView.as_view(), name='photo_upload'),
               url(r'^compliments/(?P<pk>[0-9]+)/$', NewLikeView.as_view(), name='new_like'),
               url(r'^comment/$', NewCommentView.as_view(), name='comment_add'),
               url(r'^comment/delete/(?P<pk>[0-9]+)/$', CommentDeleteView.as_view(), name='comment_delete'),
               url(r'^dish/recipe_choose/(?P<pk>[0-9]+)/$', RecipeChooseView.as_view(), name='recipe_choose'),
               url(r'^recipecategory/add/$', NewRecipeCategoryView.as_view(), name='new_recipe_category'),
               url(r'^bug/add/$', NewBugView.as_view(), name='new_bug'),
               url(r'^recipe-autocomplete/$', RecipeAutocomplete.as_view(),name='recipe-autocomplete'),
               url(r'^new/$', NewEntryView.as_view(), name='new_entry'),
               url(r'^new-done/$', NewEntryDoneView.as_view(), name='new_entry_dish'),
               url(r'^new-todo/$', NewEntryTodoView.as_view(), name='new_entry_todo'),
               url(r'^tagsearch/$', views.tagsearch, name='tagsearch_results'),
               url(r'^diagram/dish/(?P<pk>[0-9]+)/$', dish_diagram_view, name='dish_diagram'),
               url(r'^diagram/dish/add/(?P<pk>[0-9]+)/$', DishDiagramUpdate.as_view(), name='dish_diagram_update'),
               url(r'^diagram/save/dish/(?P<pk>[0-9]+)/$', DishDiagramDetailView.as_view(), name='dish_diagram_save'),

    #url(r'^like/$', 'cooklog.views.like', name='like'),
]

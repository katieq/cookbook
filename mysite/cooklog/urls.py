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
from cooklog.views import ChefList, RecipeList, DishList, IngredientList
from cooklog.views import HomePageView, RecipeDetailView, DishDetailView, ChefDetailView, IngredientDetailView
from cooklog.views import RecipeCreate, RecipeUpdate, RecipeDelete
from cooklog.views import ChefCreate, ChefUpdate
from cooklog.views import DishCreate, DishUpdate
from cooklog.views import IngredientCreate, IngredientUpdate #, IngredientDelete
from cooklog.views import my_image, UploadImageView

urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^search-form/$', views.search_form),
               url(r'^search/$', views.search),
               url(r'^chefs/$', ChefList.as_view()),
               url(r'^recipes/$', RecipeList.as_view()),
               url(r'^dishes/$', DishList.as_view()),
               url(r'^ingredients/$', IngredientList.as_view()),
               url(r'^$', HomePageView.as_view(), name='home'),
               url(r'^recipe/(?P<pk>\d+)/$', RecipeDetailView.as_view(), name='recipe-detail'),
               url(r'^chef/(?P<pk>\d+)/$', ChefDetailView.as_view(), name='chef-detail'),
               url(r'^dish/(?P<pk>\d+)/$', DishDetailView.as_view(), name='dish-detail'),
               url(r'^ingredient/(?P<pk>\d+)/$', IngredientDetailView.as_view(), name='ingredient-detail'),
               url(r'^recipe/add/$', RecipeCreate.as_view(), name='recipe_add'),
               url(r'^recipe/add/(?P<pk>[0-9]+)/$', RecipeUpdate.as_view(), name='recipe_update'),
               url(r'^recipe/delete/(?P<pk>[0-9]+)/$', RecipeDelete.as_view(), name='recipe_delete'),
               url(r'^chef/add/$', ChefCreate.as_view(), name='chef_add'),
               url(r'^chef/add/(?P<pk>[0-9]+)/$', ChefUpdate.as_view(), name='chef_update'),
               url(r'^dish/add/$', DishCreate.as_view(), name='dish_add'),
               url(r'^dish/add/(?P<pk>[0-9]+)/$', DishUpdate.as_view(), name='dish_update'),
               url(r'^ingredient/add/$', IngredientCreate.as_view(), name='ingredient_add'),
               url(r'^ingredient/add/(?P<pk>[0-9]+)/$', IngredientUpdate.as_view(), name='ingredient_update'),
               url(r'^my_image/$', my_image),
               url(r'^upload/$', UploadImageView.as_view()),
]

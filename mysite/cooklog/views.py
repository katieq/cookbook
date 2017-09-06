from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from cooklog.models import Dish, Chef, Recipe, Ingredient, Chef_Dish_Comments, ChefFollows, RecipeCategory, Bugs #Dish_Photo
#from cooklog.forms import ChefEntryForm
#from django.views.generic import CreateView
from cooklog.forms import NewDishShortForm, NewDishQuickForm, NewDishTodoForm, NewDishLongForm, NewCommentForm, CommentDeleteForm, NewRecipeForm, UpdateChefFollowsForm, NewLikeForm # UploadImageForm,
from cooklog.forms import RecipeChooseForm, NewDishTodoQuickForm
from cooklog.forms import UpdateDishForm, UpdateDishPhotoForm, UpdateDishMethodForm #, NewDishWeekTodoForm
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
import svgwrite

def generate_diagram_svg_data(pk):

    # need to access the dish's diagram.text in here!
    diagram_text = Dish.objects.filter(dish_id = pk).all()[0].dish_diagram_text
    # great, and now operate on that! develop it in my other project :) then shift function here.

    import svgwrite
    import re


    def get_utensil_path(utensil_name):
        # todo this will come from some saved text? e.g. a single file with a bunch of paths? or multiple files? not sure.
        return{'frying pan': """M1439,551 c-31,0,-50,24,-50,49 c0,27,22,50,50,50 c27,0,50,-20,50,-50 c0,-28,-21,-49,-50,-49 Z M1447,730 c-125,0,-250,-50,-375,-30 c-30,5,-30,0,-37,30 c-59,241,-277,420,-535,420 c-303,0,-550,-247,-550,-550 c0,-303,247,-550,550,-550 c258,0,476,179,535,420 c7,30,7,25,37,30 c125,20,250,-30,375,-30 c177,0,181,260,0,260 Z M1447,730""",
               'cast iron pan': """M1439,551 c-31,0,-50,24,-50,49 c0,27,22,50,50,50 c27,0,50,-20,50,-50 c0,-28,-21,-49,-50,-49 Z M1447,730 c-125,0,-250,-50,-375,-30 c-30,5,-30,0,-37,30 c-59,241,-277,420,-535,420 c-303,0,-550,-247,-550,-550 c0,-303,247,-550,550,-550 c258,0,476,179,535,420 c7,30,7,25,37,30 c125,20,250,-30,375,-30 c177,0,181,260,0,260 Z M1447,730""",
               'mixing bowl': """M95,28.748v3.176c0,1.17-0.948,2.118-2.118,2.118H92.83c-0.755,15.513-9.756,28.86-22.712,35.756v2.888  c0,1.17-0.949,2.118-2.119,2.118H32c-1.169,0-2.118-0.948-2.118-2.118v-2.888C16.926,62.902,7.925,49.556,7.17,34.042H7.118  C5.948,34.042,5,33.094,5,31.924v-3.176c0-1.169,0.948-2.118,2.118-2.118h85.764C94.052,26.63,95,27.579,95,28.748z""",
               'bowl': """M95,28.748v3.176c0,1.17-0.948,2.118-2.118,2.118H92.83c-0.755,15.513-9.756,28.86-22.712,35.756v2.888  c0,1.17-0.949,2.118-2.119,2.118H32c-1.169,0-2.118-0.948-2.118-2.118v-2.888C16.926,62.902,7.925,49.556,7.17,34.042H7.118  C5.948,34.042,5,33.094,5,31.924v-3.176c0-1.169,0.948-2.118,2.118-2.118h85.764C94.052,26.63,95,27.579,95,28.748z""",
               'large mixing bowl': """M95,28.748v3.176c0,1.17-0.948,2.118-2.118,2.118H92.83c-0.755,15.513-9.756,28.86-22.712,35.756v2.888  c0,1.17-0.949,2.118-2.119,2.118H32c-1.169,0-2.118-0.948-2.118-2.118v-2.888C16.926,62.902,7.925,49.556,7.17,34.042H7.118  C5.948,34.042,5,33.094,5,31.924v-3.176c0-1.169,0.948-2.118,2.118-2.118h85.764C94.052,26.63,95,27.579,95,28.748z""",
               'food processor': """M17,9.4V5h1V3h-5V2h-2v1H6v2h1v4.4c0,2.1,1.2,3.8,3,4.6v1H8.3c-0.4,0-0.8,0.3-0.9,0.7L6,19.8C5.9,20.4,6.4,21,7,21h0v1h2v-1  h6v1h2v-1c0.6,0,1.1-0.6,1-1.2l-1.4-4.1c-0.1-0.4-0.5-0.7-0.9-0.7H14v-1.1C15.8,13.2,17,11.4,17,9.4z M15,18c0,0.6-0.4,1-1,1  c-0.6,0-1-0.4-1-1c0-0.6,0.4-1,1-1C14.6,17,15,17.4,15,18z""",
               'saucepan': "M83.323,35.077l-3.285,3.67v-6.859h3.188v-3.477h-66.55v3.477h3.283v6.859l-3.283-3.67H6.631v6.47h10.046l3.283,3.766  v20.479c0,3.199,2.595,5.795,5.795,5.795h48.489c3.201,0,5.795-2.596,5.795-5.795V45.314l3.285-3.766h10.046v-6.47H83.323z",
               'oven': "M50,0 l1100,0 c50,0,50,0,50,50 l0,1100 c0,50,0,50,-50,50 l-1100,0 c-50,0,-50,0,-50,-50 l0,-1100 c0,-50,0,-50,50,-50 Z M301,230 c-51,0,-51,0,-51,51 l0,198 c0,51,0,51,51,51 l598,0 c51,0,51,0,51,-51 l0,-198 c0,-51,0,-51,-51,-51 Z M233,957 c-36,0,-62,26,-62,61 c0,37,29,62,62,62 c35,0,62,-29,62,-62 c0,-31,-24,-61,-62,-61 Z M0,750 l0,100 l1200,0 l0,-100 Z M472,955 c-35,1,-61,28,-62,63 c1,35,27,61,62,62 c36,-1,63,-27,63,-62 c0,-35,-27,-62,-63,-63 Z M728,955 c-36,1,-63,28,-63,63 c0,35,27,61,63,62 c35,-1,61,-27,62,-62 c-1,-35,-27,-62,-62,-63 Z M967,957 c-38,0,-62,30,-62,61 c0,33,27,62,62,62 c33,0,62,-25,62,-62 c0,-35,-26,-61,-62,-61 Z M967,957 ",
               'rolling pin': "M97.018,97.018c-3.031,3.031-5.805,5.172-11.853-0.876c-2.581-2.581-5.34-6.235-7.421-9.813l-5.227,5.228   c-0.904,0.903-2.368,0.903-3.271,0L8.444,30.755c-0.903-0.904-0.903-2.369,0-3.272l5.228-5.227   c-3.578-2.081-7.232-4.839-9.813-7.42C-2.189,8.787-0.048,6.014,2.983,2.983c3.031-3.031,5.804-5.172,11.852,0.876   c2.581,2.581,5.34,6.235,7.42,9.813l5.227-5.227c0.904-0.904,2.368-0.904,3.272,0l60.802,60.802c0.902,0.903,0.902,2.368,0,3.271   l-5.229,5.227c3.578,2.081,7.232,4.84,9.813,7.421C102.189,91.213,100.048,93.986,97.018,97.018z",
               'pie dish': "M5,44.6V46h0.9l5.5,13.3h0v1.4h77.3v-1.4L94.3,46h1.1v-1.4H5z M14.7,59.3L9.9,46h1.4l4.8,13.3H14.7z M20.4,59.3L17.1,46h1.4  l3.2,13.3H20.4z M26,59.3L24.3,46h1.3l1.8,13.3H26z M31.5,59.3l-1-13.3h1.4l0.8,13.3H31.5z M38.4,59.3H37V46h1.4V59.3z M44.7,59.3  h-1.3V46h1.3V59.3z M50.6,59.3h-1.1V46h1.1V59.3z M56.8,59.3h-1.2V46h1.2V59.3z M61.7,46h1.3v13.3h-1.3V46z M68.6,59.3h-1.2L68.3,46  h1.4L68.6,59.3z M74.2,59.3h-1.3L74.6,46h1.3L74.2,59.3z M79.7,59.3h-1.4L81.6,46H83L79.7,59.3z M85.4,59.3H84L88.8,46h1.4  L85.4,59.3z",
               'baking dish': "M82.634,39.488h-3.774v-1.582c2.605-0.024,4.72-2.15,4.72-4.761c0-2.625-2.14-4.762-4.765-4.762H11.185  c-2.627,0-4.762,2.136-4.762,4.762c0,2.611,2.112,4.737,4.718,4.761v1.582H7.364c-1.429,0-2.59,1.161-2.59,2.59  c0,1.429,1.161,2.59,2.59,2.59h3.776v8.382c0.022,4.724,3.881,8.565,8.604,8.565h50.511c4.724,0,8.582-3.842,8.604-8.574v-8.374  h3.773c1.432,0,2.592-1.161,2.592-2.59C85.227,40.649,84.064,39.488,82.634,39.488z M11.184,34.302c-0.638,0-1.157-0.52-1.157-1.156  c0-0.637,0.519-1.156,1.157-1.156h67.63c0.637,0,1.158,0.52,1.158,1.156s-0.521,1.156-1.158,1.156h-3.562v0.066H14.746v-0.066  H11.184z M70.255,58.011H19.744c-2.743,0-4.985-2.233-4.998-4.969V35.81h60.508v17.223C75.24,55.777,72.998,58.011,70.255,58.011z",
               'baking sheet': "M33.585,70.741C33.585,70.741,33.585,70.741,33.585,70.741c-2.987,0-5.368-0.757-5.468-0.789l-0.106-0.041    C9.845,61.669,4.525,53.867,1.969,50.118c-0.932-1.367-1.185-2.628-0.788-3.805c0.68-2.017,2.999-2.842,3.261-2.929    c2.195-0.777,54.187-19.173,56.667-20c0.84-0.28,1.829-0.422,2.939-0.422c1.831,0,3.387,0.384,3.452,0.4    c11.348,3.779,21.2,9.825,29.357,17.99l0.107,0.107c1.081,1.081,1.169,2.121,1.053,2.804c-0.338,1.977-2.723,3.174-2.993,3.304    c-0.583,0.234-52.126,20.719-56.586,22.37C37,70.471,35.367,70.741,33.585,70.741z M28.78,68.063    c0.338,0.101,2.368,0.678,4.805,0.678c0,0,0,0,0,0c1.544,0,2.943-0.229,4.159-0.679c4.438-1.645,55.958-22.119,56.479-22.326    c0.495-0.243,1.696-1.053,1.823-1.812c0.02-0.118,0.08-0.476-0.495-1.051l-0.107-0.107c-7.936-7.943-17.524-13.825-28.5-17.484    l0,0c-0.014,0-1.362-0.32-2.896-0.32c-0.896,0-1.672,0.107-2.307,0.319c-2.463,0.821-56.108,19.802-56.65,19.994    c-0.467,0.16-1.711,0.764-2.017,1.682c-0.183,0.549-0.011,1.215,0.51,1.979C6.072,52.586,11.17,60.062,28.78,68.063z",
               'wok': "M23,8.25c-0.05,0-0.1,0.007-0.147,0.022l-6.051,1.862C15.936,8.845,12.358,8.25,9,8.25c-2.357,0-4.818,0.294-6.379,0.914    L1.853,8.396c-0.195-0.195-0.512-0.195-0.707,0l-1,1c-0.168,0.168-0.195,0.433-0.063,0.631l1,1.5    c0.006,0.009,0.017,0.012,0.023,0.021c0.596,2.41,3.843,4.202,7.893,4.202c3.964,0,7.164-1.716,7.857-4.049L23,10.75    c0.561,0,1-0.549,1-1.25S23.561,8.25,23,8.25z M1.286,10.028L1.143,9.814L1.5,9.457l0.191,0.191    C1.526,9.766,1.395,9.894,1.286,10.028z M9,12.25c-4.618,0-7-1.051-7-1.5c0-0.449,2.382-1.5,7-1.5s7,1.051,7,1.5    C16,11.199,13.618,12.25,9,12.25z",
               'muffin tray': "M80.447,27.832c0-1.661-1.123-3.007-2.512-3.007H12.063c-1.388,0-2.513,1.346-2.513,3.007L3.697,55.034h82.604  L80.447,27.832z M44.999,30.041c4.506,0,8.157,1.721,8.157,3.845c0,2.125-3.651,3.847-8.157,3.847c-4.505,0-8.156-1.722-8.156-3.847  C36.843,31.762,40.494,30.041,44.999,30.041z M20.745,51.331c-5.056,0-9.151-1.93-9.151-4.312c0-2.384,4.096-4.314,9.151-4.314  c5.052,0,9.149,1.931,9.149,4.314C29.895,49.401,25.797,51.331,20.745,51.331z M23.375,37.732c-4.507,0-8.159-1.722-8.159-3.847  c0-2.124,3.652-3.845,8.159-3.845c4.503,0,8.155,1.721,8.155,3.845C31.53,36.011,27.878,37.732,23.375,37.732z M44.999,51.331  c-5.053,0-9.149-1.93-9.149-4.312c0-2.384,4.097-4.314,9.149-4.314s9.15,1.931,9.15,4.314  C54.149,49.401,50.052,51.331,44.999,51.331z M58.468,33.886c0-2.124,3.652-3.845,8.159-3.845c4.505,0,8.156,1.721,8.156,3.845  c0,2.125-3.651,3.847-8.156,3.847C62.12,37.732,58.468,36.011,58.468,33.886z M69.256,51.331c-5.054,0-9.149-1.93-9.149-4.312  c0-2.384,4.096-4.314,9.149-4.314c5.053,0,9.149,1.931,9.149,4.314C78.405,49.401,74.309,51.331,69.256,51.331z",
               'stand mixer': "M90.267,47.177c-0.331-0.322-0.785-0.53-1.286-0.53H66.774v-8.402c0.422-0.119,0.829-0.27,1.211-0.469  c1.69-0.845,2.949-2.402,3.42-4.273c2.363-0.575,4.482-1.776,6.151-3.445c1.258-1.239,2.279-2.743,2.951-4.426h1.977  c1.352,0,2.582-0.549,3.462-1.428c0.889-0.889,1.438-2.109,1.438-3.462c0-2.714-2.194-4.899-4.899-4.899h-1.977  C78.559,11,73.83,7.585,68.297,7.585H23.4c-1.069,0-2.109,0.123-3.102,0.369c-1.825,0.445-3.509,1.267-4.956,2.383  c-0.435,0.341-0.861,0.709-1.248,1.097c-2.374,2.383-3.849,5.665-3.849,9.307c0,6.195,4.284,11.387,10.054,12.778  c0.93,0.23,1.902,0.348,2.899,0.363l-0.024,0.006c0,0,0,4.389,0,11.927c0,11.889-3.518,26.303-5.552,31.609  c-2.346,6.138-8.418,9.609-8.418,9.609c0,1.192,0.388,2.289,1.04,3.178c0.17,0.218,0.35,0.435,0.539,0.624  c0.974,0.974,2.317,1.58,3.802,1.58h68.637c1.315,0,2.412-0.946,2.639-2.204c0.028-0.161,0.047-0.322,0.047-0.492  c0-0.738-0.303-1.419-0.785-1.901c-0.492-0.482-1.154-0.785-1.901-0.785h-8.495c0.69,0,1.249-0.558,1.249-1.249  c0-0.69-0.558-1.248-1.249-1.248h-0.454v-2.252c0.66-0.264,1.309-0.551,1.939-0.87c0.861-0.426,1.693-0.908,2.487-1.438  c2.242-1.485,4.218-3.339,5.855-5.457c3.159-4.105,5.032-9.25,5.032-14.83v-9.531c0.704-0.25,1.211-0.914,1.211-1.695  C90.797,47.962,90.589,47.508,90.267,47.177z M56.91,16.504c0.823,0,1.561,0.397,2.005,1.021c0.312,0.416,0.492,0.927,0.492,1.475  c0,1.381-1.125,2.497-2.497,2.497c-1.201,0-2.204-0.851-2.45-1.986c-0.028-0.161-0.047-0.331-0.047-0.511  C54.413,17.62,55.529,16.504,56.91,16.504z M44.255,16.504c1.248,0,2.289,0.917,2.469,2.119c0.019,0.123,0.028,0.246,0.028,0.378  c0,1.381-1.116,2.497-2.497,2.497c-1.145,0-2.109-0.776-2.393-1.825c-0.066-0.218-0.095-0.435-0.095-0.672  C41.767,17.62,42.883,16.504,44.255,16.504z M63.246,46.647H41c-1.003,0-1.807,0.813-1.807,1.816c0,0.492,0.199,0.946,0.53,1.277  c0.185,0.19,0.416,0.33,0.672,0.42v9.53c0,6.725,2.724,12.797,7.122,17.204c2.314,2.314,5.097,4.158,8.191,5.393v2.25h-0.454  c-0.69,0-1.248,0.558-1.248,1.248c0,0.69,0.558,1.249,1.248,1.249h-3.044c-8.399-7.415-12.305-15.861-13.998-20.789  c-0.794-2.298-1.163-4.719-1.163-7.15V42.542c0-4.665,4.07-7.313,7.167-8.654h14.507c0.67,2.113,2.376,3.763,4.524,4.359V46.647z",
               }.get(
            utensil_name, " M 0 0 L 10 5 L 0 10 z ")


    def get_utensil_scale(utensil_name):
        return{'frying pan': 0.04,
               'cast iron pan': .04,
               'mixing bowl': .4,
               'bowl': .4,
               'large mixing bowl': .5,
               'food processor': 1.7,
               'saucepan': .7,
               'oven': .025,
               'rolling pin': .4,
               'pie dish': .7,
               'baking dish': .7,
               'wok': 2,
               'muffin tray': .8,
               'stand mixer': .5,
               }.get(utensil_name, 1)


    def get_ingr_path(ingr_name):
        return{
            'eggs': "M76.827,28.042C67.207,5.262,50.697,5,49.999,5c-0.697,0-17.206,0.262-26.827,23.042   c-6.704,15.875-9.592,39.551-0.088,54.015C28.728,90.646,37.783,95,49.999,95c12.217,0,21.273-4.354,26.916-12.943   C86.419,67.592,83.532,43.917,76.827,28.042z M28.855,63.764c-0.708-2.608-1.043-5.547-0.994-8.733l3.886,0.059   c-0.042,2.819,0.246,5.391,0.858,7.643L28.855,63.764z M32.111,50.255l-3.854-0.51c1.717-13.154,4.789-19.381,9.86-26.27   l3.122,2.33C36.451,32.31,33.726,37.876,32.111,50.255z",
            'butternut pumpkin': "M73.56,73.419c0-5.073-1.603-9.905-4.639-13.997c-0.068-0.153-0.166-0.291-0.285-0.406  c-1.222-1.643-1.865-3.566-1.865-5.575l-0.009-1.169c-0.032-4.14-0.132-16.738,0.009-24.218c0-6.94-5.629-12.595-12.613-12.776  V8.948c0-0.715-0.58-1.295-1.296-1.295h-7.673c-0.411,0-0.797,0.194-1.041,0.524c-0.244,0.33-0.318,0.756-0.198,1.149l1.825,5.996  c-6.81,0.613-12.545,6.297-12.545,12.756c0.139,7.457,0.041,20.055,0.008,24.194l-0.008,1.169c0,2.067-0.682,4.045-1.973,5.719  c-0.044,0.058-0.083,0.118-0.116,0.182c-3.075,4.109-4.699,8.973-4.699,14.078c0,11.85,8.807,18.926,23.559,18.929  c0.838,0,1.651-0.03,2.45-0.075c0.134,0.045,0.271,0.075,0.412,0.075c0.197,0,0.39-0.063,0.573-0.154  C66.1,91.156,73.56,84.313,73.56,73.419z M51.565,10.244v5.017h-3.102l-1.527-5.017H51.565z M56.083,89.249  c1.752-2.637,3.762-7.214,3.47-14.189c-0.03-0.716-0.642-1.24-1.35-1.24c-0.715,0.03-1.27,0.635-1.24,1.35  c0.373,8.878-3.288,13.284-4.517,14.506c-0.899,0.059-1.729,0.081-2.446,0.081l-0.001,1.296v-1.296  c-6.304-0.001-20.967-1.595-20.967-16.337c0-4.606,1.487-8.992,4.301-12.684c0.042-0.056,0.08-0.114,0.112-0.175  c1.554-2.093,2.375-4.55,2.375-7.12l0.008-1.148c0.033-4.148,0.131-16.772-0.008-24.239c0-3.41,2.055-6.556,5.055-8.428  c-0.544,1.581-0.764,3.682-0.764,6.477c0,0.801,0.014,1.66,0.028,2.561c0.012,0.742,0.024,1.513,0.03,2.303  c0.004,0.712,0.583,1.287,1.295,1.287c0.003,0,0.006,0,0.009,0c0.715-0.005,1.292-0.588,1.287-1.304  c-0.005-0.799-0.018-1.578-0.03-2.327c-0.014-0.886-0.028-1.731-0.028-2.52c0-7.422,1.653-7.791,4.395-8.251H47.5  c0.001,0,0.002,0,0.003,0s0.002,0,0.003,0h6.309c5.715,0,10.363,4.577,10.364,10.178c-0.141,7.491-0.042,20.115-0.009,24.263  l0.008,1.148c0,2.569,0.82,5.025,2.374,7.118c0.033,0.062,0.071,0.121,0.114,0.177c2.813,3.69,4.301,8.076,4.301,12.684  C70.968,84.396,62.838,88.082,56.083,89.249z",
            # 'butter': "",
            # 'flour': "", # got a cool wheat grain, but it was very slow. perhaps wouldn't be in practice though?
        }.get(ingr_name, " M 0 0 L 10 5 L 0 10 z ")

    def get_ingr_scale(ingr_name):
        return{
            'eggs': .3,
            'butternut pumpkin': .4,
            # 'butter': 1,
            # 'flour': .3,
        }.get(ingr_name, .01)

    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
    ingr_index = find(diagram_text,'|')[0::2]
    action_index = find(diagram_text,'/')[0::2]
    branch_open_index = find(diagram_text,'[')

    if len(branch_open_index)>0:
        def is_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        branch_number = list()
        for i in branch_open_index:
            if is_int(diagram_text[i+1]):
                branch_number.append(int(diagram_text[i+1]))
            else:
                branch_number.append(0)
        # Fill in elements that are zero (not assigned by user) with counts, starting at max (there's probably a python way to do it, but use this for now)
        k = max(branch_number)
        for i in range(len(branch_number)):
            if branch_number[i] == 0:
                k += 1
                branch_number[i] = k
        #branch_number = [int(diagram_text[i+1]) for i in branch_open_index]

    branch_close_index_raw = find(diagram_text, ']')
    branch_close_index = list()
    for b_i in branch_open_index[-1::-1]:
      branch_close = branch_close_index_raw[next(x[0] for x in enumerate(branch_close_index_raw) if x[1] > b_i)]
      branch_close_index.append(branch_close)
      branch_close_index_raw.remove(branch_close)
    branch_close_index = list(reversed(branch_close_index))

    ingr2action = list()
    for ingr_index_i in ingr_index:
        ingr2action.append(next(x[0] for x in enumerate(action_index) if x[1] > ingr_index_i))

    action_in_branch = list()
    for action_i in action_index:
        b = 0
        for i in range(len(branch_open_index)):
            if branch_open_index[i] < action_i and branch_close_index[i] > action_i:
                if branch_number[i]>0:
                    b = branch_number[i]
                else:
                    b = i+1 # because want "first" branch =1 not 0 .. but check this works when sometimes assign a branch_number!
        action_in_branch.append(b)
    action2action = list()
    for i in range(len(action_in_branch)-1):
        if action_in_branch[i] in action_in_branch[i+1:]: # is not last occurrence of action_in_branch[i] value:
            action2action.append(i + 1 + next(x[0] for x in enumerate(action_in_branch[i+1:]) if x[1] == action_in_branch[i])) #index of next occurrence of action_in_branch[i])
        else:
            action2action.append(i + 1 + next(x[0] for x in enumerate(action_in_branch[i+1:]) if x[1] < action_in_branch[i]))


    ingr = re.findall('\|(.*?)\|', diagram_text)  # keeps [] '\[[^\[\]]*\]'
    ingr = [s.strip('->').strip() for s in ingr]
    ingr = [s.split(' + ') for s in ingr]

    line_per_ingr = [len(ingr[i])-1 for i in range(len(ingr))]

    action = re.findall('\/(.*?)\/', diagram_text)

    utensil = re.findall('in(.*?)\{', diagram_text)
    utensil = [s.strip() for s in utensil]
    # need to get number of "/" between each set of "{ .. }" e.g. [2,1,1] and use that for height_utensil
    utensil_index = find(diagram_text,'{')
    utensil_close_index_raw = find(diagram_text, '}')
    utensil_close_index = list() # this code copied from branch_close_index .. should allow for nested utensils.
    for u_i in utensil_index[-1::-1]:
      utensil_close = utensil_close_index_raw[next(x[0] for x in enumerate(utensil_close_index_raw) if x[1] > u_i)]
      utensil_close_index.append(utensil_close)
      utensil_close_index_raw.remove(utensil_close)
    utensil_close_index = list(reversed(utensil_close_index))

    if len(utensil_index) > 0:
        action_in_utensil = list()
        for action_i in action_index:
            u = 0
            for i in range(len(utensil_index)):
                if utensil_index[i] < action_i and utensil_close_index[i] > action_i:
                    u = i + 1  # because want "first"=1 not 0
            action_in_utensil.append(u)
    else:
        action_in_utensil = [0 for i in range(len(action))]

    branch_to_y_delta = {0: 50, 1: 30, 2: 30, 3: 40, 4: 40}
    y_delta = [branch_to_y_delta[action_in_branch[i]] for i in range(len(action))]
    y_action = [sum(y_delta[:i+1]) for i in range(len(action))]
    x_action = [230 - (action_in_branch[i]>0)*50 - (action_in_branch[i]>2)*30
                # - (action_in_utensil[i]==0 and i != 0 and (i != len(action)-1))*60 # <- remove for now. not sure if do want this
                for i in range(len(action))] # todo not sure always works

    height_ingr = [16*i for i in line_per_ingr]
    # attempt to align with action, but put it lower if heigh_ingr makes it necessary:
    # todo oh wait, should use middle_y_ingr[i-1] instead of sum(height_ingr[0:i]) for cases where only gets crowded "midway"
    middle_y_ingr = list()
    middle_y_ingr.append(max(y_action[ingr2action[0]]-25, .5*height_ingr[0] + 20))
    for i in range(1, len(height_ingr)):
        middle_y_ingr.append(max(y_action[ingr2action[i]]-25, middle_y_ingr[i-1] + .5*height_ingr[i-1] + .5*height_ingr[i] + 15))
    # middle_y_ingr = [max(y_action[ingr2action[i]]-25, sum(height_ingr[0:i]) + .5*height_ingr[i]  + (i+1)*20) for i in range(len(height_ingr))]
    y_ingr = [max(10,10 + middle_y_ingr[i] - .5*height_ingr[i]) for i in range(len(ingr))]

    # height utensil and y _utensil should just come from y_action and action_per_utensil
    y_utensil = [-23 + min([y_action[i] for i in range(len(y_action)) if action_in_utensil[i]==(j+1)]) for j in range(len(utensil_index))]
    height_utensil = [26 + \
                      max([y_action[i] for i in range(len(y_action)) if action_in_utensil[i] == (j + 1)]) -
                      min([y_action[i] for i in range(len(y_action)) if action_in_utensil[i] == (j + 1)])
                      for j in range(len(utensil_index))]
    x_utensil = [340 - 5*len(utensil[i]) for i in range(len(utensil_index))]

    # want: if x1 far from x2, then make x1_a2a further from (more positive) x1
    x1_a2a = [x_action[i]+10 + 5*(x_action[action2action[i]]!=x_action[i]) for i in range(len(action2action))]
    # want: if x1 far from x2, make x2_a2a further from (more negative) x2
    x2_a2a = [x_action[action2action[i]] + 10 - 7/30*(x_action[action2action[i]]-x_action[i]) for i in range(len(action2action))]
    # want: fine as is.
    y1_a2a = [y_action[i] + 5 for i in range(len(action2action))]
    # if y1 closer to y2, then make it get closer to y2
    y2_a2a = [y_action[action2action[i]] - 8 - 5/50*min(100, y_action[action2action[i]]-y_action[i]) for i in range(len(action2action))] # "min(100" puts max on y-gap, for distant action2action


    x1_i2a = [50 + 4*len(max(ingr[i], key=len)) for i in range(len(ingr2action))] # based on longest string within ingr block
    x2_i2a = [x_action[ingr2action[i]]-10 for i in range(len(ingr2action))]
    y1_i2a = [y_ingr[i] +10 + line_per_ingr[i]*7 for i in range(len(ingr2action))]
    y2_i2a = [y_action[ingr2action[i]]-5 for i in range(len(ingr2action))]

    dwg = svgwrite.Drawing(filename="test-svgwrite.svg",
                           size=("600px", max(y_action + middle_y_ingr)+50))

    marker = dwg.marker(viewBox="0 0 10 10", refX="0", refY="5",
                        markerUnits="strokeWidth", markerWidth="4", markerHeight="3",
                        orient="auto", fill="#696969")
    marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z"))
    dwg.defs.add(marker)


    for i in range(len(utensil)):
        dwg.add(dwg.rect(insert=(50+150, y_utensil[i]), size=("200px", height_utensil[i]),
                         fill="#FDC08E", style="opacity: .3", rx=5, ry=5))
        dwg.add(dwg.path(d=get_utensil_path(utensil[i]),
                         transform="translate(" + str(50+350) + "," + str(y_utensil[i] - 10) + ") scale("+str(get_utensil_scale(utensil[i]))+")",
                         style="opacity: .5", fill="#ff9900"))
        dwg.add(dwg.text(utensil[i],
                         insert=(50+x_utensil[i], y_utensil[i] + 10), fill="#545454",
                         style="font-size: 12; font-family: Arial"))

    for i in range(len(ingr2action)):
        line = dwg.add(dwg.line(start=(50+x1_i2a[i], y1_i2a[i]), end=(50+x2_i2a[i], y2_i2a[i]),
                                stroke='#696969', stroke_width=2, marker_end=marker.get_funciri()))

    for i in range(len(action2action)):
        line = dwg.add(dwg.line(start=(50+x1_a2a[i], y1_a2a[i]), end=(50+x2_a2a[i], y2_a2a[i]),
                                stroke='#696969', stroke_width=2, marker_end=marker.get_funciri()))

    for i in range(len(ingr)):  # need to use tspan for multiple line
        for j in range(len(ingr[i])):
            ingr_name = ingr[i][j][:ingr[i][j].find('(')].strip()
            dwg.add(dwg.path(d=get_ingr_path(ingr_name), # todo: until '('
                             transform="translate(" + str(45-(j%3)*20) + "," + str(-15+y_ingr[i]+12*1.05*(j+1)) + ") scale(" + str(
                                 get_ingr_scale(ingr_name)) + ")",
                             style="opacity: .5", fill="#B1654B"))
            dwg.add(dwg.text(ingr[i][j],
                             insert=(50+30, y_ingr[i]+12*1.05*(j+1)), fill="#B1654B", style="font-size: 12; font-family: Arial"))
        # paragraph = dwg.add(dwg.g(font_size=12, fill = "#B1654B", style="font-family: Arial"))
        # atext = dwg.text("", insert=(50+30, y_ingr[i]), fill="#B1654B", style="font-size: 12; font-family: Arial")
        # for ingr_j in ingr[i]:
        #     atext.add(dwg.tspan(ingr_j, dx='0', dy=['1.05em']))
        # dwg.add(atext)

    for i in range(len(action)):
        dwg.add(dwg.text(action[i],
                         insert=(50+x_action[i], y_action[i]), fill="#E75481",
                         style="font-size: 12px; font-family: Arial; font-weight=bold"))

    return dwg.tostring()


def dish_diagram_view(request, pk): # <- probably this ends up existing for each dish, so dish_id may be input and in url like the stack-overflow example
    svg_data = generate_diagram_svg_data(pk)
    return HttpResponse(svg_data, content_type="image/svg+xml")

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

# Create your views here. 8/26: I forget when I entered this and what it does! For a table!?
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
            if 'ch' in request.GET:
                ch = request.GET['ch']
                recipe_categories = RecipeCategory.objects.filter(recipecategory_name__icontains=q).all()
                recipes = Recipe.objects.filter(
                    Q(recipe_name__icontains=q) | Q(recipecategory_id__in=recipe_categories)).order_by(
                    "-date_created").all()
                dishes_all = Dish.objects.filter(chef_id=ch).filter(
                    Q(dish_method__icontains=q) | Q(dish_name__icontains=q) |
                    Q(tags__name=q) | Q(recipe_id__in=recipes)).distinct().order_by(
                    "-date_created").all()
                chefs = Chef.objects.filter(chef_id=ch).all()

                paginator = Paginator(dishes_all, 12)  # 15 per page
                page = request.GET.get('page')
                try:
                    dishes = paginator.page(page)
                except PageNotAnInteger:
                    dishes = paginator.page(1)
                except EmptyPage:
                    dishes = paginator.page(paginator.num_pages)

                return render(request, 'search_results.html',
                              {'dishes': dishes, 'query': q, 'chefs': chefs})
            else:
                # todo get dishes with recipe_category__icontains=q .. I think this below works.
                recipe_categories = RecipeCategory.objects.filter(recipecategory_name__icontains=q).all()
                recipes = Recipe.objects.filter(
                    Q(recipe_name__icontains=q) | Q(recipecategory_id__in=recipe_categories)).order_by(
                    "-date_created").all()[:12]
                dishes = Dish.objects.filter(
                    Q(dish_method__icontains=q) | Q(dish_name__icontains=q) | Q(tags__name=q) |
                    Q(recipe_id__in=recipes)).distinct().order_by(
                    "-date_created").all()[:12]
                chefs = Chef.objects.filter(first_name__icontains=q).all()[:12]
                ingredients = Ingredient.objects.filter(ingredient_name__icontains=q).all()[:12]
                return render(request, 'search_results.html',
                              {'dishes': dishes, 'recipes': recipes, 'chefs': chefs,
                               'ingredients': ingredients, 'query': q})
    return render(request, 'search_form.html', {'errors': errors})


def tagsearch(request):
    q = request.GET['q']
    dishes = Dish.objects.filter(tags__name=q).order_by("-date_created").all()
    recipes = Recipe.objects.filter(tags__name=q).order_by("-date_created").all()
    return render(request, 'tagsearch_results.html', {'dishes': dishes, 'recipes': recipes})

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
        # context['dish_diagram'] = reverse('dish_diagram', args=[1]) # ugh .. how to get this for each dish! probs can't?
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView,
                        self).get_context_data(**kwargs)
        if (self.object.recipe_id != 1):
            context['dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).order_by("-date_created")
            context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['dishes'])
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
    form_class = NewCommentForm # not needed??? form_class = NewCommentForm #UpdateDishForm
    def get_success_url(self):
        return '/cooklog/dish/' + str(self.object.dish_id) #reverse('cooklog/dish/', kwargs={'slug': self.object.slug})
    def get_context_data(self, **kwargs):
        context = super(DishDetailView, self).get_context_data(**kwargs)

        # only if dish name not empty: removes stop words and single letter words (e.g. "w" for with)
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in self.object.dish_name.replace('-', ' ') if ch not in exclude)
        go_words = [word for word in s.lower().split() if word not in get_stop_words('en') and len(word)>1]
        if len(go_words) > 0:
            context['recipe_matcher'] = go_words
            context['recipe_match'] = Recipe.objects.filter(reduce(lambda x, y: x | y, [Q(recipe_name__contains=word) for word in go_words]))

        # context['dish_update_method_on_dish_detail_form'] = UpdateDishMethodForm(initial={'dish_id': self.object, 'dish_method': self.object.dish_method})
        context['add_comment_form'] = NewCommentForm(initial={'dish_id': self.object})
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id = self.object.dish_id)
        
        context['recipe'] = Recipe.objects.get(recipe_id = self.object.recipe_id_id)
        if self.object.recipe_id_id != 1:
            context['recipe_dishes'] = Dish.objects.filter(dish_status = 1).filter(recipe_id = self.object.recipe_id).exclude(dish_id = self.object.dish_id).order_by("-date_created").all()[:10] # 10 most recent version of the recipe...

        context['dish_diagram'] = reverse('dish_diagram', args=[self.object.dish_id])
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
        context['week_dish'] = Dish.objects.filter(chef_id=self.object.chef_id).filter(dish_status=1).filter(
            date_created__range=[datetime.now() - timedelta(days=7), datetime.now()])
        context['month_dish'] = Dish.objects.filter(chef_id=self.object.chef_id).filter(dish_status=1).filter(
            date_created__range=[datetime.now() - timedelta(days=31), datetime.now()])
        context['best_dishes'] = Dish.objects.filter(chef_id=self.object.chef_id,
                                                     chef_id__followed_by=self.request.user.id).order_by("-dish_rating",
                                                                                                         "-date_created").all()[:3]
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['best_dishes'])
        return context

class ChefFeedView(DetailView):
    model = Chef
    def get_context_data(self, **kwargs):
        context = super(ChefFeedView, self).get_context_data(**kwargs)
        dish_list = Dish.objects.filter(chef_id = self.object.chef_id, dish_status = 1, chef_id__followed_by = self.request.user.id).order_by("-date_created").all()
        paginator = Paginator(dish_list, 6) # 6 per page
        page = self.request.GET.get('page')
        try:
            context['page_dishes'] = paginator.page(page)
        except PageNotAnInteger:
            context['page_dishes'] = paginator.page(1)
        except EmptyPage:
            context['page_dishes'] = paginator.page(paginator.num_pages)

        # context['best_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id, chef_id__followed_by = self.request.user.id).order_by("-dish_rating","-date_created").all()[:4]
        # context['todo_dishes'] = Dish.objects.filter(chef_id = self.object.chef_id, dish_status = 2, chef_id__followed_by = self.request.user.id).order_by("-date_scheduled").all()
        context['chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['page_dishes'])
        # context['best_chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['best_dishes'])
        # context['todo_chef_comments'] = Chef_Dish_Comments.objects.filter(dish_id__in=context['todo_dishes'])
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
            if self.request.GET.get('next')=="new":
                return '/cooklog/dish/add/?next=' + str(self.object.recipe_id)
            elif self.request.GET.get('next')=="newtodo":
                return '/cooklog/dish/add-todo/?next=' + str(self.object.recipe_id)
            else:
                return '/cooklog/dish/recipe_choose/' + self.request.GET.get('next') + '/?next=' + str(self.object.recipe_id)
        else:
            return '/cooklog/recipe/' + str(self.object.recipe_id) + '/'


class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['recipe_name', 'recipecategory_id', 'tags', 'recipe_source', 'recipe_method','recipe_comments',
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
        return ChefFollows.objects.filter(follower_id=self.kwargs.get("pk", None)) # self.request.user.id should work too
    def get_success_url(self):
        return '/cooklog/' # not: chef/' + str(self.request.user.id) + '/'


class ChefUpdate(UpdateView):
    model = Chef
    fields = ['first_name', 'last_name', 'bio', 'email', 'chef_image'] #'date_created'
    def get_success_url(self):
        return '/cooklog/chef/' + str(self.object.chef_id) + '/'

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

class DishTodoQuickCreate(CreateView):
    form_class = NewDishTodoQuickForm
    template_name = 'new_dish_todo_quick_form.html'
    def get_initial(self):
        return {'chef_id': self.request.user.id, 'recipe_id': 1, 'dish_status': 2}  # default recipe: None.
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
        if self.request.GET.get('c'):
            if (str(self.request.GET.get('c')) == "0"):
                return '/cooklog/'
            else:
                return '/cooklog/chef/feed/' + str(self.request.GET.get('c')) + '/'
        else:
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


class NewEntryView(TemplateView):
    template_name = 'new_entry.html'

class NewEntryDoneView(TemplateView):
    template_name = 'new_entry_done.html'

class NewEntryTodoView(TemplateView):
    template_name = 'new_entry_todo.html'
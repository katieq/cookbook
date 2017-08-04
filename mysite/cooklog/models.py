import datetime

from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from annoying.fields import AutoOneToOneField

#from taggit.managers import TaggableManager

class Chef(models.Model):
    chef_id = models.AutoField(primary_key=True)
    chef_to_user_id = models.ForeignKey(User) # could be OneToOneField, but annoying to start. I'm fine if One User Has Two Chef acounts. ... tried: OneToOneField(User, on_delete=models.CASCADE, primary_key=True) # <- but created other problems.
    # chef_id = AutoOneToOneField('auth.user')
    email = models.CharField("Email address", max_length=50)
    first_name = models.CharField("First name", max_length=30)
    last_name = models.CharField("Last name", max_length=30)
    bio = models.TextField(max_length = 500, blank = True, null = True)
    birth_date = models.DateField(null = True, blank = True)
    #follower_id = models.ManyToManyField(User,  blank=True)
    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    def get_absolute_url(self):
        return reverse('chef-detail', kwargs={'pk': self.pk})

class ChefFollows(models.Model):
    # chef_follow_id = models.AutoField(primary_key=True)
    follower_id = AutoOneToOneField('auth.user') #models.ForeignKey(User, on_delete=models.CASCADE)
    # chef_id = models.ForeignKey(Chef, on_delete=models.CASCADE)
    chef_id = models.ManyToManyField(Chef, related_name='followed_by')
    date_created = models.DateTimeField("Date created", default = datetime.datetime.now)
    def __str__(self):
        return self.follower_id.username

#@receiver(post_save, sender=User)
#def create_user_chef(sender, instance, created, **kwargs):
#    if created:
#        Chef.objects.create(user=instance)
#@receiver(post_save, sender=User)
#def save_user_chef(sender, instance, **kwargs):
#    instance.chef.save()

class RecipeCategory(models.Model):
    recipecategory_id = models.AutoField(primary_key=True)
    recipecategory_name = models.CharField("Recipe category name", max_length=30)
    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
    def __str__(self):
        return self.recipecategory_name
    def get_absolute_url(self):
        return reverse('recipecategory-detail', kwargs={'pk': self.pk})


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipecategory_id = models.ForeignKey(RecipeCategory, blank = True, null = True)
    recipe_name = models.CharField("Recipe name", max_length=200)
    recipe_source = models.CharField("Recipe source", max_length=200)
    recipe_type = models.CharField(max_length=30)
    chef_id = models.ForeignKey(Chef) # removed on.delete=CASCADE, because if chef is deleted, I want to keep recipes
    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
    def __str__(self):
        return self.recipe_name
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})

#class Ingredient(models.Model):
#    ingredient_id = models.AutoField(primary_key=True)
#    ingredient_name = models.CharField("Ingredient name", max_length=30)
#    ingredient_type = models.CharField("Ingredient type", max_length=30)
#    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
#    def __str__(self):
#        return self.ingredient_name
#    def get_absolute_url(self):
#        return reverse('ingredient-detail', kwargs={'pk': self.pk})
class IngredientType(models.Model):
    ingredient_type_id = models.AutoField(primary_key = True)
    ingredient_type_name = models.CharField("Ingredient type name", max_length=30)
    date_created = models.DateTimeField("Date created", default = datetime.datetime.now)
    def __str__(self):
        return self.ingredient_type_name

class Maker(models.Model):
    maker_id = models.AutoField(primary_key = True)
    maker_name = models.CharField("Maker name", max_length=30)
    maker_type = models.CharField("Maker type", max_length=30, null = True, blank = True) # e.g. farm
    maker_url =  models.URLField("Ingredient URL", max_length=200, null = True, blank = True)
    maker_image = models.ImageField(upload_to="maker_photos", null = True, blank = True)
    date_created = models.DateTimeField("Date created", default = datetime.datetime.now)
    def __str__(self):
        return self.maker_name
    def get_absolute_url(self):
            return reverse('maker-detail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField("Ingredient name", max_length=30)
    ingredient_type_id = models.ForeignKey(IngredientType, on_delete=models.CASCADE, null = True, blank = True)
    ingredient_type_detail = models.CharField("Ingredient type detail", max_length = 30, null = True, blank = True)
    maker_id = models.ForeignKey(Maker, on_delete=models.CASCADE, null = True, blank = True) #<- optional!!! or have a Maker=NA
    ingredient_image = models.ImageField(upload_to="ingredient_photos", null = True, blank = True)
    ingredient_url = models.URLField("Ingredient URL", max_length=200, null = True, blank = True)
    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
    def __str__(self):
        return self.ingredient_name
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'pk': self.pk})

#class DishType(models.Model):
#    dishtype_id = models.AutoField(primary_key=True)
#    dishtype_tag = models.CharField("Dish type tag", max_length=30)
#    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
#    def __str__(self):
#        return self.dishtype_tag
#    def get_absolute_url(self):
#        return reverse('dishtype-detail', kwargs={'pk': self.pk})


class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    chef_id = models.ForeignKey(Chef, default=1, on_delete=models.CASCADE) # I wonder..if cook together, ManytoMany Chef!?
    recipe_id = models.ForeignKey(Recipe)
    extra_recipe_id = models.ManyToManyField(Recipe, blank = True, related_name="extra_recipe_dish") # changed from ForeignKey with on_delete=models.CASCADE; allow blank for now, perhaps change later.
    STATUS_CHOICES = ((u'1', u'Done'),
                      (u'2', u'To-do-soon'),
                      (u'3', u'To-do-someday'),)
    dish_status = models.CharField("Dish status", max_length=1, choices=STATUS_CHOICES, default='1')
    date_scheduled = models.DateField("Date scheduled", null=True, blank=True)
    dish_name = models.CharField("Dish name", max_length=200) # default recipe name??
    #dishtype_id = models.ManyToManyField(DishType,  blank=True)
    dish_source = models.CharField("Recipe source", null=True, blank=True, max_length=200)
    dish_method = models.CharField("Dish method", max_length=1000,
                                   null=True, blank=True)
    dish_rating = models.IntegerField("Dish rating", validators=[MaxValueValidator(5), MinValueValidator(0)],
                                      null=True, blank=True)
    dish_comments = models.CharField("Dish comments", max_length=800,
                                     null=True, blank=True) # my own comments about how I liked it..
    ingredient_id = models.ManyToManyField(Ingredient,  blank=True)
    ##can't have two fields to Chef? like_chef_id = models.ManyToManyField(Chef) # tie to dish, instead of its own Likes model. AGH! I think you can! but just needs related_name! thus can remove the "likes" model..??
    dish_image = models.ImageField(upload_to="dish_photos", null = True, blank = True)
    photo_comment = models.CharField("Photo comment", max_length=200, null = True, blank = True)
    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
    # tags = TaggableManager()
    def __str__(self):
        return self.dish_name
    def get_absolute_url(self):
        return reverse('dish-detail', kwargs={'pk': self.pk})

## From now on: this will only be *backup duplicate* and maybe soon *removed*
#class Dish_Photo(models.Model):
#    dish_photo_id = models.AutoField(primary_key=True)
#    dish_id = models.ManyToManyField(Dish) #models.ForeignKey(Dish, on_delete=models.CASCADE)
#    dish_image = models.ImageField(upload_to="dish_photos")
#    photo_comment = models.CharField("Photo comment", max_length=200)
#    date_created = models.DateTimeField("Date created", default=datetime.datetime.now)
##def __str__(self):
##return self.dish_id

class Likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    chef_id = models.ForeignKey(Chef, on_delete=models.CASCADE)

class Chef_Dish_Comments(models.Model):   # avoided ever just comment, since reserved word perhaps?
    chef_dish_comment_id = models.AutoField(primary_key=True)
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    chef_id = models.ForeignKey(Chef, default=1, on_delete=models.CASCADE)
    chef_dish_comment = models.CharField("Chef dish comment", max_length = 800) # not sure what name should be?










#class Recipe_Ingredients(models.Model):
#    recipe_ingredients_id = models.AutoField(primary_key=True)
#    recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
#    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE) # no many:many b/c new table
#    quantity = models.CharField("Ingredient quantity", max_length=10)
#    date_created = models.DateTimeField("Date created")
# No __str__(self) .. should there be?

#class Recipe_Method(models.Model):
#    recipe_method_id = models.AutoField(primary_key=True)
#    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#    method_text = models.CharField("Recipe method", max_length=500)
#    date_created = models.DateTimeField("Date created")

#class Dish_Ingredients(models.Model):
#    dish_ingredient_id = models.AutoField(primary_key=True)
#    dish_id = models.ForeignKey(Dishes, on_delete=models.CASCADE)
#    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE) # no many:many here b/c new table
#    quantity = models.CharField("Ingredient quantity", max_length=10)
#    date_created = models.DateTimeField("Date created")


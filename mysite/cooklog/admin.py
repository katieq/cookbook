from django.contrib import admin

from .models import Chef, Recipe, Ingredient, Dish, Chef_Dish_Comments, RecipeCategory, IngredientType, Maker, ChefFollows, Bugs

class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 3

class ChefAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')
    # inlines = [RecipeInline] # <- Because annoying, forcing entries for the "blank extras"

admin.site.register(Chef, ChefAdmin)

class DishInline(admin.TabularInline):
    model = Dish
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    # inlines = [DishInline] # <- Removed because Dish->Recipe is now ManyToMany
    search_fields = ('recipe_name', 'recipecategory_id')
    list_display = ('recipe_name', 'date_created')
    list_filter = ('date_created',)

admin.site.register(Recipe, RecipeAdmin)

class DishAdmin(admin.ModelAdmin):
    search_fields = ('dish_name', 'dish_method') # method kinda enables ingredient searching
    list_display = ('dish_name', 'recipe_id', 'date_created')
    list_filter = ('date_created',)
    filter_horizontal = ('ingredient_id',)

admin.site.register(Dish, DishAdmin)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name','ingredient_type_id','date_created')

admin.site.register(Ingredient, IngredientAdmin)

class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('ingredient_type_name','date_created')

admin.site.register(IngredientType, IngredientTypeAdmin)

class MakerAdmin(admin.ModelAdmin):
    list_display = ('maker_name','date_created')

admin.site.register(Maker, MakerAdmin)

#admin.site.register(Dish_Photo)
admin.site.register(RecipeCategory)

class ChefDishCommentsAdmin(admin.ModelAdmin):
    list_display = ('dish_id', 'chef_id', 'date_created')
admin.site.register(Chef_Dish_Comments, ChefDishCommentsAdmin)

admin.site.register(ChefFollows)

class BugsAdmin(admin.ModelAdmin):
    list_display = ('user_id','bug_comment','bug_status','date_created')

admin.site.register(Bugs, BugsAdmin)





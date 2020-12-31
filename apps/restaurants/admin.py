from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _

from .models import Restaurant, City, Ingredient, DishIngredient, Dish, Beverage


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    search_fields = ('name', )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_type', 'city', 'is_enable')
    search_fields = ('name', )
    list_filter = ('is_enable', 'restaurant_type', 'city')
    list_select_related = ('city',)
    # save_as = True


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'portion')
    search_fields = ('name', 'portion')
    list_filter = ('type', 'portion')


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    search_fields = ('name', )


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    fields = ['ingredient', 'portion']
    raw_id_fields = ('ingredient', )
    extra = 1


@admin.register(Beverage)
class BeverageAdmin(FoodAdmin):
    pass


@admin.register(Dish)
class DishAdmin(FoodAdmin):
    readonly_fields = ('price', )
    inlines = (DishIngredientInline,)

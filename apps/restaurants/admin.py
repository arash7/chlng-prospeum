from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _

from .models import Restaurant, City, Ingredient, DishIngredient, Dish, Beverage, Stock


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    search_fields = ('name', )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_type', 'city', 'seats', 'is_enable')
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
    list_display = ('name', 'type', 'kind', 'price')
    search_fields = ('name', )
    list_filter = ('kind',)


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    fields = ['ingredient', 'portion']
    raw_id_fields = ('ingredient', )
    extra = 1


@admin.register(Beverage)
class BeverageAdmin(FoodAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type=Beverage.TYPE_BEVERAGE)


@admin.register(Dish)
class DishAdmin(FoodAdmin):
    readonly_fields = ('price', )
    inlines = (DishIngredientInline,)
    save_as_continue = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type=Dish.TYPE_DISH)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'restaurant', 'created_time', 'amount')
    list_filter = ('created_time', 'restaurant', 'ingredient')
    date_hierarchy = 'created_time'

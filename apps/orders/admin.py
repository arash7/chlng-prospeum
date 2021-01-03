from django.contrib import admin

from .models import Order, OrderContent


class OrderContentInline(admin.TabularInline):
    model = OrderContent
    fields = ['food', 'qty']
    raw_id_fields = ('food', )
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'guest', 'reservation_date', 'price', 'is_takeout')
    search_fields = ('name', )
    list_filter = ('is_takeout', 'restaurant')
    raw_id_fields = ('guest', 'restaurant')
    inlines = (OrderContentInline,)

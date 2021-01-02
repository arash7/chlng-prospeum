from django.db import models
# from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        verbose_name_plural = _('cities')

    def __str__(self):
        return self.name


class LiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_enable=True)


class Restaurant(models.Model):
    TYPE_CHINESE = 'ch'
    TYPE_BAVARIAN = 'bv'
    TYPE_ITALIAN = 'it'
    TYPE_CHOICES = (
        (TYPE_CHINESE, _('chinese')),
        (TYPE_BAVARIAN, _('bavarian')),
        (TYPE_ITALIAN, _('italian')),
    )

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    restaurant_type = models.CharField(_('type'), max_length=2, choices=TYPE_CHOICES)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    is_enable = models.BooleanField(_('is enable?'), default=True)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    objects = models.Manager()
    lives = LiveManager()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    TYPE_CHICKEN = 1
    TYPE_BEEF = 2
    TYPE_PORK = 3
    TYPE_VEGETARIAN = 4
    TYPE_VEGAN = 5
    TYPE_CHOICES = (
        (TYPE_CHICKEN, _('chicken')),
        (TYPE_BEEF, _('beef')),
        (TYPE_PORK, _('pork')),
        (TYPE_VEGETARIAN, _('vegetarian')),
        (TYPE_VEGAN, _('vegan')),
    )

    name = models.CharField(_('name'), max_length=20)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, help_text=_('Price per portion'))
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES)
    portion = models.CharField(_('portion'), max_length=10, help_text=_('Just for display, eg: litre, gr, ounce, cup, etc..'))

    def __str__(self):
        return self.name


class Food(models.Model):
    TYPE_DISH = 1
    TYPE_BEVERAGE = 2
    TYPE_CHOICES = (
        (TYPE_DISH, _('dish')),
        (TYPE_BEVERAGE, _('beverage')),
    )

    name = models.CharField(_('name'), max_length=40)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=2, default=0)
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES, editable=False)
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')

    def __str__(self):
        return self.name


class Beverage(Food):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = self.TYPE_BEVERAGE
        super().save(*args, **kwargs)


class Dish(Food):
    class Meta:
        proxy = True
        verbose_name_plural = _('dishes')

    def save(self, *args, **kwargs):
        self.type = self.TYPE_DISH
        super().save(*args, **kwargs)


class DishIngredient(models.Model):
    dish = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='ing_list')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    portion = models.DecimalField(_('portion'), max_digits=5, decimal_places=2, help_text=_('portion used in dish'))

    class Meta:
        unique_together = ('dish', 'ingredient')

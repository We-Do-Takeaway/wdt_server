from django.contrib import admin

from .models import Ingredient, Item, ItemIngredient, Menu, Section, SectionItem

admin.site.register(Menu)
admin.site.register(Section)
admin.site.register(Item)
admin.site.register(Ingredient)
admin.site.register(SectionItem)
admin.site.register(ItemIngredient)

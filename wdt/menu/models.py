import uuid
from django.db import models


class Menu(models.Model):
    """ Menu is a top level container that contains sections and items """
    class Meta:
        db_table = "menu"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.TextField()
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    """ A thing in a menu that you can order and eat, made up of ingredients """
    class Meta:
        db_table = "item"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        to='Ingredient',
        through='ItemIngredient',
        through_fields=('item', 'ingredient'),
    )
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)
    sections = models.ManyToManyField(
        to='Section',
        through='SectionItem',
        through_fields=('item', 'section'),
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    """ A section belongs to a menu and contains items """
    class Meta:
        db_table = "section"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    items = models.ManyToManyField(
        to='Item',
        through='SectionItem',
        through_fields=('section', 'item'),
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)
    display_order = models.IntegerField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredients are combined to produce a menu item """
    class Meta:
        db_table = "ingredient"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.TextField()
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SectionItem(models.Model):
    """ Join Sections to items and define the order items appear """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section_id", "item_id"],
                name="unique_section_and_item"
            )
        ]
        db_table = "section_item"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    display_order = models.IntegerField()

    def __str__(self):
        return f'{self.section.name}:{self.item.name}:{self.display_order}'


class ItemIngredient(models.Model):
    """ Associate items and ingredients and set how much is needed """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item_id", "ingredient_id"],
                name="unique_item_and_ingredient"
            )
        ]
        db_table = "item_ingredient"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.item.name}:{self.ingredient.name}:{self.quantity}'

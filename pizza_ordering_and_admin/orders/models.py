from django.db import models


types_choices=(
    ("Regular Pizza" , 'Regular Pizza'),
    ("Sicilian Pizza" , 'Sicilian Pizza'),
    ("Toppings" , 'Toppings'),
    ("Subs" , 'Subs'),
    ("Pasta" , 'Pasta'),
    ("Salads", 'Salads'),
    ("Dinner Platters" , 'Dinner Platters'),
)


# Create your models here.
class Menu(models.Model):

    type = models.CharField(max_length=64, choices=types_choices)
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=5, decimal_places=2, null= True, blank= True)
    large = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    toppings = models.IntegerField(null = True, blank = True)


    def __str__(self):
        if self.type == "Toppings":
            return f"{self.name}"
        elif self.type == "Pasta" or self.type == "Salad":
            return f"{self.name} ({self.small})$"
        else:
            return f"{self.name} small:({self.small})$ large:({self.large})$"


class Cart(models.Model):

    username = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    topping1 = models.CharField(max_length=64, null= True, blank= True)
    topping2 = models.CharField(max_length=64, null= True, blank= True)
    topping3 = models.CharField(max_length=64, null= True, blank= True)
    topping4 = models.CharField(max_length=64, null= True, blank= True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null= True, blank= True)

    def __str__(self):
        draft = f"{self.type}, {self.name}"
        if self.topping1 or self.topping2 or self.topping3:
            draft += f" ({self.topping1})({self.topping2})({self.topping3})({self.topping4})"
        draft += f"    {self.price}$"
        while "(None)" in draft:
            draft = draft.replace("(None)","")
        return draft

class Order(models.Model):

    username = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    topping1 = models.CharField(max_length=64, null= True, blank= True)
    topping2 = models.CharField(max_length=64, null= True, blank= True)
    topping3 = models.CharField(max_length=64, null= True, blank= True)
    topping4 = models.CharField(max_length=64, null= True, blank= True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null= True, blank= True)

    def __str__(self):
        draft = f"{self.type}, {self.name}"
        if self.topping1 or self.topping2 or self.topping3:
            draft += f" ({self.topping1})({self.topping2})({self.topping3})({self.topping4})"
        draft += f"    {self.price}$"
        while "(None)" in draft:
            draft = draft.replace("(None)","")
        return draft

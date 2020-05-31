from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Menu, Cart, Order
from django.db.models import Avg, Count, Min, Sum
from django.core.mail import send_mail

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    username = request.user.username
    return HttpResponseRedirect(reverse("menu"))
def signin(request):
    if request.user.is_authenticated:
        context = {
            "user": request.user
        }
        return HttpResponseRedirect(reverse("menu"))
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
    except:
        return render(request, "users/signup.html", {"message":"oops! something went wrong"})

    if not username or not password or not email or not first_name or not last_name:
        return render(request, "users/signup.html", {"message":"all fields are necassary to fill"})
    if "@" not in email:
        return render(request, "users/signup.html", {"message":"enter valid email id"})
    try:
        user = User.objects.create_user(username,email,password)
    except:
        return render(request, "users/signup.html", {"message":"username already exists"})
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    login(request, user)
    authorize = request.user.username
    if authorize ==  "administrator":
        return HttpResponseRedirect(reverse("administrators"))
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return render(request, "users/login.html", {"message": "something went wrong there please retry and do not refresh the page"})
    if not username or not password:
        return render(request, "users/login.html", {"message": "this time put some effort in typing"})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        authorize = request.user.username
        if authorize ==  "administrator":
            return HttpResponseRedirect(reverse("administrators"))
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})
def signup(request):

    return render(request, "users/signup.html", {"message":None})

def menu(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters")
    }
    return render(request, "orders/menu.html", context)

def orders(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters"),
        "message":None
    }
    return render(request, "orders/orders.html", context)

def pizza(request):

    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    username = request.user.username
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters"),
        "message":None
    }
    try:
        type = request.POST["pizza-type"]
        toppings = request.POST.getlist("pizza-toppings")
        size  = request.POST["pizza-size"]
    except:
        context["message"] = "Something is wrong in your pizza order please try again"

        return render(request, "orders/orders.html", context)
    toppingscount = len(toppings)
    if toppingscount == 0:
        topping1,topping2,topping3,topping4 = None,None,None,None
    elif toppingscount == 1:
        topping1,topping2,topping3,topping4 = toppings[0],None,None,None
    elif toppingscount == 2:
        topping1,topping2,topping3,topping4 = toppings[0],toppings[1],None,None
    elif toppingscount == 3:
        topping1,topping2,topping3,topping4 = toppings[0],toppings[1],toppings[2],None
    elif toppingscount == 4:
        topping1,topping2,topping3,topping4 = toppings[0],toppings[1],toppings[2],toppings[3]
    else:
        context["message"] = f"You can select at max 4 toppings and you have selected {toppingscount}"
        return render(request, "orders/orders.html", context)
    data = Menu.objects.filter(type=type, toppings=toppingscount)
    if not data:
        context["message"] = "No Such Pizza Found"
        return render(request, "orders/orders.html", context)

    name = data[0].name
    if size == "small":
        price = data[0].small
    else:
        price = data[0].large
    type = type + " (" + size + ")"
    #type toppings  size  price username name
    try:
        add = Cart(username = username, type = type, name = name, topping1=topping1, topping2=topping2, topping3=topping3, topping4=topping4, price=price)
        add.save()
    except:
        context["message"] = "Our apology there is some database error"
    context["message"] = "Succesfully added to the cart"
    return render(request, "orders/orders.html", context)

def pns(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    username = request.user.username
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters"),
        "message":None
    }
    try:
        type = request.POST["pns-type"]
        name = request.POST["pns-name"]
    except:
        context["message"] = "Something is wrong in your Pasta/Salad order please try again"
        return render(request, "orders/orders.html", context)
    data = Menu.objects.filter(type=type, name=name)
    if not data:
        context["message"] = f"No Such {type} Found"
        return render(request, "orders/orders.html", context)
    price = data[0].small
    try:
        add = Cart(username = username, type = type, name = name, price=price)
        add.save()
    except:
        context["message"] = "our apology there is some database error"
    context["message"] = "Succesfully added to the cart"
    return render(request, "orders/orders.html", context)
def subs(request):

    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    username = request.user.username
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters"),
        "message":None
    }
    try:
        name = request.POST["sub-name"]
        toppings = request.POST.getlist("sub-toppings")
        size  = request.POST["sub-size"]
        type = "Subs"
    except:
        context["message"] = "Something is wrong in your Subs order please try again"
        return render(request, "orders/orders.html", context)
    try:
        extracheese  = request.POST["extracheese"]
    except:
        extracheese = None

    data = Menu.objects.filter(type=type, name = name)
    if not data:
        context["message"] = "No Such Sub Found"
        return render(request, "orders/orders.html", context)

    if size == "small":
        price = float(data[0].small)
    else:
        price = float(data[0].large)

    if name == "Steak + Cheese":
        toppingscount = len(toppings)
        price += (0.5* toppingscount)
        if toppingscount == 0:
            topping1,topping2,topping3 = None,None,None
        elif toppingscount == 1:
            topping1,topping2,topping3 = toppings[0],None,None
        elif toppingscount == 2:
            topping1,topping2,topping3 = toppings[0],toppings[1],None
        elif toppingscount == 3:
            topping1,topping2,topping3 = toppings[0],toppings[1],toppings[2]
    else:
        topping1,topping2,topping3 = None,None,None

    type = type + " (" + size + ")"

    if extracheese == "Extra Cheese":
        price += 0.5
        topping4 = "Extra Cheese"
    else:
        topping4 = None
    #type toppings  size  price username name
    try:
        add = Cart(username = username, type = type, name = name, topping1=topping1, topping2=topping2, topping3=topping3, topping4=topping4, price=price)
        add.save()
    except:
        context["message"] = "Our apology there is some database error"
    context["message"] = f"Succesfully added your Sub to the cart"
    return render(request, "orders/orders.html", context)
def dinnerplatter(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":"you need to login/register first"})
    username = request.user.username
    context= {
        "rp":Menu.objects.filter(type = "Regular Pizza"),
        "sp":Menu.objects.filter(type = "Sicilian Pizza"),
        "t":Menu.objects.filter(type = "Toppings"),
        "sub":Menu.objects.filter(type = "Subs"),
        "p":Menu.objects.filter(type = "Pasta"),
        "sal":Menu.objects.filter(type = "Salads"),
        "dp":Menu.objects.filter(type = "Dinner Platters"),
        "message":None
    }
    try:
        type = "Dinner Platters"
        size = request.POST["dp-size"]
        name = request.POST["dp-name"]
    except:
        context["message"] = "Something is wrong in your Dinner Platters order please try again"
        return render(request, "orders/orders.html", context)
    data = Menu.objects.filter(type=type, name=name)
    if not data:
        context["message"] = f"No Such {type} Found"
        return render(request, "orders/orders.html", context)
    if size == "small":
        price = data[0].small
    else:
        price = data[0].large
    type = type + " (" + size + ")"
    try:
        add = Cart(username = username, type = type, name = name, price=price)
        add.save()
    except:
        context["message"] = "Our apology there is some database error"
    context["message"] = "Succesfully added to the cart"
    return render(request, "orders/orders.html", context)



def cart(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    username = request.user.username
    try:
        context= {
            "cart": Cart.objects.filter(username = username),
            "total": round(Cart.objects.filter(username=username).aggregate(Sum('price'))["price__sum"],2)
        }
    except:
        context= {
            "cart": Cart.objects.filter(username = username),
            "total": "Your Cart is Empty"
        }

    return render(request, "orders/cart.html", context)

def remove(request, cart_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    username = request.user.username
    try:
        data = Cart.objects.get(pk=cart_id)
    except:
        return HttpResponseRedirect(reverse("cart"))
    if data.username != username:
        return HttpResponseRedirect(reverse("cart"))
    data.delete()
    return HttpResponseRedirect(reverse("cart"))

def checkout(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    user = request.user
    username = user.username
    email_id = user.email

    try:
        items = Order.objects.filter(username = username)
        total = round(Order.objects.filter(username=username).aggregate(Sum('price'))["price__sum"],2)
    except:
        pass
    else:
        context= {
            "cart": Cart.objects.filter(username = username),
            "total":round(Cart.objects.filter(username=username).aggregate(Sum('price'))["price__sum"],2)
        }
        return render(request, "orders/cart.html", context)
    try:
        items = Cart.objects.filter(username = username)
        total = round(Cart.objects.filter(username=username).aggregate(Sum('price'))["price__sum"],2)
    except:
        context= {
            "cart": Cart.objects.filter(username = username),
            "total": "Your Cart is Empty"
        }
        return render(request, "orders/cart.html", context)
    for i in items:
        f = Order(username=str(i.username), type=str(i.type), name = str(i.name), topping1 = str(i.topping1), topping2 = str(i.topping2), topping3 = str(i.topping3), topping4 = str(i.topping4), price = float(i.price))
        f.save()
        i.delete()
    uri = request.build_absolute_uri(reverse('order'))
    send_mail("Order Confirmation",f"Order for {username}({user.first_name} {user.last_name}) amount {total}. Check order summary at {uri}","sambhav2003gupta@gmail.com", ["sambhav2003gupta@gmail.com"], fail_silently=False)
    return HttpResponseRedirect(reverse("menu"))



def order(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    username = request.user.username
    context= {
        "cart": Order.objects.filter(username = username),
        "total": round(Order.objects.filter(username=username).aggregate(Sum('price'))["price__sum"],2)
    }
    return render(request, "orders/order.html", context)


def administrators(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    username = request.user.username
    if username !=  "administrator":
        return HttpResponseRedirect(reverse("index"))
    try:
        user = request.POST["username"]
    except:
        users = Order.objects.all()
        context = {
            "users":[]
        }
        for i in users:
            if i.username not in context["users"]:
                context["users"].append(i.username)
        return render(request, "orders/administrator.html", context)
    context = {
        "order": Order.objects.filter(username = user),
        "user":user
    }
    return render(request, "orders/administrator0.html", context)

def administratorsrem(request, username):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html',{"message":None})
    authorize = request.user.username
    if authorize !=  "administrator":
        return HttpResponseRedirect(reverse("index"))
    f = Order.objects.all()
    for i in f:
        i.delete()
    return HttpResponseRedirect(reverse("administrators"))

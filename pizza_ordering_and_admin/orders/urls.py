from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("menu", views.menu, name="menu"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("pizza", views.pizza, name="pizza"),
    path("pns", views.pns, name="pns"),
    path("dinnerplatter", views.dinnerplatter, name="dinnerplatter"),
    path("subs", views.subs, name="subs"),
    path("remove/<int:cart_id>", views.remove, name="remove"),
    path("administratorsrem/<slug:username>", views.administratorsrem, name="administratorsrem"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("order", views.order, name="order"),
    path("administrators", views.administrators, name="administrators"),
    path("orders", views.orders, name="orders")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.newlisting, name="newlisting"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("newcategory", views.newcategory, name="newcategory"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("placebid/<int:listing_id>", views.placebid, name="placebid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closelisting/<int:listing_id>", views.closelisting, name="closelisting"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("deletewatchlist/<int:listing_id>", views.deletewatchlist, name="deletewatchlist"),
    path("category", views.category, name="category")
]


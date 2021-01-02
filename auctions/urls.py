from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createList/", views.create_list, name="createlist"),
    path("details/<int:txt>", views.details, name="details"),
    path("catagorySearch/<str:catagory>", views.catagory, name="catagory"),
    path("comment/", views.addComment, name="addcommenturl"),
    path("addtowatchList", views.add_to_watchList, name="addtowatchList"),
    path("watchList", views.watchList, name="watchList"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("closeList", views.clostList, name="closeList"),
    path("closedList", views.closedList, name="closedList")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ActiveAuctionsListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.AuctionCreateView.as_view(), name="create"),
    path("auctions/<int:pk>/", views.AuctionDetailView.as_view(), name="auctions"),
    path("update/<int:pk>/watchlist", views.toggle_watchlist, name="update_watchlist"),
    path("update/<int:pk>/bid", views.bid, name="bid"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ActiveAuctionsListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.AuctionCreateView.as_view(), name="create"),
    path("auctions/<int:pk>/", views.AuctionDetailView.as_view(), name="auctions"),
    path("wishlist", views.WishlistListView.as_view(), name="wishlist"),
    path("categories", views.Categories, name="categories"),
    path("categories/<str:category>/", views.CategoryListView.as_view(), name="category"),
    path("update/<int:pk>/watchlist", views.toggle_watchlist, name="update_watchlist"),
    path("update/<int:pk>/bid", views.bid, name="bid"),
    path("update/<int:pk>/active", views.active, name="active"),
    path("update/<int:pk>/comment", views.comment, name="comment"),
]

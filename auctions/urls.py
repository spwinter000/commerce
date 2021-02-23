from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("comment/<int:listing_id>", views.create_comment, name="create_comment"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

# if settings.DEBUG: # new
#     urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

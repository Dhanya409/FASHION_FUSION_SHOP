from . import views
from django.urls import path

urlpatterns = [
    # GENERAL URLS
    path("", views.index, name="s_index"),
    path("products/", views.products, name="s_products"),
    path("sales/", views.sales, name="s_sales"),
    path("notifications/", views.notifications, name="s_notifications"),
    path("logout/", views.signout, name="s_logout"),
    path("accept_restock/<int:id>/", views.accept_restock, name="s_accept_restock"),


]
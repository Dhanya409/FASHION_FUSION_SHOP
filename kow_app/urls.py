from . import views
from django.urls import path
from .views import chat, customer_report, dashboard, similar_products, stock_chart, visualization_view

urlpatterns = [
    path('', views.index, name='index'),
    path('all_products/', views.all_products, name='all_products'),
    path('product/<int:id>', views.product, name='product'),
    path('category/<int:id>', views.category, name='category'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("order_details/<int:pk>/", views.order_details, name="order_details"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/full_remove/<int:product_id>/', views.full_remove, name='full_remove'),
    path("place_order/", views.place_order, name="place_order"),

    path('adminpage/', views.admin_login, name='admin_login'),
    path('adminpage/home/', views.home, name='home'),
    path('adminpage/add_category/', views.add_category, name='add_category'),
    path('adminpage/add_product/', views.add_product, name='add_product'),
    path('adminpage/edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('adminpage/edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('adminpage/delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('adminpage/delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('reports/', views.monthly_sales_report, name='admin_reports'),
    path('visualizations/', views.visualization_view, name='visualizations'),
    path('similar_products/', similar_products, name='similar_products'),
    path('fashion-recommendation/', views.fashion_recommendation, name='fashion_recommendation'),
    path('chat/', chat, name='chat'), 
    path('stock_report/', views.stock_report, name='stock_report'),
    path('customer_report/', customer_report, name='customer_report'),

    path('visualization/', visualization_view, name='visualizations'),
    path('stock-chart/', stock_chart, name='stock_chart'),
   
    
    

   

]
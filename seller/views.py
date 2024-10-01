from django.shortcuts import render, redirect
from kow_app.models import *
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    seller = request.user.seller
    orders = OrderDetail.objects.filter(product__seller=seller)
    earnings = sum(order.price for order in orders)
    sold = orders.count()
    context = {
        'earnings': earnings,
        'sold': sold,
    }
    return render(request, "seller/index.html", context)

@login_required
def products(request):
    seller = request.user.seller
    inventory = Products.objects.filter(seller=seller)
    context = {
        'seller': seller,
        'inventory': inventory
    }
    return render(request, "seller/products.html", context)

@login_required
def sales(request):
    seller = request.user.seller
    sales = OrderDetail.objects.filter(product__seller=seller)
    context = {
        'sales': sales
    }
    return render(request, "seller/sales.html", context)

@login_required
def notifications(request):
    return render(request, "seller/notifications.html")

def accept_restock(request, id):
    item = SellerNotification.objects.get(id=id)
    inventory = item.inventory
    restock_quantity = item.quantity_to_restock
    inventory.quantity += restock_quantity
    inventory.save()
    admin_user = User.objects.filter(is_staff=True).first()
    if admin_user:
        subject = "Seller Restock Success"
        message = f"The seller has supplied '{item.quantity_to_restock} x {item.inventory.name}' to the Inventory"
        Notification.objects.create(subject=subject, message=message)
    item.delete()
    return redirect('s_notifications')

@login_required
def signout(request):
    logout(request)
    return redirect('/')



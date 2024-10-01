from django.contrib import admin, messages
from .models import *
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Seller)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'quantity', 'price', 'date', 'status')

    def customer(self, obj):
        return obj.order.customer
    
    def item(self, obj):
        return truncatechars(obj.product.name, 40)
    
    def date(self, obj):
        return obj.order.order_date
    
    def status(self, obj):
        return obj.order.status

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'quantity', 'reorder_level', 'seller')

    def product_name(self, obj):
        return truncatechars(obj.name, 30)

@admin.register(LowStockProducts)
class LowStockProductsAdmin(admin.ModelAdmin):
    readonly_fields = ('inventory',)
    list_display = ('item_name', 'restock_level', 'current_quantity', 'restock_quanity', 'seller')
    actions = ['send_restock_request']

    def item_name(self, obj):
        return truncatechars(obj.inventory.name, 50)

    def current_quantity(self, obj):
        return obj.inventory.quantity
    
    def restock_level(self, obj):
        return obj.inventory.reorder_level
    
    def restock_quanity(self, obj):
        return obj.quantity_to_restock
    
    def seller(self, obj):
        return obj.inventory.seller.name
    
    def send_restock_request(self, request, queryset):
        for low_stock_product in queryset:
            if low_stock_product.quantity_to_restock > 0:
                # Create SellerNotification for restock request
                sender = request.user  # Admin sending the request
                receiver = low_stock_product.inventory.seller.user  # Seller receiving the request
                subject = "Restock Request"
                message = f"Please restock {low_stock_product.inventory.name}."
                request_type = "restock"
                quantity_to_restock = low_stock_product.quantity_to_restock
                inventory = low_stock_product.inventory

                # Create SellerNotification with quantity to restock
                SellerNotification.objects.create(sender=sender, receiver=receiver, subject=subject,
                                                message=message, request_type=request_type,
                                                quantity_to_restock=quantity_to_restock, inventory=inventory)
            else:
                messages.warning(request, format_html("Warning: The quantity to restock for '{}' is 0. No restock request sent.", low_stock_product.inventory.product.name))

        self.message_user(request, "Restock requests sent to selected sellers.")
    send_restock_request.short_description = "Send Restock Request to Sellers"
    
# Admin Notification Area ------------------------------------------------------------
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)

mark_as_read.short_description = "Mark selected notifications as read"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'is_read')
    readonly_fields = ('subject', 'message', 'created_at')
    actions = [mark_as_read]

    def has_add_permission(self, request):
        return False
    
# Admin Notification Area End --------------------------------------------------------




from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, null=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True) 

    def __str__(self):
        return self.name

class Products(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='products')
    name=models.CharField(max_length=50, unique=True)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=0)
    reorder_level = models.IntegerField(default=5)
    image = models.ImageField(upload_to='product', blank=True)
    last_update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name} - Quantity: {self.quantity}'
    
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return '{}'.format(self.cart_id)

class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return '{}'.format(self.product)
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    delivery_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Order #{self.pk} - Customer: {self.customer}, Total Amount: {self.total_amount}: {self.status}'
    
    def save(self, *args, **kwargs):
        # Ensure the order_date is set
        if not self.order_date:
            self.order_date = timezone.now().date()
        
        # Set delivery_date if not already set
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(days=7)
        super().save(*args, **kwargs)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order #{self.order.pk} - Product: {self.product.name}, Quantity: {self.quantity}, Price: {self.price}'

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('successful', 'Successful'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    transaction_id = models.CharField(max_length=255, primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment for Order #{self.transaction_id} - Amount: {self.amount} - Method: {self.payment_method}: {self.status}"

class SellerNotification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_seller_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_seller_notifications', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    request_type = models.CharField(max_length=20, choices=[('restock', 'Restock Request')])
    inventory = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity_to_restock = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.subject

class Notification(models.Model):
    subject = models.CharField(max_length=20)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class LowStockProducts(models.Model):
    inventory = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity_to_restock = models.IntegerField(default=0)

    def __str__(self):
        return f'Name: {self.inventory.name[:20]} --- Quantity: {self.inventory.quantity} --- Restock Level: {self.inventory.reorder_level}'

# To automatically create entries in the LowStockProducts model when the quantity <= reorder_level and send notification to admin
@receiver(post_save, sender=Products)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity <= instance.reorder_level:
        LowStockProducts.objects.create(inventory=instance)
        # Notify admin
        admin_user = User.objects.filter(is_staff=True).first()  # Assuming admin is identified by being a staff user
        if admin_user:
            subject = "Low Stock Alert"
            message = f"{subject}: {instance.name} quantity is {instance.quantity}."
            Notification.objects.create(subject=subject, message=message)

# To automatically delete entries in the LowStockProducts model when the quantity > restock level
@receiver(post_save, sender=Products)
@receiver(post_delete, sender=Products)
def check_stock_levels(sender, instance, **kwargs):
    low_stock_entries = LowStockProducts.objects.filter(inventory=instance)
    for entry in low_stock_entries:
        if entry.inventory.quantity > entry.inventory.reorder_level:
            entry.delete()
















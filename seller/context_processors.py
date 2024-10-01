from kow_app.models import SellerNotification

def seller_processor(request):
    try: 
        seller = request.user.seller
        notifications = SellerNotification.objects.filter(receiver=seller.user)
        notification_count = SellerNotification.objects.count()
        context = {
            'seller': seller,
            'notifications': notifications,
            'notification_count': notification_count,
        }
        return context
    except:
        return {'seller': 'Not a Seller'}
    


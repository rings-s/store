from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product, Order
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New order created: {instance.order_number}")
        # Here you can add email notifications, etc.


@receiver(pre_save, sender=Product)
def check_stock_levels(sender, instance, **kwargs):
    if instance.pk:  # Only for existing products
        try:
            old_product = Product.objects.get(pk=instance.pk)
            if old_product.stock_quantity > 0 and instance.stock_quantity == 0:
                logger.warning(f"Product {instance.name} is now out of stock")
            elif old_product.stock_quantity == 0 and instance.stock_quantity > 0:
                logger.info(f"Product {instance.name} is back in stock")
        except Product.DoesNotExist:
            pass
# base/serializers.py
from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant, Stock,
    Cart, CartItem, Order, OrderItem, Payment, Delivery, Review,
    Wishlist, Coupon
)
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    full_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = '__all__'
    
    def get_stock(self, obj):
        if hasattr(obj, 'stock'):
            return StockSerializer(obj.stock).data
        return None


class StockSerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    brand_detail = BrandSerializer(source='brand', read_only=True)
    vendor_detail = UserSerializer(source='vendor', read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    variant_detail = ProductVariantSerializer(source='variant', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    variant_detail = ProductVariantSerializer(source='variant', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'gateway_response': {'write_only': True}
        }


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number']


class ReviewSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Coupon
        fields = '__all__'


# Nested serializers for creating/updating
class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        
        # Create images
        for i, image in enumerate(images_data):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(i == 0),
                display_order=i
            )
        
        # Create initial stock
        Stock.objects.create(product=product)
        
        return product


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    variant_id = serializers.UUIDField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1)
    customization = serializers.JSONField(required=False, default=dict)
    gift_message = serializers.CharField(required=False, allow_blank=True)


class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    # Billing Information
    billing_first_name = serializers.CharField(max_length=100)
    billing_last_name = serializers.CharField(max_length=100)
    billing_email = serializers.EmailField()
    billing_phone = serializers.CharField(max_length=20)
    billing_address = serializers.CharField(max_length=255)
    billing_city = serializers.CharField(max_length=100)
    billing_state = serializers.CharField(max_length=100)
    billing_postal_code = serializers.CharField(max_length=20)
    billing_country = serializers.CharField(max_length=100)
    
    # Shipping Information
    same_as_billing = serializers.BooleanField(default=False)
    shipping_first_name = serializers.CharField(max_length=100, required=False)
    shipping_last_name = serializers.CharField(max_length=100, required=False)
    shipping_phone = serializers.CharField(max_length=20, required=False)
    shipping_address = serializers.CharField(max_length=255, required=False)
    shipping_city = serializers.CharField(max_length=100, required=False)
    shipping_state = serializers.CharField(max_length=100, required=False)
    shipping_postal_code = serializers.CharField(max_length=20, required=False)
    shipping_country = serializers.CharField(max_length=100, required=False)
    
    # Payment
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)
    
    # Additional
    notes = serializers.CharField(required=False, allow_blank=True)
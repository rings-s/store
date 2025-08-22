
# base/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Sum, Count
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant, Stock,
    Cart, CartItem, Order, OrderItem, Payment, Delivery, Review,
    Wishlist, Coupon
)
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer,
    ProductCreateSerializer, ProductImageSerializer, ProductVariantSerializer,
    StockSerializer, CartSerializer, CartItemSerializer, AddToCartSerializer,
    OrderSerializer, OrderItemSerializer, CheckoutSerializer,
    PaymentSerializer, DeliverySerializer, ReviewSerializer,
    WishlistSerializer, CouponSerializer
)
from .permissions import IsVendorOrReadOnly, IsOwnerOrReadOnly, IsVendor


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        elif self.request.query_params.get('root'):
            queryset = queryset.filter(parent__isnull=True)
        return queryset


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrReadOnly]


# Brand Views
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [IsVendorOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('featured'):
            queryset = queryset.filter(is_featured=True)
        return queryset


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsVendorOrReadOnly]


# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsVendorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by brand
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand_id=brand)
        
        # Filter by vendor
        vendor = self.request.query_params.get('vendor')
        if vendor:
            queryset = queryset.filter(vendor_id=vendor)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by featured
        if self.request.query_params.get('featured'):
            queryset = queryset.filter(is_featured=True)
        
        # Filter by in_stock
        if self.request.query_params.get('in_stock'):
            queryset = queryset.filter(stock__quantity__gt=0)
        
        # Ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductSearchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'results': []})
        
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).filter(is_active=True)[:20]
        
        serializer = ProductSerializer(products, many=True)
        return Response({'results': serializer.data})


class ProductImageUploadView(APIView):
    permission_classes = [IsVendor]
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, vendor=request.user)
        images = request.FILES.getlist('images')
        
        created_images = []
        for i, image in enumerate(images):
            is_primary = ProductImage.objects.filter(product=product).count() == 0
            product_image = ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=is_primary,
                display_order=i
            )
            created_images.append(product_image)
        
        serializer = ProductImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductVariantView(APIView):
    permission_classes = [IsVendor]
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        variants = product.variants.all()
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, vendor=request.user)
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockUpdateView(APIView):
    permission_classes = [IsVendor]
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk, vendor=request.user)
        stock, created = Stock.objects.get_or_create(product=product)
        
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Cart Views
class CartView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create cart
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        # Get product and variant
        product = get_object_or_404(Product, pk=serializer.validated_data['product_id'])
        variant = None
        if serializer.validated_data.get('variant_id'):
            variant = get_object_or_404(ProductVariant, pk=serializer.validated_data['variant_id'])
        
        # Check stock
        if variant and hasattr(variant, 'stock'):
            stock = variant.stock
        else:
            stock = product.stock
        
        if stock.available_quantity < serializer.validated_data['quantity']:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add to cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={
                'quantity': serializer.validated_data['quantity'],
                'price': variant.price if variant else product.price,
                'customization': serializer.validated_data.get('customization', {}),
                'gift_message': serializer.validated_data.get('gift_message', '')
            }
        )
        
        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()
        
        return Response(CartSerializer(cart).data)


class UpdateCartItemView(APIView):
    permission_classes = [AllowAny]
    
    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        
        # Verify ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if cart_item.cart.session_key != request.session.session_key:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        quantity = request.data.get('quantity')
        if quantity:
            # Check stock
            if cart_item.variant and hasattr(cart_item.variant, 'stock'):
                stock = cart_item.variant.stock
            else:
                stock = cart_item.product.stock
            
            if stock.available_quantity < quantity:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = quantity
            cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)


class RemoveFromCartView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        
        # Verify ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if cart_item.cart.session_key != request.session.session_key:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})


class ClearCartView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            cart = get_object_or_404(Cart, session_key=request.session.session_key)
        
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'superadmin']:
            return Order.objects.all()
        elif user.role == 'vendor':
            return Order.objects.filter(items__product__vendor=user).distinct()
        else:
            return Order.objects.filter(user=user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'superadmin']:
            return Order.objects.all()
        elif user.role == 'vendor':
            return Order.objects.filter(items__product__vendor=user).distinct()
        else:
            return Order.objects.filter(user=user)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Get cart
        cart = get_object_or_404(Cart, pk=data['cart_id'], user=request.user)
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check stock for all items
        for item in cart.items.all():
            if item.variant and hasattr(item.variant, 'stock'):
                stock = item.variant.stock
            else:
                stock = item.product.stock
            
            if stock.available_quantity < item.quantity:
                return Response({
                    'error': f'Insufficient stock for {item.product.name}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            status='pending',
            
            # Billing info
            billing_first_name=data['billing_first_name'],
            billing_last_name=data['billing_last_name'],
            billing_email=data['billing_email'],
            billing_phone=data['billing_phone'],
            billing_address=data['billing_address'],
            billing_city=data['billing_city'],
            billing_state=data['billing_state'],
            billing_postal_code=data['billing_postal_code'],
            billing_country=data['billing_country'],
            
            # Shipping info
            shipping_first_name=data.get('shipping_first_name') or data['billing_first_name'],
            shipping_last_name=data.get('shipping_last_name') or data['billing_last_name'],
            shipping_phone=data.get('shipping_phone') or data['billing_phone'],
            shipping_address=data.get('shipping_address') or data['billing_address'],
            shipping_city=data.get('shipping_city') or data['billing_city'],
            shipping_state=data.get('shipping_state') or data['billing_state'],
            shipping_postal_code=data.get('shipping_postal_code') or data['billing_postal_code'],
            shipping_country=data.get('shipping_country') or data['billing_country'],
            
            # Pricing
            subtotal=cart.subtotal,
            tax_amount=cart.tax_amount,
            discount_amount=cart.discount_amount,
            total_amount=cart.total,
            
            # Additional
            coupon_code=cart.coupon_code,
            notes=data.get('notes', ''),
            
            # Metadata
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                variant_name=cart_item.variant.name if cart_item.variant else '',
                quantity=cart_item.quantity,
                price=cart_item.price,
                tax_rate=cart_item.product.tax_rate,
                customization=cart_item.customization
            )
            
            # Update stock
            if cart_item.variant and hasattr(cart_item.variant, 'stock'):
                stock = cart_item.variant.stock
            else:
                stock = cart_item.product.stock
            
            stock.reserved_quantity += cart_item.quantity
            stock.save()
            
            # Update product sales count
            cart_item.product.sales_count += cart_item.quantity
            cart_item.product.save(update_fields=['sales_count'])
        
        # Create payment record
        Payment.objects.create(
            order=order,
            payment_method=data['payment_method'],
            status='pending',
            amount=order.total_amount,
            currency='USD'
        )
        
        # Create delivery record
        Delivery.objects.create(
            order=order,
            status='pending',
            delivery_latitude=float(data.get('shipping_latitude', 0)),
            delivery_longitude=float(data.get('shipping_longitude', 0))
        )
        
        # Clear cart
        cart.items.all().delete()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        # Check permissions
        if request.user.role not in ['admin', 'superadmin', 'vendor']:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        
        # Update timestamps
        if new_status == 'shipped':
            order.shipped_at = timezone.now()
        elif new_status == 'delivered':
            order.delivered_at = timezone.now()
        elif new_status == 'cancelled':
            order.cancelled_at = timezone.now()
            
            # Release reserved stock
            for item in order.items.all():
                if item.variant and hasattr(item.variant, 'stock'):
                    stock = item.variant.stock
                else:
                    stock = item.product.stock
                
                stock.reserved_quantity -= item.quantity
                stock.save()
        
        order.save()
        
        return Response(OrderSerializer(order).data)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        if order.status not in ['pending', 'processing']:
            return Response({
                'error': 'Cannot cancel order in current status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()
        
        # Release reserved stock
        for item in order.items.all():
            if item.variant and hasattr(item.variant, 'stock'):
                stock = item.variant.stock
            else:
                stock = item.product.stock
            
            stock.reserved_quantity -= item.quantity
            stock.save()
        
        return Response({'message': 'Order cancelled successfully'})


# Payment Views
class PaymentProcessView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get('order_id')
        payment = get_object_or_404(Payment, order_id=order_id, order__user=request.user)
        
        # Here you would integrate with actual payment gateway
        # For now, we'll simulate successful payment
        
        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.transaction_id = f"TXN-{timezone.now().timestamp()}"
        payment.save()
        
        # Update order status
        order = payment.order
        order.status = 'processing'
        order.paid_at = timezone.now()
        order.save()
        
        # Update stock (convert reserved to sold)
        for item in order.items.all():
            if item.variant and hasattr(item.variant, 'stock'):
                stock = item.variant.stock
            else:
                stock = item.product.stock
            
            stock.quantity -= item.quantity
            stock.reserved_quantity -= item.quantity
            stock.save()
        
        return Response(PaymentSerializer(payment).data)


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk, order__user=request.user)
        return Response(PaymentSerializer(payment).data)


# Delivery Views
class DeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk, order__user=request.user)
        return Response(DeliverySerializer(delivery).data)


class DeliveryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        if request.user.role not in ['admin', 'superadmin']:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        delivery = get_object_or_404(Delivery, pk=pk)
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Add to tracking history
            delivery.tracking_history.append({
                'status': request.data.get('status'),
                'timestamp': timezone.now().isoformat(),
                'location': {
                    'lat': request.data.get('current_latitude'),
                    'lng': request.data.get('current_longitude')
                }
            })
            delivery.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        # Check if user has purchased the product
        product = serializer.validated_data['product']
        user = self.request.user
        
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__status='delivered',
            product=product
        ).exists()
        
        serializer.save(
            user=user,
            is_verified_purchase=has_purchased
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ProductReviewsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        reviews = product.reviews.filter(is_approved=True)
        
        # Get review statistics
        stats = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id'),
            five_star=Count('id', filter=Q(rating=5)),
            four_star=Count('id', filter=Q(rating=4)),
            three_star=Count('id', filter=Q(rating=3)),
            two_star=Count('id', filter=Q(rating=2)),
            one_star=Count('id', filter=Q(rating=1))
        )
        
        serializer = ReviewSerializer(reviews, many=True)
        
        return Response({
            'reviews': serializer.data,
            'statistics': stats
        })


# Wishlist Views
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)


class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        wishlist, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            return Response(
                WishlistSerializer(wishlist).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Product already in wishlist'},
            status=status.HTTP_200_OK
        )


class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist.delete()
        return Response({'message': 'Removed from wishlist'})


# Coupon Views
class CouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )


class CouponValidateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        
        try:
            coupon = Coupon.objects.get(code=code)
            
            if not coupon.is_valid:
                return Response(
                    {'valid': False, 'message': 'Coupon is not valid'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'valid': True,
                'discount_type': coupon.discount_type,
                'discount_value': coupon.discount_value,
                'minimum_purchase_amount': coupon.minimum_purchase_amount
            })
        
        except Coupon.DoesNotExist:
            return Response(
                {'valid': False, 'message': 'Invalid coupon code'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ApplyCouponView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        cart_id = request.data.get('cart_id')
        
        cart = get_object_or_404(Cart, pk=cart_id)
        
        # Verify cart ownership
        if request.user.is_authenticated:
            if cart.user != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if cart.session_key != request.session.session_key:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            coupon = Coupon.objects.get(code=code)
            
            if not coupon.is_valid:
                return Response(
                    {'error': 'Coupon is not valid'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check minimum purchase amount
            if cart.subtotal < coupon.minimum_purchase_amount:
                return Response(
                    {'error': f'Minimum purchase amount is {coupon.minimum_purchase_amount}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate discount
            if coupon.discount_type == 'percentage':
                discount = (cart.subtotal * coupon.discount_value) / 100
                if coupon.maximum_discount_amount:
                    discount = min(discount, coupon.maximum_discount_amount)
            elif coupon.discount_type == 'fixed':
                discount = coupon.discount_value
            else:  # free_shipping
                discount = Decimal('0')
            
            cart.coupon_code = code
            cart.discount_amount = discount
            cart.save()
            
            return Response(CartSerializer(cart).data)
        
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Invalid coupon code'},
                status=status.HTTP_400_BAD_REQUEST
            )


# Analytics Views
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.role == 'customer':
            stats = {
                'total_orders': Order.objects.filter(user=user).count(),
                'pending_orders': Order.objects.filter(user=user, status='pending').count(),
                'wishlist_items': Wishlist.objects.filter(user=user).count(),
                'loyalty_points': user.loyalty_points
            }
        elif user.role == 'vendor':
            today = timezone.now().date()
            thirty_days_ago = today - timedelta(days=30)
            
            stats = {
                'total_products': Product.objects.filter(vendor=user).count(),
                'active_products': Product.objects.filter(vendor=user, is_active=True).count(),
                'total_orders': Order.objects.filter(items__product__vendor=user).distinct().count(),
                'pending_orders': Order.objects.filter(
                    items__product__vendor=user,
                    status='pending'
                ).distinct().count(),
                'revenue_today': OrderItem.objects.filter(
                    product__vendor=user,
                    order__created_at__date=today,
                    order__status='delivered'
                ).aggregate(total=Sum('price'))['total'] or 0,
                'revenue_month': OrderItem.objects.filter(
                    product__vendor=user,
                    order__created_at__date__gte=thirty_days_ago,
                    order__status='delivered'
                ).aggregate(total=Sum('price'))['total'] or 0
            }
        else:  # admin
            today = timezone.now().date()
            thirty_days_ago = today - timedelta(days=30)
            
            stats = {
                'total_users': User.objects.count(),
                'total_products': Product.objects.count(),
                'total_orders': Order.objects.count(),
                'pending_orders': Order.objects.filter(status='pending').count(),
                'revenue_today': Order.objects.filter(
                    created_at__date=today,
                    status='delivered'
                ).aggregate(total=Sum('total_amount'))['total'] or 0,
                'revenue_month': Order.objects.filter(
                    created_at__date__gte=thirty_days_ago,
                    status='delivered'
                ).aggregate(total=Sum('total_amount'))['total'] or 0,
                'new_users_today': User.objects.filter(date_joined__date=today).count(),
                'new_users_month': User.objects.filter(date_joined__date__gte=thirty_days_ago).count()
            }
        
        return Response(stats)


class SalesReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role not in ['vendor', 'admin', 'superadmin']:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
        
        # Build query
        if request.user.role == 'vendor':
            orders = Order.objects.filter(
                items__product__vendor=request.user,
                created_at__date__range=[start_date, end_date]
            ).distinct()
        else:
            orders = Order.objects.filter(
                created_at__date__range=[start_date, end_date]
            )
        
        # Generate report
        report = {
            'period': {
                'start': start_date,
                'end': end_date
            },
            'summary': {
                'total_orders': orders.count(),
                'completed_orders': orders.filter(status='delivered').count(),
                'cancelled_orders': orders.filter(status='cancelled').count(),
                'total_revenue': orders.filter(
                    status='delivered'
                ).aggregate(total=Sum('total_amount'))['total'] or 0,
                'average_order_value': orders.filter(
                    status='delivered'
                ).aggregate(avg=Avg('total_amount'))['avg'] or 0
            },
            'top_products': [],
            'daily_sales': []
        }
        
        # Top products
        if request.user.role == 'vendor':
            top_products = OrderItem.objects.filter(
                product__vendor=request.user,
                order__created_at__date__range=[start_date, end_date],
                order__status='delivered'
            ).values('product__name').annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('price')
            ).order_by('-total_revenue')[:10]
        else:
            top_products = OrderItem.objects.filter(
                order__created_at__date__range=[start_date, end_date],
                order__status='delivered'
            ).values('product__name').annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('price')
            ).order_by('-total_revenue')[:10]
        
        report['top_products'] = list(top_products)
        
        # Daily sales
        current_date = start_date
        while current_date <= end_date:
            daily_orders = orders.filter(created_at__date=current_date)
            report['daily_sales'].append({
                'date': current_date,
                'orders': daily_orders.count(),
                'revenue': daily_orders.filter(
                    status='delivered'
                ).aggregate(total=Sum('total_amount'))['total'] or 0
            })
            current_date += timedelta(days=1)
        
        return Response(report)
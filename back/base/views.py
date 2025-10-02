# back/base/views.py - COMPLETE FILE

from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.db import transaction
import logging

from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, 
    Review, Wishlist
)
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    CartSerializer, CartItemSerializer, AddToCartSerializer,
    UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer,
    OrderItemSerializer, ReviewSerializer, WishlistSerializer
)
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            products = self.queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        else:
            products = self.queryset.none()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart
    
    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart = self.get_cart(request)
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        
        # Check stock
        if product.stock_quantity < quantity:
            return Response(
                {'error': 'Not enough stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartSerializer(cart).data)


class CartItemView(APIView):
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                return None
            cart = Cart.objects.filter(session_key=session_key).first()
        return cart
    
    def patch(self, request, item_id):
        cart = self.get_cart(request)
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        # Check stock
        if cart_item.product.stock_quantity < quantity:
            return Response(
                {'error': 'Not enough stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    def delete(self, request, item_id):
        cart = self.get_cart(request)
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    """
    Handle checkout process with proper stock management and transactions.
    Supports both authenticated users and guest checkout.
    """
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        """Retrieve cart for authenticated user or guest session."""
        if request.user.is_authenticated:
            return Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                return None
            return Cart.objects.filter(session_key=session_key).first()
    
    def validate_cart(self, cart):
        """Validate that cart exists and has items."""
        if not cart:
            raise ValidationError({
                'error': 'Cart not found',
                'code': 'CART_NOT_FOUND'
            })
        
        if not cart.items.exists():
            raise ValidationError({
                'error': 'Cart is empty',
                'code': 'CART_EMPTY'
            })
    
    def validate_stock_availability(self, cart_items):
        """Validate stock availability for all cart items with row locking."""
        validated_items = []
        
        for cart_item in cart_items:
            # Lock the product row to prevent concurrent modifications
            product = Product.objects.select_for_update().get(id=cart_item.product.id)
            
            # Check if product is still active
            if not product.is_active:
                raise ValidationError({
                    'error': f'Product "{product.name}" is no longer available',
                    'code': 'PRODUCT_UNAVAILABLE',
                    'product_id': str(product.id)
                })
            
            # Check stock availability
            if product.stock_quantity < cart_item.quantity:
                raise ValidationError({
                    'error': f'Not enough stock for "{product.name}". Available: {product.stock_quantity}, Requested: {cart_item.quantity}',
                    'code': 'INSUFFICIENT_STOCK',
                    'product_id': str(product.id),
                    'available_quantity': product.stock_quantity,
                    'requested_quantity': cart_item.quantity
                })
            
            validated_items.append({
                'cart_item': cart_item,
                'product': product
            })
        
        return validated_items
    
    def create_order_items(self, order, validated_items):
        """Create order items and update product stock."""
        order_items = []
        
        for item in validated_items:
            cart_item = item['cart_item']
            product = item['product']
            
            # Create order item
            order_item = OrderItem(
                order=order,
                product=product,
                product_name=product.name,
                quantity=cart_item.quantity,
                price=product.price
            )
            order_items.append(order_item)
            
            # Update stock quantity
            product.stock_quantity -= cart_item.quantity
            product.save(update_fields=['stock_quantity'])
            
            logger.info(
                f"Order item created: {product.name} x{cart_item.quantity} "
                f"for order {order.order_number}"
            )
        
        # Bulk create order items for better performance
        OrderItem.objects.bulk_create(order_items)
        
        return order_items
    
    def post(self, request):
        """Process checkout and create order."""
        try:
            # Get and validate cart
            cart = self.get_cart(request)
            self.validate_cart(cart)
            
            # Validate order data
            serializer = CreateOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Get cart items with product relations
            cart_items = cart.items.select_related('product').all()
            
            # Start atomic transaction
            with transaction.atomic():
                # Validate stock availability (with row locking)
                validated_items = self.validate_stock_availability(cart_items)
                
                # Calculate total (recalculate to ensure accuracy)
                total_amount = sum(
                    item['product'].price * item['cart_item'].quantity
                    for item in validated_items
                )
                
                # Create order
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    total_amount=total_amount,
                    **serializer.validated_data
                )
                
                logger.info(
                    f"Order created: {order.order_number} for "
                    f"{'user ' + request.user.email if request.user.is_authenticated else 'guest'}"
                )
                
                # Create order items and update stock
                self.create_order_items(order, validated_items)
                
                # Clear cart after successful order creation
                cart.items.all().delete()
                logger.info(f"Cart cleared for order {order.order_number}")
            
            # Return order details
            return Response(
                {
                    'status': 'success',
                    'message': 'Order placed successfully',
                    'data': OrderSerializer(order).data
                },
                status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            logger.warning(f"Checkout validation error: {str(e.detail)}")
            return Response(
                {
                    'status': 'error',
                    'error': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Product.DoesNotExist:
            logger.error("Product not found during checkout")
            return Response(
                {
                    'status': 'error',
                    'error': 'One or more products in your cart are no longer available',
                    'code': 'PRODUCT_NOT_FOUND'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}", exc_info=True)
            return Response(
                {
                    'status': 'error',
                    'error': 'An error occurred while processing your order. Please try again.',
                    'code': 'CHECKOUT_ERROR'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_id'))
    
    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        serializer.save(user=self.request.user, product=product)


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            return Response(
                WishlistSerializer(wishlist_item).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Product already in wishlist'},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, product_id):
        wishlist_item = get_object_or_404(
            Wishlist,
            user=request.user,
            product_id=product_id
        )
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
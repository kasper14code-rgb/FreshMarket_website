from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_total_price']
    list_filter = ['cart__is_active']
    search_fields = ['product__name', 'cart__user__username']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product', 'quantity', 'ordered_at', 'is_completed']
#     list_filter = ['is_completed', 'ordered_at']
#     search_fields = ['user__username', 'product__name']
#     list_editable = ['is_completed']
#     readonly_fields = ['ordered_at']
#     date_hierarchy = 'ordered_at'
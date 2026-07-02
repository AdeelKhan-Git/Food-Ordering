from rest_framework import serializers
from restaurants.models import Category,MenuItem,Restaurants,Deal,DealItem

class AllRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['id','name','created_by','created_at']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug','created_by','created_at','updated_at']
        extra_kwargs = {
            'name':{'required':True}
        }

class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_by','created_at']
 
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source="category_id", read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','name','description','price','image','is_available','is_featured','created_by','restaurant_id','created_at','updated_at','category']
        extra_kwargs ={
            'name':{'required':True},
            'price':{'required':True}
        }

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only = True)
    class Meta:
        model = Restaurants
        fields = ['id','name','description','address','image','is_featured','is_active','created_by','created_at','updated_at','menu_items']
        extra_kwargs ={
            'name':{'required':True}
        }






class DealItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer( read_only=True)
    class Meta:
        model = DealItem
        fields = ['id','deal_id','menu_item','quantity']

class DealSerializer(serializers.ModelSerializer):
    items = DealItemSerializer(many=True,read_only=True)
    class Meta:
        model = Deal
        fields = ['id','name','description','combo_price','image','is_active','is_featured','created_by','restaurant_id','created_at','updated_at','items']
        extra_kwargs ={
            'name':{'required':True},
            'combo_price':{'required':True}
        }
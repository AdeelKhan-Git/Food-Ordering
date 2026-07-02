from rest_framework import serializers
from restaurants.models import Category,MenuItem,Restaurants,Deal,DealItem

class AllRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['id','name','created_by','created_at']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug','created_at','updated_at']
        extra_kwargs = {
            'name':{'required':True}
        }

class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_by','created_at']
 
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source="category_id", read_only=True)
    restaurant = CategorySerializer(source="restaurant_id", read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','restaurant_id','category_id','name','description','price','image','is_available','is_featured','restaurant','category','created_at','updated_at',]
        extra_kwargs ={
            'name':{'required':True},
            'price':{'required':True},
            'restaurant_id':{'required':True},
            'category_id':{'required':True}
        }

class AllMenuItemSerializer(serializers.ModelSerializer):
    restaurant = AllRestaurantSerializer(source = "restaurant_id",read_only=True)
    category = CategorySerializer(source="category_id", read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','name','price','image','restaurant','category']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only = True)
    class Meta:
        model = Restaurants
        fields = ['id','name','description','address','image','is_featured','is_active','menu_items','created_at','updated_at',]
        extra_kwargs ={
            'name':{'required':True}
        }






class DealItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(source = 'menu_item_id', read_only=True)
    class Meta:
        model = DealItem
        fields = ['id','deal_id','quantity',"menu_item_id",'menu_item',]
        extra_kwargs = {
            "deal_id": {"required": True},
            "menu_item_id": {"required": True},
            "quantity": {"required": True},
        }


class DealSerializer(serializers.ModelSerializer):
    items = DealItemSerializer(source = 'deal_item',many=True,read_only=True)
    class Meta:
        model = Deal
        fields = ['id','name','description','combo_price','image','is_active','is_featured','created_by','restaurant_id','created_at','updated_at','items']
        extra_kwargs ={
            'name':{'required':True},
            'combo_price':{'required':True},
            'restaurant_id': {'required': True},
        }
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurants, Category,MenuItem,Deal,DealItem
from restaurants.serializer import CategorySerializer,AllCategorySerializer,AllRestaurantSerializer ,RestaurantSerializer, MenuItemSerializer,AllMenuItemSerializer,DealItemSerializer, DealSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

#--------------- Category ----------------------

class CreateCategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
            request_body=CategorySerializer,
            responses={201: CategorySerializer}
    )
    
    def post(self, request):
        try:
            serializer = CategorySerializer(data =request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(created_by= request.user)

            return Response({"message":"Category Added","data":serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetCategoryView(APIView):
    def get(self, request, cat_id):
        try:
            restaurants = Restaurants.objects.filter(menu_items__category_id=cat_id).select_related("created_by").only("id", "name", "created_by", "created_at").distinct()
            

            data = AllRestaurantSerializer(restaurants, many=True).data

            return Response(
                {"data": data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class GetAllCategoryView(APIView):

    def get(self,request):
        try:
            category = Category.objects.select_related('created_by').only('name','created_by','created_at')

            data = AllCategorySerializer(category, many=True).data

            return Response({"data":data}, status= status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class UpdateCategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def patch(self, request,cat_id):
        try:
            category = Category.objects.select_related('created_by').get(id =cat_id) 
            serializer = CategorySerializer(category, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save(updated_by = request.user)

            return Response({"message":"Category Updated","data":serializer.data},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error":"Category not Found"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class DeleteCategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request,cat_id):
        try:
            category = Category.objects.select_related('created_by').get(id=cat_id)

            serializer = CategorySerializer(category).data

            category.delete()
            return Response({"message":"Category Deleted","data":serializer})
        except Category.DoesNotExist:
            return Response({"error":"Category not Found"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        


#----------------Restaurant------------------------------

class CreateRestuarantView(APIView):
    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
            request_body=RestaurantSerializer,
            responses={201: RestaurantSerializer}
    )

    def post(self,request):
        try:
            serializer = RestaurantSerializer(data =request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(created_by =request.user)
            return Response({"message":"Resturant Added","data":serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class GetAllRestaurantView(APIView):
    def get(self, request):
        try:
            restaurants =  Restaurants.objects.select_related('created_by').only('name','created_by','created_at')

            serializer= AllRestaurantSerializer(restaurants,many =True)

            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class GetRestaurantView(APIView):
    def get(self, request, rest_id):
        try:
            restaurant = Restaurants.objects.select_related('created_by').prefetch_related("menu_items__category_id").get(id = rest_id)
            serializer = RestaurantSerializer(restaurant)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except Restaurants.DoesNotExist:
            return Response({"error":"Restaurant not Found"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class UpdateRestaurantView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def patch(self,request,rest_id):
        try:
            restaurant = Restaurants.objects.select_related('created_by').get(id = rest_id)

            serailizer = RestaurantSerializer(restaurant, data=request.data, partial =True)
            serailizer.is_valid(raise_exception=True)
            serailizer.save(updated_by = request.user)

            return Response({"message":"Restaurant Updated","data":serailizer.data},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Restaurants.DoesNotExist:
            return Response({"error":"Restaurant not Found"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class DeleteRestaurantView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request,rest_id):
        try:
            restaurant = Restaurants.objects.select_related('created_by').get(id=rest_id)

            serializer = RestaurantSerializer(restaurant).data

            restaurant.delete()
            return Response({"message":"Restaurant Deleted","data":serializer})
        except Restaurants.DoesNotExist:
            return Response({"error":"Restaurant not Found"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
#---------------Menu Item----------------------

class CreateMenuItemView(APIView):
    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
            request_body=MenuItemSerializer,
            responses={201: MenuItemSerializer}
    )
    def post(self, request):
        try:
            serialzer = MenuItemSerializer(data = request.data)
            serialzer.is_valid(raise_exception=True)
            serialzer.save(created_by = request.user)
            return Response({"Message":"Menu Item Added","data":serialzer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)

class GetAllMenuItemsView(APIView):
    def get(self, request):
        try:
            menu_items = MenuItem.objects.select_related('created_by','restaurant_id','category_id').only('id','name','created_by','restaurant_id','category_id')

            serializer = AllMenuItemSerializer(menu_items,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class GetMenuItemView(APIView):
    def get(self,request,menu_id):
        try:
            menu = MenuItem.objects.select_related('restaurant_id','category_id').get(id=menu_id)
            serializer = MenuItemSerializer(menu)

            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response({"error":"Menu Item not Found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class UpdateMenuItemView(APIView):
    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
            request_body=MenuItemSerializer,
            responses={201: MenuItemSerializer}
    )
    def patch(self, request,menu_id):
        try:
            menu = MenuItem.objects.get(id=menu_id)

            serializer = MenuItemSerializer(menu, data = request.data, partial =True)
            serializer.is_valid(raise_exception=True)
            serializer.save(updated_by = request.user)
            return Response({"message":"Updated Menu Item","data":serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except MenuItem.DoesNotExist:
            return Response({"error":"Menu Item not Found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class DeleteMenuItemView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, menu_id):
        try:
            menu = MenuItem.objects.get(id=menu_id)
            serializer = MenuItemSerializer(menu)
            menu.delete()
            return Response({"message":"Menu Item Deleted","data":serializer.data}, status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response({"error":"Menu Item not Found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class CreateDealView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=DealSerializer,
        responses={201: DealSerializer}
    )
    def post(self, request):
        try:
            serializer = DealSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)

            return Response({"message": "Deal Created","data": serializer.data},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class GetDealView(APIView):

    def get(self, request, deal_id):
        try:
            deal = Deal.objects.select_related("restaurant_id", "created_by").prefetch_related("deal_item__menu_item_id").get(id=deal_id)

            serializer = DealSerializer(deal)

            return Response({"data": serializer.data},status=status.HTTP_200_OK)

        except Deal.DoesNotExist:
            return Response({"error": "Deal not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class GetAllDealView(APIView):

    def get(self, request):
        try:
            deals = Deal.objects.select_related("restaurant_id", "created_by").prefetch_related("deal_item__menu_item_id")
            serializer = DealSerializer(deals, many=True)

            return Response({"data": serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class UpdateDealView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=DealSerializer,
        responses={200: DealSerializer}
    )
    def patch(self, request, deal_id):
        try:
            deal = Deal.objects.get(id=deal_id)

            serializer = DealSerializer(deal,data=request.data,partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save(updated_by =request.user)

            return Response({"message": "Deal Updated","data": serializer.data},status=status.HTTP_200_OK)

        except Deal.DoesNotExist:
            return Response({"error": "Deal not found"},status=status.HTTP_404_NOT_FOUND)


class DeleteDealView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, deal_id):
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.delete()

            return Response({"message": "Deal Deleted"},status=status.HTTP_200_OK)

        except Deal.DoesNotExist:
            return Response({"error": "Deal not found"},status=status.HTTP_404_NOT_FOUND)


#--------Deal Item
class CreateDealItemView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=DealItemSerializer,
        responses={201: DealItemSerializer}
    )
    def post(self, request):
        try:
            serializer = DealItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            deal = serializer.validated_data['deal_id']
            menu_item = serializer.validated_data['menu_item_id']

            if deal.restaurant_id.id != menu_item.restaurant_id.id:
                return Response({"error":"This menu item does not belong to the selected restaurant"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({"message": "Deal Item Added","data": serializer.data},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    
class GetDealItemView(APIView):

    def get(self, request, item_id):
        try:
            item = DealItem.objects.select_related("deal_id","menu_item_id").get(id=item_id)

            serializer = DealItemSerializer(item)

            return Response({"data": serializer.data},status=status.HTTP_200_OK)

        except DealItem.DoesNotExist:
            return Response({"error": "Deal Item not found"},status=status.HTTP_404_NOT_FOUND)

class GetAllDealItemView(APIView):

    def get(self, request):
        try:
            items = DealItem.objects.select_related("deal_id","menu_item_id")

            serializer = DealItemSerializer(items, many=True)

            return Response({"data": serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class UpdateDealItemView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=DealItemSerializer,
        responses={200: DealItemSerializer}
    )
    def patch(self, request, item_id):
        try:
            item = DealItem.objects.get(id=item_id)

            serializer = DealItemSerializer(item,data=request.data,partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Deal Item Updated","data": serializer.data},status=status.HTTP_200_OK)

        except DealItem.DoesNotExist:
            return Response({"error": "Deal Item not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class DeleteDealItemView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, item_id):
        try:
            item = DealItem.objects.get(id=item_id)
            item.delete()

            return Response({"message": "Deal Item Deleted"},status=status.HTTP_200_OK)

        except DealItem.DoesNotExist:
            return Response({"error": "Deal Item not found"},status=status.HTTP_404_NOT_FOUND)

class GlobalSearchView(APIView):
    def get(self, request):

        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({'error':'search query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        restaurants = Restaurants.objects.filter(name__icontains =query).prefetch_related('menu_items__category_id')
        menuitem = MenuItem.objects.filter(name__icontains=query, is_available=True).select_related('restaurant_id','category_id')
        category = Category.objects.filter(name__icontains=query).prefetch_related('menu_items__restaurant_id')

        return Response({
            "restaurants":AllRestaurantSerializer(restaurants, many=True).data,
            "categories":AllCategorySerializer(category, many=True).data,
            "menuitems":AllMenuItemSerializer(menuitem, many=True).data,
        }, status=status.HTTP_200_OK)

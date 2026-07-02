from django.urls import path
from restaurants.views import GetCategoryView, CreateCategoryView,GetAllCategoryView,UpdateCategoryView,DeleteCategoryView,CreateRestuarantView,GetAllRestaurantView,UpdateRestaurantView,GetRestaurantView,DeleteRestaurantView,CreateMenuItemView,GetAllMenuItemsView,GetMenuItemView,UpdateMenuItemView,DeleteMenuItemView

urlpatterns = [
   #----- category 
   path('create-category/',CreateCategoryView.as_view(), name ='create-category'),
   path('category/<int:cat_id>',GetCategoryView.as_view(), name ='get-category'),
   path('all-category',GetAllCategoryView.as_view(), name = 'all-category'),
   path('update-category/<int:cat_id>/',UpdateCategoryView.as_view(), name = 'update-category'),
   path('delete-category/<int:cat_id>/',DeleteCategoryView.as_view(), name = 'delete-category'),

   #----- restaurants
   path('create-restaurant/',CreateRestuarantView.as_view(), name ='create-restaurant'),
   path('restaurant/<int:rest_id>',GetRestaurantView.as_view(), name ='get-restaurant'),
   path('all-restaurant',GetAllRestaurantView.as_view(), name = 'all-restaurant'),
   path('update-restaurant/<int:rest_id>/',UpdateRestaurantView.as_view(), name = 'update-restaurant'),
   path('delete-restaurant/<int:rest_id>/',DeleteRestaurantView.as_view(), name = 'delete-restaurant'),

   #--------- Menu items
   path('create-menuitem/',CreateMenuItemView.as_view(), name ='create-menuitem'),
   path('menuitem/<int:menu_id>',GetMenuItemView.as_view(), name ='get-menuitem'),
   path('all-menuitem',GetAllMenuItemsView.as_view(), name = 'all-menuitem'),
   path('update-menuitem/<int:menu_id>/',UpdateMenuItemView.as_view(), name = 'update-menuitem'),
   path('delete-menuitem/<int:menu_id>/',DeleteMenuItemView.as_view(), name = 'delete-menuitem'),

]
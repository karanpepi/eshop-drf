from django.urls import path
from rest_apis import views


urlpatterns = [
    path('showproducts',views.ShowAllProducts.as_view()),
    path('register',views.UserRegister.as_view()),
    path('category',views.CategoryDetails.as_view()),
    path('category/<id>',views.CategoryActions.as_view()),
    path('brand',views.BrandDetails.as_view()),
    path('brand/<id>',views.BrandActions.as_view()),
    path('product',views.ProductDetailInfo.as_view()),
    path('product/<id>',views.ProductActions.as_view()),
    path('filter_category/<id>',views.FilterCategory.as_view()),
    path('filter_brand/<id>',views.FilterBrand.as_view()),
]
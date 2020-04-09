from django.urls import path
from rest_apis import views


urlpatterns = [
    path('register',views.UserRegister.as_view()),
    path('category',views.CategoryDetails.as_view()),
    path('category/<id>',views.CategoryActions.as_view()),
    path('brand',views.BrandDetails.as_view()),
    path('brand/<id>',views.BrandActions.as_view()),
    path('product',views.ProductDetailInfo.as_view()),
    path('product/<id>',views.ProductActions.as_view()),
]
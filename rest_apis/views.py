from django.shortcuts import render
from rest_apis.serializers import (RegisterSerializer,BrandSerializer,
    CategorySerializer,ProductSerializer,ImageSerializer)

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_apis.models import Register,Brand,Category,Product,Images
from rest_apis.permission import CustomAuthentication
from django.http import Http404,JsonResponse,HttpResponse
from eshops_api.settings import MEDIA_ROOT,URL
from django.db import connection
import json


from django.core.files.storage import FileSystemStorage

from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

# Create your views here.

class UserRegister(views.APIView):
    def post(self,request):
        data = request.POST
        serializer= RegisterSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUp(views.APIView):
    pass

class ProductDetailInfo(views.APIView):
    # authentication_classes = (CustomAuthentication,)
    def post(self,request):
        product_serializer = ProductSerializer(data=request.data)

        file_list=[]
        for count,file_obj in enumerate(request.FILES.getlist("img_path")):
            if file_obj.name.split(".")[1] in ['jpeg','png','jpg','pdf']:
                file_list.append(file_obj)
                # filename = fs.save(MEDIA_ROOT+file_obj.name,file_obj)
            else:
                return Response({"error":"Extension not supported"},status=status.HTTP_400_BAD_REQUEST)

        if product_serializer.is_valid():
            product = product_serializer.save()
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
        for fileobj in file_list:
            fs = FileSystemStorage()
            filename = fs.save(MEDIA_ROOT+fileobj.name,fileobj)
            Images.objects.create(img_path=URL+fileobj.name,img_pid=product.p_id)
            
        image_objects = Images.objects.filter(img_pid = product.p_id).values()
        #change the serializer response to show proper data
        new_dict = {'results': list(image_objects)}
        new_dict.update(product_serializer.data)
        return JsonResponse(new_dict)

    def get(self, request, format=None):
        all_product = Product.objects.all()
        serializer = ProductSerializer(all_product, many=True)
        return Response(serializer.data)

class ProductActions(views.APIView):
    def get_object(self, pk):
         try:
             return Product.objects.get(pk=pk)
         except Product.DoesNotExist:
             raise Http404

    def get(self, request, id):
        product = self.get_object(id)
        product = ProductSerializer(product)
        return Response(product.data)


    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BrandDetails(views.APIView):
    def post(self,request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrandActions(views.APIView):
    def get_object(self, pk):
         try:
             return Brand.objects.get(pk=pk)
         except Brand.DoesNotExist:
             raise Http404

    def get(self, request, id):
         brand = self.get_object(id)
         brand = BrandSerializer(brand)
         return Response(brand.data)


    def put(self, request, id, format=None):
        brand = self.get_object(id)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        brand = self.get_object(id)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetails(views.APIView):
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryActions(views.APIView):
    def get_object(self, pk):
         try:
             return Category.objects.get(pk=pk)
         except Category.DoesNotExist:
             raise Http404

    def get(self, request, id):
         category = self.get_object(id)
         category = CategorySerializer(category)
         return Response(category.data)


    def put(self, request, id, format=None):
        category = self.get_object(id)
        serializer = BrandSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShowAllProducts(views.APIView):
    #try a join query here to join brand,category,images,product table to display
    #all products
    def get(self,request):
        cursor = connection.cursor()
        cursor.execute(''' select pr.p_id,pr.p_name,pr.p_mrp,pr.p_dis,pr.p_descrip,
            br.brand_name,
            br.id as br_id,cat.cat_name,
            cat.id as cat_id,img.img_path from product pr 
            inner join brand br on (br.id=pr.p_id) 
            inner join category cat on (cat.id=pr.p_id) 
            inner join images img on (img.img_pid=pr.p_id);
 ''')
        rows = cursor.fetchall()
        cursor.close()
        result = []
        keys = ('product_id','product_name','product_mrp','product_dis',
            'product_descrip','brand_name','brand_id','category_name','category_id','image_path')
        for row in rows:
            result.append(dict(zip(keys,row)))
        json_data = json.dumps(result)
        return HttpResponse(json_data, content_type="application/json")
        



        



class JSONWebTokenAPIOverride(ObtainJSONWebToken):
    """
    Override JWT
    """
    # remove the hard coded input value later
    def post(self, request):
        print(request.data)
        result = Register.objects.filter(email="kar8@gmail.com",password="karan1992")[:1].get()
        payload = jwt_payload_handler(result)
        token = jwt_encode_handler(payload)
        return Response({'token': token})



from rest_framework import serializers
from rest_apis.models import Register,Brand,Category,Product,Images
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    # bill_details = serializers.SerializerMethodField()


    class Meta:
        model = Register
        fields = "__all__"
    
    def validate(self,data):
        if data["password"] != data["confirmpass"]:
            raise ValidationError({"password_confpassword":["Password and Confirmpass does not match"]})
    
        return data

    # def get_bill_details(self,obj):
    #     return "sdasd" + "/tts/%s/%s"%(obj.firstname,obj.lastname)
            

class RegisterToken(serializers.ModelSerializer):


    class Meta:
        model = Register
        fields = ['email','password']


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
from rest_framework import serializers
from .models import Superfrog, Admin, Customer, Appearance, Event

class SuperfrogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superfrog
        fields = "__all__"

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        return Event(**validated_data)

class AppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appearance
        fields = "__all__"

    def create(self, validated_data):
        return Appearance(**validated_data)

class AppearanceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appearance
        fields = ('id','name','date','start_time','end_time','location','status')


#Serializer for custom user model
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            #prevent logging user out after changing password
            #update_session_auth_hash(self.context.get('request'), instance)

            return instance
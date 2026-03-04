from rest_framework import serializers
from .models import Coleccion, Bookmark
import re
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'titulo', 'url', 'descripcion', 'imagen_url', 'coleccion', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']  

    def validate_titulo(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El título debe contener más de 2 caracteres")
        if len(value.strip()) > 100:
            raise serializers.ValidationError("El título no debe exceder 100 caracteres")
        return value

    def validate_url(self, value):
        if not (value.startswith("http://") or value.startswith("https://")):
            raise serializers.ValidationError("La URL debe empezar con http:// o https://")
        if len(value) < 10:
            raise serializers.ValidationError("La URL es demasiado corta")
        return value
    
    def validate_imagen_url(self, value):
        if value:  # Solo validar si se proporcionó
            if not (value.startswith("http://") or value.startswith("https://")):
                raise serializers.ValidationError("La imagen_url debe empezar con http:// o https://")
        return value
    
    def validate_coleccion(self, value):
        request = self.context.get('request')
        if request and request.user:
            if value.usuario != request.user:
                raise serializers.ValidationError("La colección no pertenece al usuario autenticado")
        return value
    
    def validate(self, data):
        url = data.get('url')
        imagen_url = data.get('imagen_url')
        
        if url and imagen_url and url == imagen_url:
            raise serializers.ValidationError({
                "imagen_url": "La URL de imagen debe ser diferente a la URL del bookmark"
            })
        return data

class ColeccionSerializer(serializers.ModelSerializer):
    bookmarks_count = serializers.IntegerField(source='bookmarks.count', read_only=True)
    bookmarks = BookmarkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Coleccion
        fields = ['id', 'nombre', 'descripcion', 'usuario', 'fecha_creacion', 'bookmarks', 'bookmarks_count']
        read_only_fields = ['id', 'usuario', 'fecha_creacion', 'bookmarks_count']

    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe contener más de 2 caracteres")
        if len(value) > 100:
            raise serializers.ValidationError("El nombre no debe exceder 100 caracteres")
        if not re.match(r'^[A-Za-z0-9\s]+$', value):
            raise serializers.ValidationError("El nombre solo debe contener letras, números y espacios")
        return value
    
    def validate(self, data):
        request = self.context.get('request')
        nombre = data.get('nombre')
        
        if request and request.user and nombre:
            # Verificar si ya existe una colección con este nombre para este usuario
            queryset = Coleccion.objects.filter(
                nombre__iexact=nombre,  
                usuario=request.user
            )
            
            # Si es actualización, excluir esta instancia
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    "nombre": "Ya tienes una colección con este nombre"
                })
        
        return data
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("El password2 debe ser igual al password")
        return data
    
    def validate_username(self, value):
        value = value.strip()
        if len(value) < 4:
            raise serializers.ValidationError("El nombre debe contener más de 3 caracteres")
        if len(value) > 20:
            raise serializers.ValidationError("El nombre no debe exceder 20 caracteres")
        if not re.match(r'^[A-Za-z0-9_]+$', value):
            raise serializers.ValidationError("El nombre solo debe contener letras, números y guiones bajos")
        return value
    
    def validate_email(self, value):
        email = value.strip()
        
        queryset = User.objects.filter(
            email__iexact=email
        )
            
        if queryset.exists():
            raise serializers.ValidationError({"Ya existe un usuario con el mismo email"})
        
        return email

    def validate_first_name(self, value):
        value = value.strip()
        if value:
            if len(value) < 2:
                raise serializers.ValidationError("El firstname debe contener más de 1 caracter")
            if not re.match(r'^[A-Za-z\s]+$', value):
                raise serializers.ValidationError("El firstname solo debe contener letras y espacios")
        return value
    
    def validate_last_name(self, value):
        value = value.strip()
        if value:
            if len(value) < 2:
                raise serializers.ValidationError("El lastname debe contener más de 1 caracter")
            if not re.match(r'^[A-Za-z\s]+$', value):
                raise serializers.ValidationError("El lastname solo debe contener letras y espacios")
        return value
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Coleccion, Bookmark
from .serializers import ColeccionSerializer, BookmarkSerializer, UserSerializer
from django.shortcuts import render

class ColeccionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        colecciones = Coleccion.objects.filter(usuario=request.user)
        serializer = ColeccionSerializer(colecciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ColeccionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ColeccionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        coleccion = get_object_or_404(Coleccion, pk=pk, usuario=request.user)
        serializer = ColeccionSerializer(coleccion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        coleccion = get_object_or_404(Coleccion, pk=pk, usuario=request.user)
        serializer = ColeccionSerializer(coleccion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        coleccion = get_object_or_404(Coleccion, pk=pk, usuario=request.user)
        serializer = ColeccionSerializer(coleccion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        coleccion = get_object_or_404(Coleccion, pk=pk, usuario=request.user)
        coleccion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookmarks = Bookmark.objects.filter(coleccion__usuario=request.user)
        coleccion_id = request.query_params.get('coleccion')
        if coleccion_id:
            bookmarks = bookmarks.filter(coleccion_id=coleccion_id)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            coleccion_id = request.data.get('coleccion')
            coleccion = get_object_or_404(Coleccion, id=coleccion_id, usuario=request.user)
            serializer.save(coleccion=coleccion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarkDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, coleccion__usuario=request.user)
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, coleccion__usuario=request.user)
        serializer = BookmarkSerializer(bookmark, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, coleccion__usuario=request.user)
        serializer = BookmarkSerializer(bookmark, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, coleccion__usuario=request.user)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "mensaje": "Usuario creado exitosamente",
                "usuario": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def index_view(request):
    return render(request, 'frontend/index.html')

def login_view(request):
    return render(request, 'frontend/login.html')

def registro_view(request):
    return render(request, 'frontend/registro.html')

def dashboard_view(request):
    return render(request, 'frontend/dashboard.html')
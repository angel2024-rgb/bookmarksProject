from django.urls import path
from .views import ColeccionListCreateView, ColeccionDetailView, BookmarkListCreateView, BookmarkDetailView, RegistroView

urlpatterns = [
    path('colecciones/', ColeccionListCreateView.as_view(), name='coleccion-list-create'),
    path('colecciones/<int:pk>/', ColeccionDetailView.as_view(), name='coleccion-detail'),
    path('bookmarks/', BookmarkListCreateView.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>/', BookmarkDetailView.as_view(), name='bookmark-detail'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
app_name = 'store'

urlpatterns = [
    # Vistas públicas
    path('', views.base, name='base'),
    path('productos/', views.productos, name='productos'),
    path('categorias/', views.categorias, name='categorias'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar_item/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),

    # Vistas de administración (CRUDs, restringidas a usuarios autenticados)
    path('base_sesion/', views.base_sesion, name='base_sesion'),
    path('ver_carritos/', views.ver_carritos, name='ver_carritos'),
    path('ver_carrito_dni/<str:dni_cliente>/', views.ver_carrito_por_dni, name='ver_carrito_dni'),


    # CRUD de Productos
    path('crud_productos/', views.crud_productos, name='crud_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # CRUD de Categorías
    path('crud_categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Gestión de Stock
    path('stock/', views.gestionar_stock, name='stock'),
    path('stock/actualizar/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
path('ver_carrito/', views.ver_carrito, name='ver_carrito'),

    # Cerrar Sesión
    path('cerrar_sesion/', LogoutView.as_view(next_page='store:iniciar_sesion'), name='cerrar_sesion'),
    path('eliminar_carrito/<int:carrito_id>/', views.eliminar_carrito, name='eliminar_carrito'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
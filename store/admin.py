from django.contrib import admin
from .models import Categoria, Producto, Carrito, CarritoItem

# Personalización de la administración de la categoría
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Personalización de la administración del producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

# Personalización de la administración del carrito
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('dni_cliente', 'creado')  # Muestra el DNI del cliente y la fecha de creación del carrito
    search_fields = ('dni_cliente',)  # Campo de búsqueda por DNI del cliente
    date_hierarchy = 'creado'  # Permite filtrar por fecha de creación en la parte superior

# Personalización de la administración de los items del carrito
@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')  # Muestra el carrito, producto y cantidad en la lista de items
    list_filter = ('carrito', 'producto')  # Filtros por carrito y producto
    search_fields = ('producto__nombre',)  # Búsqueda por el nombre del producto

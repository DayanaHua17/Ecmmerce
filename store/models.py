from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name="productos")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Nuevo campo de imagen

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    dni_cliente = models.CharField(max_length=8, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.dni_cliente or 'Sin DNI'}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # Asegúrate de incluir el valor por defecto

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
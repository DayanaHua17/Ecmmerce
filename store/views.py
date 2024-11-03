from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Carrito, CarritoItem
from .forms import CategoriaForm, ProductoForm

# Vista para la página principal
def base(request):
    return render(request, 'store/base.html')

# Vista pública para listar todos los productos
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'store/productos.html', {'productos': productos})

# Vista pública para listar todas las categorías
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'store/categorias.html', {'categorias': categorias})

# Vista para ver el contenido del carrito
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoItem

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoItem

from django.contrib import messages  # Importa para usar mensajes de Django

from django.db import IntegrityError

def ver_carrito(request):
    # Obtener el ID del carrito almacenado en la sesión, si existe
    carrito_id = request.session.get('carrito_id', None)

    if not carrito_id:
        # Si no hay carrito en la sesión, redirigir a la página de productos para agregar uno primero
        return redirect('store:productos')

    # Obtener el carrito actual
    carrito = get_object_or_404(Carrito, id=carrito_id)

    # Verificar si el DNI ya se ha ingresado
    if request.method == 'POST':
        dni_cliente = request.POST.get('dni')
        if dni_cliente:
            try:
                # Guardar o cambiar el DNI
                carrito.dni_cliente = dni_cliente
                carrito.save()
                return redirect('store:ver_carrito')  # Redirigir a ver el carrito después de ingresar el DNI
            except IntegrityError:
                # Mostrar un mensaje de error si el DNI ya está en uso en otro carrito
                error_message = 'Este DNI ya está asociado a otro carrito. Use un DNI diferente.'
                return render(request, 'store/ver_carrito.html', {
                    'items': carrito.items.all(),
                    'total': sum(item.producto.precio * item.cantidad for item in carrito.items.all()),
                    'dni_cliente': carrito.dni_cliente,
                    'error': error_message
                })

    # Si el carrito tiene un DNI asociado o no se necesita ingresar uno todavía, mostramos los items
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render(request, 'store/ver_carrito.html', {
        'items': items,
        'total': total,
        'dni_cliente': carrito.dni_cliente,
    })




# Vista para la página de inicio de sesión
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Vista para la página de inicio de sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store:base_sesion')  # Redirigir a la vista `base_sesion` después de iniciar sesión
        else:
            return render(request, 'store/iniciar_sesion.html', {'error': 'Credenciales incorrectas.'})
    return render(request, 'store/iniciar_sesion.html')


# Vista del panel de administración (restringida a usuarios autenticados)
@login_required
def base_sesion(request):
    return render(request, 'store/base_sesion.html')

# CRUD de Productos (restringido a usuarios autenticados)
@login_required
def crud_productos(request):
    productos = Producto.objects.all()
    return render(request, 'store/crud_productos.html', {'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:crud_productos')
    else:
        form = ProductoForm()
    return render(request, 'store/agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('store:crud_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'store/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('store:crud_productos')
    return render(request, 'store/eliminar_producto.html', {'producto': producto})

# CRUD de Categorías (restringido a usuarios autenticados)
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'store/lista_categorias.html', {'categorias': categorias})

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'store/agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('store:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'store/editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('store:lista_categorias')
    return render(request, 'store/eliminar_categoria.html', {'categoria': categoria})

# Gestión de Stock (restringido a usuarios autenticados)
@login_required
def gestionar_stock(request):
    productos = Producto.objects.all()
    return render(request, 'store/gestionar_stock.html', {'productos': productos})

@login_required
def actualizar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        nuevo_stock = int(request.POST.get('nuevo_stock', 0))
        producto.stock = nuevo_stock
        producto.save()
    return redirect('store:stock')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoItem

# Vista para agregar un producto al carrito
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoItem

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Utilizamos una clave de sesión única para cada carrito temporal
    if 'carrito_id' not in request.session:
        # Verificar si ya existe un carrito con el dni_cliente proporcionado por el usuario
        dni_cliente = request.POST.get('dni', None)  # El `DNI` puede venir del formulario o sesión en el futuro
        if dni_cliente:
            carrito, created = Carrito.objects.get_or_create(dni_cliente=dni_cliente)
        else:
            # Si no se proporciona el DNI, se crea un carrito temporal vacío
            carrito = Carrito.objects.create(dni_cliente="")
        
        request.session['carrito_id'] = carrito.id
        print("Nuevo carrito creado y almacenado en la sesión:", carrito.id)
    else:
        # Usar el carrito existente en la sesión
        carrito = get_object_or_404(Carrito, id=request.session['carrito_id'])
        print("Carrito existente encontrado:", carrito.id)

    # Obtener o crear el CarritoItem para el producto
    item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if item_created:
        item.cantidad = 1
    else:
        item.cantidad += 1
    item.save()
    print(f"Producto agregado al carrito: {producto.nombre}, Cantidad: {item.cantidad}")

    return redirect('store:ver_carrito')


# Vista para actualizar la cantidad de un item en el carrito
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
        else:
            item.delete()  # Si la cantidad es 0, se elimina el item
    return redirect('store:ver_carrito')

from django.shortcuts import render, redirect, get_object_or_404
from .models import CarritoItem

# Vista para eliminar un item del carrito
def eliminar_item(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if request.method == 'POST':
        item.delete()
    return redirect('store:ver_carrito')


from django.shortcuts import render, get_object_or_404
from .models import Carrito

from django.shortcuts import render, get_object_or_404
from .models import Carrito

@login_required
def ver_carritos(request):
    dni_cliente = request.GET.get('dni', None)  # Obtenemos el DNI desde el formulario de búsqueda
    carritos = Carrito.objects.all()  # Obtenemos todos los carritos

    if dni_cliente:
        carritos = carritos.filter(dni_cliente=dni_cliente)  # Filtrar por DNI si se proporciona

    return render(request, 'store/ver_carritos.html', {'carritos': carritos, 'dni_cliente': dni_cliente})


@login_required
def ver_carrito_por_dni(request, dni_cliente):
    # Obtener todos los carritos asociados con el DNI ingresado
    carritos = Carrito.objects.filter(dni_cliente=dni_cliente)

    if not carritos.exists():
        # Si no se encuentra ningún carrito, mostrar un mensaje de error
        return render(request, 'store/ver_carrito_dni.html', {'error': 'No se encontró un carrito para el DNI ingresado.'})

    # Acumular todos los items de todos los carritos
    items = []
    total = 0
    for carrito in carritos:
        for item in carrito.items.all():
            items.append(item)
            total += item.producto.precio * item.cantidad

    return render(request, 'store/ver_carrito_dni.html', {'items': items, 'total': total, 'dni_cliente': dni_cliente})


@login_required
def eliminar_carrito(request, carrito_id):
    carrito = get_object_or_404(Carrito, id=carrito_id)
    if request.method == 'POST':
        carrito.delete()
        messages.success(request, f"El carrito con ID {carrito_id} ha sido eliminado con éxito.")
        return redirect('store:ver_carritos')
    
    return render(request, 'store/eliminar_carrito.html', {'carrito': carrito})
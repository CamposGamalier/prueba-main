from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Ticket, Producto, Carrito
from .forms import LoginForm, ProductoForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm,UpdateForm 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Profile
from .forms import CustomRegisterForm, CustomAuthenticationForm, ProductoForm, LoginForm, CustomUserCreationForm
from .models import Producto, PurchaseReceipt, PurchaseDetail
from datetime import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.utils import timezone
from django.shortcuts import render
from .models import Producto
from .serializers import ProductoSerializer, CarritoSerializer, TicketSerializer, PurchaseReceiptSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

class PurchaseReceiptViewSet(viewsets.ModelViewSet):
    queryset = PurchaseReceipt.objects.all()
    serializer_class = PurchaseReceiptSerializer
    permission_classes = [IsAuthenticated]
def buscar(request):
    if 'q' in request.GET:
        query = request.GET['q']
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.none()  # No mostrar ningún producto si no hay consulta

    return render(request, 'buscar.html', {'productos': productos, 'query': query})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = '/password_reset/done/'
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html'

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

def index(request):
    return render(request, 'index.html')

def carrito_vacio(request):
    return render(request, 'carrito_vacio.html')

def hombre(request):
    productos = Producto.objects.all()

    # Obtener el contenido del carrito para el usuario actual
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user)
        total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    else:
        carrito_items = []
        total = 0

    return render(request, 'hombre.html', {'productos': productos, 'carrito_items': carrito_items, 'total': total})

def nosotros(request):
    return render(request, 'nosotros.html')

def formu(request):
    form = CustomRegisterForm()
    return render(request, 'formu.html', {'form': form})

def ticket(request):
    return render(request, 'ticket.html')

def formu(request):
    return render(request, 'registration/formu.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('index')

@login_required
def micuenta(request):
    user = request.user

    # Obtener el perfil del usuario si existe
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None
        messages.warning(request, 'No se encontró un perfil asociado a este usuario.')

    # Procesar el formulario de actualización del usuario
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido actualizada!')
            return redirect('micuenta')
    else:
        form = UpdateForm(instance=user)

    # Obtener el historial de compras del usuario
    purchase_receipts = PurchaseReceipt.objects.filter(user=user).order_by('-purchase_date')

    return render(request, 'micuenta.html', {
        'form': form,
        'profile': profile,
        'purchase_receipts': purchase_receipts,
    })
  
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('index')  # Redirige al index.html después de un registro exitoso
        else:
            messages.error(request, 'Ha ocurrido un error en el registro. Por favor verifica los datos ingresados.')
    else:
        form = CustomRegisterForm()

    return render(request, 'formu.html', {'form': form})

def crear_ticket(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        if not nombre or not correo or not categoria or not descripcion:
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            ticket = Ticket(
                nombre=nombre,
                email=correo,
                categoria=categoria,
                descripcion=descripcion,
                imagen=imagen
            )
            ticket.save()
            messages.success(request, 'Ticket creado exitosamente.')
            return redirect('index')

    return render(request, 'index.html')

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
        else:
            print(form.errors)
    else:
        form = ProductoForm()
    return render(request, 'crear.html', {'productoform': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def buscar_producto(request):
    producto_id = request.GET.get('id')
    if producto_id:
        try:
            producto = Producto.objects.get(id=producto_id)
            data = {
                'success': True,
                'producto': {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'categoria': producto.categoria,
                    'stock': producto.stock,
                    'imagen': producto.imagen.url if producto.imagen else '',
                }
            }
        except Producto.DoesNotExist:
            data = {
                'success': False,
                'message': 'Producto no encontrado'
            }
    else:
        data = {
            'success': False,
            'message': 'ID de producto no proporcionado'
        }
    return JsonResponse(data)

def obtener_productos(request):
    productos = Producto.objects.all()
    data = [{'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio, 'imagen': producto.imagen.url} for producto in productos]
    
    return JsonResponse({'productos': data})

def carrito_compras(request):
    user = request.user
    carrito_items = Carrito.objects.filter(usuario=user)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})



@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        quantities = request.POST.getlist('quantities')

        if not product_ids:
            messages.error(request, 'No ha seleccionado ningún artículo. Por favor, agregue artículos al carrito antes de continuar.')
            return redirect('hombre')

        for product_id, quantity in zip(product_ids, quantities):
            product = get_object_or_404(Producto, pk=product_id)
            if product.stock >= int(quantity):
                try:
                    carrito = Carrito.objects.get(usuario=request.user, producto=product)
                    carrito.cantidad += int(quantity)
                    carrito.save()
                except Carrito.DoesNotExist:
                    Carrito.objects.create(usuario=request.user, producto=product, cantidad=int(quantity))
                
                # Descontar el stock
                product.stock -= int(quantity)
                product.save()

                messages.success(request, f'Producto {product.nombre} agregado al carrito.')
            else:
                messages.error(request, f'No hay suficiente stock para el producto {product.nombre}.')

        return redirect('ver_carrito')  # Ajusta el nombre de la URL según sea necesario

    return HttpResponseBadRequest('Bad request')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            auth_login(request , user)
            messages.success(request , "Te has registrado correctamente")
        data['form'] = formulario    

    return render(request, 'registration/registro.html', data)



@login_required
def comprar(request):
    if request.method == 'POST':
        carrito_items = Carrito.objects.filter(usuario=request.user)

        if carrito_items.exists():
            total_compra = 0
            detalles_compra = []

            # Crear detalles de compra y calcular el total
            for item in carrito_items:
                total_producto = item.producto.precio * item.cantidad
                total_compra += total_producto

                # Crear detalle de compra
                detalle_compra = PurchaseDetail.objects.create(
                    product=item.producto,
                    quantity=item.cantidad,
                    total_price=total_producto
                )
                detalles_compra.append(detalle_compra)

                # Restar stock del producto comprado
                item.producto.stock -= item.cantidad
                item.producto.save()

            # Crear recibo de compra
            recibo_compra = PurchaseReceipt.objects.create(
                user=request.user,
                purchase_date=timezone.now(),
                total_amount=total_compra
            )

            # Asociar detalles de compra con el recibo de compra
            recibo_compra.details.set(detalles_compra)

            # Limpiar carrito después de la compra
            carrito_items.delete()

            messages.success(request, "Compra realizada correctamente.")
            return redirect('compra_exitosa')  # Cambiar esto por la página que se debe mostrar después de la compra

        else:
            messages.error(request, "No hay productos en el carrito para comprar.")

    return redirect('carrito_vacio')  # O rediri# O redirige al carrito si no hay artículos


@login_required
def purchase_history(request):
    # Obtener todas las compras del usuario actual
    purchases = PurchaseReceipt.objects.filter(user=request.user).prefetch_related('details__product')
    
    purchase_details = []
    for purchase in purchases:
        for detail in purchase.details.all():
            purchase_details.append({
                'purchase_date': purchase.purchase_date,
                'product': detail.product,
                'quantity': detail.quantity,
                'total_price': detail.total_price,
            })
    
    return render(request, 'purchase_history.html', {
        'purchase_details': purchase_details,
        'user': request.user,
    })


def eliminar_del_carrito(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Carrito, id=item_id)
        
        # Restaurar el stock del producto eliminado
        item.producto.stock += item.cantidad
        item.producto.save()
        
        # Eliminar el item del carrito
        item.delete()

        messages.success(request, 'Producto eliminado del carrito.')
        return redirect('hombre')

    return HttpResponseBadRequest('Bad request')


@login_required
def ver_carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)

    # Crear una lista de elementos del carrito con el total por cada ítem
    carrito_detalles = []
    for item in carrito_items:
        carrito_detalles.append({
            'usuario': request.user.username,
            'correo': request.user.email,
            'producto': item.producto,
            'imagen': item.producto.imagen,
            'nombre': item.producto.nombre,
            'precio_unitario': item.producto.precio,
            'cantidad': item.cantidad,
            'total_por_item': item.producto.precio * item.cantidad,
            'fecha_compra': item.fecha_agregado.strftime('%Y-%m-%d %H:%M')  # Formatear la fecha de compra
        })

    return render(request, 'ver_carrito.html', {
        'carrito_detalles': carrito_detalles,
        'total': total
    })
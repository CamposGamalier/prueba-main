from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CustomLoginView, register_view, registro
from django.contrib.auth import views as auth_views  # Importar las vistas de autenticación

router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet)
router.register(r'carritos', views.CarritoViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'purchase_receipts', views.PurchaseReceiptViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('hombre/', views.hombre, name='hombre'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('formu/', views.formu, name='formu'),
    path('ticket/', views.ticket, name='ticket'),
    path('register/', register_view, name='register'),
    path('crear_ticket/', views.crear_ticket, name='crear_ticket'),
    path('registro/', registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('micuenta/', views.micuenta, name='micuenta'),
    path('productos/', views.productos, name='productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('eliminar-producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('buscar/', views.buscar, name='buscar'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('carrito/', views.carrito_compras, name='carrito_compras'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('comprar/', views.comprar, name='comprar'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito_vacio/', views.carrito_vacio, name='carrito_vacio'),
    path('compra_exitosa/', views.comprar, name='compra_exitosa'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('reset/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('api/', include(router.urls)),  # Añadir las rutas de la API
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
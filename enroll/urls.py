from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.IndexView.as_view(), name='main-page'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('allproductsinfo/<int:pk>/', views.AllProductsInfo.as_view(), name='allproductsinfo'),
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart-dashboard/', views.CartDashboardView.as_view(), name='cart_dashboard'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('increase-item-quantity/<int:pk>/', views.IncreaseCartItemQuantity.as_view(), name='increase_cart_quantity'),
    path('decrease-item-quantity/<int:pk>/', views.DecreaseCartQuantity.as_view(), name='decrease_cart_quantity'),
    path('delete-item-from-cart/<int:pk>/', views.DeleteCartItem.as_view(), name='remove_from_cart'),
    path('search/', views.SearchProductsView.as_view(), name='search_products'),
    path('customer-profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/', views.payment_page, name='payment_page'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


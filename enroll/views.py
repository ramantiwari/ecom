from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Banner, HeaderCategoryDetails, ProductListing, LISTING_TYPES, User, Product, UserCartInfo, NewQueryInfo, Address, OrderPlacedData, OrderItem
from django.views import View
from .forms import SignUpForm, QueryForm, CustomerProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.views.generic import ListView
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from square.client import Client
import requests
import uuid

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        banners = Banner.objects.all()[:3]
        header_category_details = HeaderCategoryDetails.objects.all()
    
        new_arrivals = ProductListing.objects.filter(listing_type="NewArrivals")
        trending = ProductListing.objects.filter(listing_type="Trending")
        top_rated = ProductListing.objects.filter(listing_type="TopRated")

        user_data_in_cart = UserCartInfo.objects.filter(user=request.user)
        cart_count = len(user_data_in_cart)

        deal_of_the_day = ProductListing.objects.filter(deal_of_the_day=True)
        best_seller = ProductListing.objects.filter(best_seller=True)
        

        all_product = ProductListing.objects.all()
        new_products = {
        "new_products": [
            {
                "id":product.product.id,
                "title": product.product.title,
                "selling_price": product.product.selling_price,
                "discounted_price": product.product.discounted_price,
                "category": product.product.category,
                "product_image": product.product.product_image.url
            }
            for product in all_product
        ]
    }
    
        listing_data = {
            "NewArrivals": [
                {
                    "id":product.product.id,
                    "title": product.product.title,
                    "selling_price": product.product.selling_price,
                    "discounted_price": product.product.discounted_price,
                    "category": product.product.category,
                    "product_image": product.product.product_image.url
                }
                for product in new_arrivals
            ],
            "Trending": [
                {
                    "id":product.product.id,
                    "title": product.product.title,
                    "selling_price": product.product.selling_price,
                    "discounted_price": product.product.discounted_price,
                    "category": product.product.category,
                    "product_image": product.product.product_image.url
                }
                for product in trending
            ],
            "TopRated": [
                {
                    "id":product.product.id,
                    "title": product.product.title,
                    "selling_price": product.product.selling_price,
                    "discounted_price": product.product.discounted_price,
                    "category": product.product.category,
                    "product_image": product.product.product_image.url
                }
                for product in top_rated
            ],
            "DealOfTheDay":[
                {
                    "id":product.product.id,
                    "title": product.product.title,
                    "selling_price": product.product.selling_price,
                    "discounted_price": product.product.discounted_price,
                    "category": product.product.category,
                    "product_image": product.product.product_image.url,
                    "description": product.product.description
                }
                for product in deal_of_the_day
            ],
            "BestSeller":[
                {
                    "id":product.product.id,
                    "title": product.product.title,
                    "selling_price": product.product.selling_price,
                    "discounted_price": product.product.discounted_price,
                    "category": product.product.category,
                    "product_image": product.product.product_image.url
                }
                for product in best_seller
            ]
            
        }

    
        return render(request, 'enroll/main-page.html', {
            'banner': banners,
            "header_category_details": header_category_details,
            "listing_data": listing_data,
            "new_productss": new_products,
            "cart_count": cart_count,
        })


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'enroll/signup.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        return render(request, 'enroll/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        print("login page")
        if request.user.is_authenticated:
            print("already authenticated")
            return redirect('main-page')
        return render(request, 'enroll/login.html')

    def post(self, request):
        print("inside post")
        if request.user.is_authenticated:
            return redirect('main-page')

        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('main-page')
            else:
                return HttpResponse("Invalid username or password", status=401)

        return render(request, 'enroll/login.html', {'form': fm})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'enroll/changepassword.html'

    def form_valid(self, form):
        form.save()
        return redirect("logout")


class AllProductsInfo(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = ProductListing.objects.get(id=pk)
        print(pk, "this is pk")
        print(data.id)
        product = Product.objects.get(id=data.id)
        data = {
            "id":product.id,
            "title": product.title,
            "selling_price": product.selling_price,
            "discounted_price": product.discounted_price,
            "description": product.description,
            "brand": product.brand,
            "category": product.category,
            "product_image": product.product_image.url}
        return render(request, 'enroll/new_arrivals.html', {"products": data})
        
class AddToCartView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)

        if request.user.is_authenticated:
            user = request.user
            item_already_exists_in_cart = UserCartInfo.objects.filter(user=user, product=product).exists()

            if item_already_exists_in_cart:
                return redirect("cart_dashboard")
            else:
                cart_item = UserCartInfo(user=user, product=product, quantity=1)
                cart_item.save()
                return redirect("cart_dashboard")

        return render(request, 'enroll/addtocart.html', {"product": product})

    def post(self, request, pk):
        return render(request, 'enroll/addtocart.html')  


class CartDashboardView(View):
    def get(self, request):
        user = request.user
        cart_items = UserCartInfo.objects.filter(user=user)

        subtotal = sum(item.product.discounted_price * item.quantity for item in cart_items)
        shipping_charge = 70 if subtotal > 0 else 0
        total_price = subtotal + shipping_charge

        data_lst = {
            "cart_info": [
                {
                    "id": item.product.id,
                    "product_image": item.product.product_image.url,
                    "selling_price": item.product.selling_price,
                    "discounted_price": item.product.discounted_price,
                    "category": item.product.category,
                    "title": item.product.title,
                    "description": item.product.description,
                    "quantity": item.quantity,
                }
                for item in cart_items
            ]
        }

        return render(request, 'enroll/cartdashboard.html', {
            'dashboard_data': data_lst, 
            'subtotal': subtotal, 
            'total_price': total_price
        })


class ContactUsView(View):
    def get(self, request):
        return render(request, 'enroll/contactus.html')

    def post(self, request):
        fm = QueryForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('signup')
        else:
            return render(request, 'enroll/contactus.html', {'form': fm})



class DecreaseCartQuantity(View):
    def get(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        cart_item = UserCartInfo.objects.filter(user=user, product=product).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity = F('quantity') - 1
                cart_item.save(update_fields=['quantity'])
            else:
                cart_item.delete()  # Remove if quantity reaches 0

        return redirect('cart_dashboard')

class IncreaseCartItemQuantity(View):
    def get(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        cart_item = UserCartInfo.objects.filter(user=user, product=product).first()

        if cart_item:
            cart_item.quantity = F('quantity') + 1
            cart_item.save(update_fields=['quantity'])

        return redirect('cart_dashboard')

class DeleteCartItem(View):
    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        UserCartInfo.objects.filter(user=user, product=product).delete()
        return redirect('cart_dashboard')


class SearchProductsView(ListView):
    model = Product
    template_name = 'enroll/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('search', '').strip()
        if query:
            product = Product.objects.filter(title__icontains=query) | Product.objects.filter(description__icontains=query)
            return product
        return Product.objects.none() if not product else product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search', '')
        return context
    

class CustomerProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        customer = request.user
        addresses = Address.objects.filter(user=customer)

        form = CustomerProfileForm(instance=customer)
        return render(request, 'enroll/profile.html', {'form': form, 'addresses': addresses})
        
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        else:
            customer = request.user
            form = CustomerProfileForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
            
            locality = request.POST.get('locality')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')
            state = request.POST.get('state')

            print(locality, city, zipcode, state)
            if Address.objects.filter(user=customer, locality=locality, city=city, zipcode=zipcode, state=state).exists():
                return HttpResponse("Address already exists")
            
            if locality and city and zipcode and state:
                Address.objects.create(user=customer, locality=locality, city=city, zipcode=zipcode, state=state)

            return redirect('customer_profile')
        
@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        user = request.user
        cart_items = UserCartInfo.objects.filter(user=user)

        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        subtotal = sum(item.product.discounted_price * item.quantity for item in cart_items)
        shipping_charges = 70 if subtotal > 0 else 0
        total_price = subtotal + shipping_charges

        address_id = request.POST.get("address_id")
        payment_method = request.POST.get("payment_method")
        square_token = request.POST.get("square_token")

        if not address_id or not payment_method:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if payment_method == "card" and not square_token:
            return JsonResponse({"error": "Card payment requires a valid token"}, status=400)

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Invalid address"}, status=400)

        transaction_id = None
        payment_status = "Pending"

        # Process card payment with Square API
        if payment_method == "card":
            headers = {
                "Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}",
                "Content-Type": "application/json",
            }
            data = {
                "idempotency_key": str(uuid.uuid4()),  # Unique transaction key
                "amount_money": {"amount": int(total_price * 100), "currency": "USD"},
                "source_id": square_token,
            }

            response = requests.post("https://connect.squareupsandbox.com/v2/payments", json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                transaction_id = response_data.get("payment", {}).get("id", None)
                print(transaction_id, "this is transaction id")
                payment_status = "Completed"
            else:
                return JsonResponse({"error": response_data.get("errors", "Payment failed.")}, status=400)

        order = OrderPlacedData.objects.create(
            order_id=uuid.uuid4(),
            user=user,
            address=address,
            payment_status=payment_status,
            order_status="Processing",
            transaction_id=transaction_id,
            total_price=total_price,
        )

        order_items = []
        for cart_item in cart_items:
            order_items.append(OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_at_checkout=cart_item.product.discounted_price
            ))

        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()

        return JsonResponse({
            "success": True,
            "message": "Order placed successfully",
            "order_id": str(order.order_id),
            "payment_status": payment_status
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)

def payment_page(request):
    if request.method == "POST":
        address_id = request.POST.get("selected_address")
        print(address_id)

        if not address_id:
            return JsonResponse({"success": False, "error": "Please select an address."}, status=400)
        
        selected_address = Address.objects.get(id=address_id)
        print(selected_address)

        user = request.user

        cart_items = UserCartInfo.objects.filter(user=user)
        subtotal = sum(item.product.discounted_price * item.quantity for item in cart_items)
        shipping_charges = 70 if subtotal > 0 else 0
        total_price = subtotal + shipping_charges


        context = {
            "SQUARE_APPLICATION_ID": settings.SQUARE_APPLICATION_ID,
            "SQUARE_LOCATION_ID": settings.SQUARE_LOCATION_ID,
            "address":selected_address,
            "total_price":float(total_price)
        }
        return render(request, "enroll/payment.html", context=context)
    
    else:
        return redirect("customer_profile")
    

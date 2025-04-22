from django.db import models
from django.contrib.auth.models import User
import uuid



STATE_CHOICES = (
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    phone_number = models.CharField(max_length=15, unique=True, null=True)

    def __str__(self):
        return self.user.username
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    locality = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    zipcode = models.CharField(max_length=5)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.locality}, {self.city}, {self.state}"
    

CATEGORY_CHOICES = (
    ('pillow block bearings', 'Pillow Block Bearings'),
    ('rod ends', 'Rod Ends'),
    ('pneumatics parts', 'Pneumatics Parts'),
    ('motors&gearbox', 'Motors&Gearbox'),
    ('office supply', 'Office Supply'),
    ('product1', 'Product1'),
    ('Contactors&Contacts', 'contactors&contacts'),
    ('photoelectric sensors', 'Photoelectric Sensors')
)

class Product(models.Model):
    title = models.CharField(max_length=256)
    selling_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=256)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=256)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title

class Banner(models.Model):
    banner_img = models.ImageField(upload_to="banner")

    def __str__(self):
        return f"Banner {self.id}"


class HeaderCategoryDetails(models.Model):
    category_name = models.CharField(max_length=256)
    category_img = models.ImageField(upload_to="header_category_details")
    category_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.category_name


LISTING_TYPES = (
    ('NewArrivals', 'New Arrivals'),
    ('Trending', 'Trending'),
    ('TopRated', 'Top Rated'),
)

class ProductListing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    listing_type = models.CharField(choices=LISTING_TYPES, default="NewArrivals", max_length=256)
    deal_of_the_day = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title} - {self.listing_type}"

class UserCartInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class NewQueryInfo(models.Model):
    username = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    message = models.TextField()
    def __str__(self):
        return self.email

class OrderPlacedData(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, null=True, blank=True, related_name="order_address")
    payment_status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('Refunded', 'Refunded')],
        default='Pending'
    )
    order_status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(OrderPlacedData, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_checkout = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} for Order {self.order.order_id}"


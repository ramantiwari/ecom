from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(HeaderCategoryDetails)
admin.site.register(ProductListing)
admin.site.register(UserCartInfo)
admin.site.register(NewQueryInfo)
admin.site.register(UserProfile)
admin.site.register(OrderPlacedData)
admin.site.register(OrderItem)



from django.db import models
from django.contrib.auth.models import User

# Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)   # ✅ FIX
    category = models.CharField(max_length=100, blank=True, null=True)  # ✅ FIX
    image = models.ImageField(upload_to='products/', blank=True, null=True)


# Order
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    items = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
    
    # Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username
    from django.db import models


    def __str__(self):
        return self.name
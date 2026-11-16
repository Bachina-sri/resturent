from django.db import models
from django.contrib.auth.models import User

class Item_list(models.Model):
    categeory_name = models.CharField(max_length=15)

    def __str__(self):
        return self.categeory_name


class Items(models.Model):
    Item_name = models.CharField(max_length=15)
    description = models.TextField(max_length=200)
    price = models.IntegerField()
    categeory = models.ForeignKey(Item_list, related_name='Name', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.Item_name


class aboutus(models.Model):
    description = models.TextField(max_length=200)


class Feedback(models.Model):
    Name = models.CharField(max_length=15)
    Email = models.EmailField(default='default@example.com')
    Message = models.TextField(blank=False)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Name


class Booktable(models.Model):
    Name = models.CharField(max_length=18)
    phn_no = models.CharField(max_length=10)
    Email = models.EmailField()
    Total_persons = models.IntegerField()
    Booking_date = models.DateField()

    def __str__(self):
        return self.Name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  # Link to the item
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the item
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"{self.user.username}'s cart - {self.item.Item_name}"
from django.db import models
from django.utils.timezone import now


# Model for handling property listings.
class Listing(models.Model):
    # Nested class for defining sale types using Django's TextChoices utility.
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'  

 
    class HomeType(models.TextChoices):
        HOUSE = 'House'  
        CONDO = 'Condo'  
        TOWNHOUSE = 'Town House'  

    # Fields for the listing model.
    realtor = models.EmailField(max_length=100)  
    title = models.CharField(max_length=100) 
    slug = models.SlugField(unique=True)  
    address = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    zipcode = models.CharField(max_length=100)  
    description = models.TextField()  
    price = models.IntegerField() 
    bedrooms = models.IntegerField()  
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)  
    sale_type = models.CharField(max_length=100, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=100, choices=HomeType.choices, default=HomeType.HOUSE)
    main_photo = models.ImageField(upload_to="listings/")
    photo_1 = models.ImageField(upload_to="listings/")
    photo_2 = models.ImageField(upload_to="listings/")
    photo_3 = models.ImageField(upload_to="listings/")
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    
    
    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_1.storage.delete(self.photo_1.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)
        
        super().delete()

    # String representation of the listing model, returns the title of the listing.
    def __str__(self):
        return self.title

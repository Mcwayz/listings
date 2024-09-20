from django.db import models
from django.utils.timezone import now
class  Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'
    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        TOWNHOUSE = 'Town House'
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

    def __str__(self):
        return self.title




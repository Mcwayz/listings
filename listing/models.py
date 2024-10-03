from django.db import models
from django.utils.timezone import now


# Model for handling property listings.
class Listing(models.Model):
    # Nested class for defining sale types using Django's TextChoices utility.
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'  # Option for properties that are for sale.
        FOR_RENT = 'For Rent'  # Option for properties that are for rent.

    # Nested class for defining home types using Django's TextChoices utility.
    class HomeType(models.TextChoices):
        HOUSE = 'House'  # Option for houses.
        CONDO = 'Condo'  # Option for condos.
        TOWNHOUSE = 'Town House'  # Option for townhouses.

    # Fields for the listing model.
    realtor = models.EmailField(max_length=100)  # Email of the realtor associated with the listing.
    title = models.CharField(max_length=100)  # Title of the listing.
    slug = models.SlugField(unique=True)  # Slug field to generate URL-friendly strings, must be unique.
    address = models.CharField(max_length=100)  # Address of the property.
    city = models.CharField(max_length=100)  # City where the property is located.
    state = models.CharField(max_length=100)  # State where the property is located.
    zipcode = models.CharField(max_length=100)  # Zipcode of the property location.
    description = models.TextField()  # Detailed description of the property.
    price = models.IntegerField()  # Price of the property.
    bedrooms = models.IntegerField()  # Number of bedrooms in the property.
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)  # Number of bathrooms, allowing one decimal place.
    # Field to select sale type, either 'For Sale' or 'For Rent'. Default is 'For Sale'.
    sale_type = models.CharField(max_length=100, choices=SaleType.choices, default=SaleType.FOR_SALE)

    # Field to select home type, either 'House', 'Condo', or 'Town House'. Default is 'House'.
    home_type = models.CharField(max_length=100, choices=HomeType.choices, default=HomeType.HOUSE)

    # Image fields for property photos. All images are uploaded to the "listings/" directory.
    main_photo = models.ImageField(upload_to="listings/")
    photo_1 = models.ImageField(upload_to="listings/")
    photo_2 = models.ImageField(upload_to="listings/")
    photo_3 = models.ImageField(upload_to="listings/")

    # Field indicating if the listing is published or not, default is unpublished.
    is_published = models.BooleanField(default=False)

    # Date when the listing was created, defaults to the current time.
    date_created = models.DateTimeField(default=now)

    # String representation of the listing model, returns the title of the listing.
    def __str__(self):
        return self.title

from django.http import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ListingSerializer

from listing.models import Listing


# Create your views here.

class ManageListingView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Retrieve Listings '}, status=status.HTTP_403_FORBIDDEN)
            slug = request.query_params.get('slug')
            
            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(realtor=user.email)
                listing = ListingSerializer(listing, many=True)
                return Response({'listings': listing.data}, status=status.HTTP_200_OK)
            
            if Listing.objects.filter(realtor=user.email, slug=slug).exists():
                listing = Listing.objects.get(realtor=user.email,slug=slug)
                listing = ListingSerializer(listing)
                return Response({'listing': listing.data}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Listing Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'Error': 'Something Went Wrong When Retrieving Listings.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Create Listings '}, status=status.HTTP_403_FORBIDDEN)
            data = request.data

            slug = data['slug']
            city = data['city']
            price = data['price']
            title = data['title']
            state = data['state']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            address = data['address']
            zipcode = data['zipcode']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            main_photo = data['main_photo']
            description = data['description']
            is_published = data['is_published']

            try:
                price = int(price)
            except:
                return Response({'Error': 'Price must Be an Integer'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({'Error': 'Bedrooms Must Be An Integer'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({'Error': 'bathrooms Must Be A Number'}, status=status.HTTP_400_BAD_REQUEST)
            if bathrooms <=0 or bathrooms >=10:
                bathrooms = 1.0
            bathrooms = round(bathrooms, 1)
            sale_type = data['sale_type']
            if sale_type == 'FOR_RENT':
                sale_type = 'For Rent'
            else:
                sale_type = 'For Sale'
            home_type = data['home_type']
            if home_type == 'CONDO':
                home_type = 'Condo'
            elif home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            else:
                home_type = 'House'

            if is_published == 'True':
                is_published = True
            else:
                is_published = False

            if Listing.objects.filter(slug=slug).exists():
                return Response({'Error': 'Listing Already Exists'}, status=status.HTTP_400_BAD_REQUEST)

            Listing.objects.create(
                slug=slug,
                city=city,
                title=title,
                price=price,
                state=state,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                address=address,
                zipcode=zipcode,
                bedrooms=bedrooms,
                realtor=user.email,
                bathrooms=bathrooms,
                main_photo=main_photo,
                description=description,
                is_published=is_published,

            )
            return Response({'Success', 'Listing Created'}, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {'Error': 'Something Went Wrong Creating Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

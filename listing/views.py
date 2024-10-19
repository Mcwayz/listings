from django.http import request
from django.shortcuts import render
from rest_framework import status, permissions
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
        
        
    def retrieve_values(self, data):
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
            
        data = { 
            'title':  title,
            'slug':  slug,
            'address':  address,
            'city':  city,
            'state':  state,
            'zipcode':  zipcode,
            'description': description,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sale_type': sale_type,
            'home_type': home_type,
            'main_photo': main_photo,
            'photo_1': photo_1,
            'photo_2': photo_2,
            'photo_3': photo_3,
            'is_published': is_published
        }
        
        return data

        

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Create Listings '}, status=status.HTTP_403_FORBIDDEN)
            data = request.data
            data = self.retrieve_values(data)
            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']


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
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                description=description,
                is_published=is_published,
            )
            return Response({'Success', 'Listing Created'}, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {'Error': 'Something Went Wrong Creating Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
    def put(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Update Listings '}, status=status.HTTP_403_FORBIDDEN)
            data = request.data
            data = self.retrieve_values(data)
            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']
            
            Listing.objects.filter(realtor=user.email, slug=slug).update(
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
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                description=description,
                is_published=is_published
            )
            return Response({'Success', 'Listing Updated Successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Something Went Wrong Updating Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def patch(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Update Listings '}, status=status.HTTP_403_FORBIDDEN)
            data = request.data
            slug = data['slug']
            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'Error': 'Listing Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
            
            Listing.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published,
            )
            return Response({'Success', 'Listing Published Status Updated Successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Something Went Wrong Deleting Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def delete(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'Error': 'User Does Not Have Permission To Delete Listings '}, status=status.HTTP_403_FORBIDDEN)
            data = request.data
            try:
                slug = data['slug']
            except:
                return Response({'Error': 'Slug Must Be Provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'Error': 'Listing You Are Trying To Delete Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
            Listing.objects.filter(realtor=user.email, slug=slug).delete()
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'Success', 'Listing Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Error': 'Failed to Delete Listing, Try Again'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Error': 'Something Went Wrong Deleting Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')
            if not slug:
                return Response({'Error': 'Must Provide Slug'}, status=status.HTTP_400_BAD_REQUEST)
            if Listing.objects.filter(slug=slug,is_published=True).exists():
                listing = Listing.objects.get(slug=slug,is_published=True)
                listing = ListingSerializer(listing)
                return Response({'listing': listing.data}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Listing With This Slug Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'Error': 'Something Went Wrong When Retrieving Listing Details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ListingsView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_published=True).exists():
                return Response({'Error': 'No Published Listings Available'}, status=status.HTTP_404_NOT_FOUND)
            listings = Listing.objects.order_by('-date_created').filter(is_published=True)
            listings = ListingSerializer(listings, many=True)
            return Response({'listings': listings.data}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Something Went Wrong When Retrieving Listings.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class SearchListingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            search = request.query_params.get('search')
            if not search:
                return Response({'Error': 'Search query parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

            # Case-insensitive search for better user experience
            listings = Listing.objects.filter(title__icontains=search)

            print('Listings Retrieved:')
            for listing in listings:
                print(listing.title)

            return Response({'Success': 'Listings Retrieved Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Logging the specific exception for debugging purposes
            print(f'Error occurred: {str(e)}')
            return Response({'Error': 'Something Went Wrong When Searching For Listings.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
from functools import total_ordering
from sys import exec_prefix

from .models import Category, Product, Review
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status
from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer
)
#дз2
@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()

    data = []

    for product in products:
        reviews = product.review_set.all()

        reviews_list = []
        total_stars = 0

        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'text': review.text,
                'stars': review.stars
            })
            total_stars += review.stars

        # средний рейтинг
        rating = 0
        if reviews.count() > 0:
            rating = total_stars / reviews.count()

        data.append({
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'reviews': reviews_list,
            'rating': round(rating, 2)
        })

    return Response(data)


#дз1
@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()

    data = []
    for category in categories:
        product_count = category.product_set.count()
        data.append({
            'id': category.id,
            'name': category.name,
            'product_count': product_count
        })

    return Response(data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)



@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    list_ = ProductListSerializer(products, many=True).data
    return Response(data= list_, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)



@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewListSerializer(reviews, many=True).data
    return Response(data= list_, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)






from django.urls import path

from .views import index, product_detail, search

urlpatterns = [
    path("", index, name="store"),
    path("category/<slug:category_slug>", index, name="products_by_category"),
    path(
        "category/<slug:category_slug>/<slug:product_slug>",
        product_detail,
        name="products_detail",
    ),
    path("search", search, name="search"),
]

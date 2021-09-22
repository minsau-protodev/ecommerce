from django.urls import path

from .views import index, product_detail

urlpatterns = [
    path("", index, name="store"),
    path("<slug:category_slug>", index, name="products_by_category"),
    path(
        "<slug:category_slug>/<slug:product_slug>",
        product_detail,
        name="products_detail",
    ),
]

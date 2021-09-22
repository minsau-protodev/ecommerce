from .models import Category

def menu_links(_):
    links = Category.objects.all()
    return dict(links=links)
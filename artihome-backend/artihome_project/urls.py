from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "ArtiHome API is running.",
        "endpoints": {
            "admin": "/admin/",
            "accounts": "/api/accounts/",
            "products": "/api/products/",
            "waitlist": "/api/waitlist/"
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/waitlist/', include('waitlist.urls')),
]

from django.contrib import admin
from django.urls import path, include  # ✅ include must be imported!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # ✅ Homepage routes
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('python_web_final_project.accounts_app.urls')),
                  path('', include('python_web_final_project.common_app.urls')),
                  path('company/', include('python_web_final_project.companies_app.urls')),
                  path('profile/', include('python_web_final_project.applicants_app.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

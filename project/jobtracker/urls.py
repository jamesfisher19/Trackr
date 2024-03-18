from django.contrib import admin
from django.urls import path, include
from trackr.views import home, signup, tracker
from trackr.views import create_job
from trackr.views import LoginView
from trackr.views import delete_job
from trackr.views import fetch_filtered_jobs


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    # path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(template_name='pages/home.html'), name='login'),
    path('tracker/', tracker, name='tracker'),
    path('create_job/', create_job, name='create_job'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('fetch_filtered_jobs/', fetch_filtered_jobs, name='fetch_filtered_jobs'),
    path('', home, name='home'),
    path('home/', home, name='home_page'),
]
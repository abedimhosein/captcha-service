from django.urls import path
from icaptcha import views

app_name = 'icaptcha'
urlpatterns = [
    path('load/', views.captcha_load, name='load'),
    path('download/<uuid:pub_id>/', views.captcha_download, name='download'),
    path('solve/', views.captcha_solve, name='solve'),
]

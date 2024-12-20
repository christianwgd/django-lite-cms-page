from django.urls import path

from lite_cms_page import views

app_name = 'lite_cms_page'

urlpatterns = [
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-view'),
    path('<slug:slug>/<str:template>/', views.PageDetailView.as_view(), name='page-view'),
]

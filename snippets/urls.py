from django.urls import path

from snippets import views

urlpatterns = [
    path('', views.snippet_list),
    # path('snippets/<int:pk>/',views.snippet_detail)
]


from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/<slug:slug>', views.blogDetailView, name = 'blog-detail'),
    path('authors/', views.AuthorListView.as_view(),name = 'authors'),
    path('authors/<slug:slug>', views.AuthorDetailView.as_view(), name = 'author-detail'),
    path("profile/<id>", views.user_profile, name='profile'),
    path("register/", views.user_register, name='register'),
    path('tagged/<slug:slug>/',views.tagged, name='tagged'),
    path('category/<slug:slug>/',views.category, name='category-detail'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
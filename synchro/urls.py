from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('update', views.update_view, name='update'),
    path('wfirma', views.wfirma_update_view, name='wfirma'),
    path('change_status/<int:pk>', views.change_status, name='change_status'),
    path('shop/add/', views.ShopCreateView.as_view(), name='shop-create'),
    path('shop/<int:pk>', views.ShopDetailView.as_view(), name='shop-detail'),
    path('shop/<int:pk>/delete', views.shop_delete, name='shop-delete'),
    path('settings', views.SettingsView.as_view(), name='settings')
]

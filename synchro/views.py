from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic


from .forms import CityForm
from .models import City, Product, Credentials
from .tasks import get_wfirma_products, authenticate_shop, synchronize
from .tables import ProductTable
from .filters import ProductFilter

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from synchro.models import Shop
from synchro.tables import ShopTable
from django import forms



class HomeView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'home2.html'
    table_pagination = { "per_page": 10}

    filterset_class = ProductFilter

home_view = HomeView.as_view()

class SettingsView(SingleTableView):
    model = Shop
    table_class = ShopTable
    template_name = 'settings.html'
    


class WfirmaUpdateView(generic.View):

    def get(self, request, *args, **kwargs):
        
        get_wfirma_products.delay()
        messages.add_message(request, messages.INFO,
            'Update products from wfirma database started')
        
        return HttpResponseRedirect(reverse('home'))

wfirma_update_view = WfirmaUpdateView.as_view()

class ClickShopUpdateView(generic.View):
    
    def get(self, request, *args, **kwargs):
        
        authenticate_shop.delay()
        messages.add_message(request, messages.INFO,
            'Shop autentication started')
        
        return HttpResponseRedirect(reverse('home'))

class SynchronizeView(generic.View):
    
    def get(self, request, *args, **kwargs):
    
        synchronize.delay()
        messages.add_message(request, messages.INFO,
            'Synchronization started')
        
        return HttpResponseRedirect(reverse('home'))


def change_status(request, pk):
    query = Product.objects.get(id=pk)
    query.enabled = not query.enabled
    query.save()
    return HttpResponseRedirect(reverse('home'))

def shop_delete(request, pk):
    query = Shop.objects.get(id=pk)
    query.delete()
    return HttpResponseRedirect(reverse('home'))

def product_delete_all(request):
    Product.objects.all().delete()
    return HttpResponseRedirect(reverse('home'))

class ShopCreateView(generic.CreateView):
    model = Shop
    fields = ['url', 'username', 'password']
    # template_name = 'shop-create.html'
    # form_class = ShopCreateForm

class ShopDetailView(generic.DetailView):
    model = Shop
    # template_name = 'shop-details.html'

class ShopDeleteView(generic.DeleteView):
    model = Shop
    success_url = reverse_lazy('home')

class CredentialsUpdateView(generic.UpdateView):
    model = Credentials
    fields=['login', 'password']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CredentialsUpdateView, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form

    def get_success_url(self):
        
        return reverse('home')

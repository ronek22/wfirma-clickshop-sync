from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic


from .forms import CityForm
from .models import City, Product
from .tasks import get_weather_data, get_wfirma_products
from .tables import ProductTable
from .filters import ProductFilter

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from synchro.models import Shop
from synchro.tables import ShopTable

# Create your views here.


# class HomeView(generic.CreateView):
#     template_name = 'home2.html'
#     model = City
#     form_class = CityForm
#     success_url = reverse_lazy('home')

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['cities'] = City.objects.order_by('name').all()
#         context['products'] = Product.objects.order_by('name').all()
#         return context

#     def post(self, request, *args, **kwargs):
#         result = super().post(request, *args, **kwargs)
#         city = request.POST['name']
#         if city:
#             get_weather_data(city)
#         return result

class HomeView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'home2.html'

    filterset_class = ProductFilter

home_view = HomeView.as_view()

class SettingsView(SingleTableView):
    model = Shop
    table_class = ShopTable
    template_name = 'settings.html'
    

class UpdateView(generic.View):

    def get(self, request, *args, **kwargs):

        cities = City.objects.all()
        for city in cities:
            get_weather_data.delay(city.name)

        messages.add_message(request, messages.INFO,
                             'Weather update task started.')
        return HttpResponseRedirect(reverse('home'))

update_view = UpdateView.as_view()

class WfirmaUpdateView(generic.View):

    def get(self, request, *args, **kwargs):
        
        get_wfirma_products.delay()
        messages.add_message(request, messages.INFO,
            'Update products from wfirma database started')
        
        return HttpResponseRedirect(reverse('home'))

wfirma_update_view = WfirmaUpdateView.as_view()

def change_status(request, pk):
    query = Product.objects.get(id=pk)
    query.enabled = not query.enabled
    query.save()
    return HttpResponseRedirect(reverse('home'))

def shop_delete(request, pk):
    query = Shop.objects.get(id=pk)
    query.delete()
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
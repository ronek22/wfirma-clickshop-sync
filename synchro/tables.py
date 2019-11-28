import django_tables2 as tables
from .models import Product, Shop

class ProductTable(tables.Table):

    # onclick="return confirm('Are you sure? {{record.id}}')"
    code = '''
    <a href="/change_status/{{record.id}}" class="btn btn-sm btn-info">Switch</a>'''

    change = tables.TemplateColumn(template_code=code,verbose_name='Change',)


    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap4.html"
        row_attrs = {
            'data-enabled': lambda record: record.enabled
        }
        fields = {'name', 'available', 'modified'}
        empty_text = "Brak produktów, spróbuj połączyć z WFirma"


class ShopTable(tables.Table):
    code = '''
    <a href="/shop/{{record.id}}" class="btn btn-sm btn-info pull-right">Details</a>'''
    detail = tables.TemplateColumn(template_code=code, verbose_name='', attrs = {"td": {"align": "right"}})


    class Meta:
        model = Shop
        template_name = "django_tables2/bootstrap4.html"
        fields = {'url'}
        empty_text = "Brak sklepów..."
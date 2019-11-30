from dataclasses import dataclass, field, fields
from dataclasses_json import dataclass_json
from typing import Optional, List
from datetime import datetime, timedelta

@dataclass_json
@dataclass
class Product:
    id:int
    name:str
    code:str
    netto:float
    brutto:float
    unit:str
    count:float

@dataclass_json
@dataclass
class Token:
    access_token:str
    expires_in:int
    token_type:str
    expiration_date:Optional[datetime] = None 

    def __post_init__(self):
        self.expiration_date = datetime.now() + timedelta(seconds=self.expires_in)


@dataclass_json
@dataclass
class Stock:
    stock_id:int
    price:float
    stock:float
    package:float
    sold:float
    weight:float
    availability_id:int
    delivery_id:int
    comp_price:float
    comp_promo_price:float
    price_wholesale:float
    comp_price_wholesale:float
    comp_promo_price_wholesale:float
    price_special:float
    comp_price_special:float
    comp_promo_price_special:float
    calculation_unit_id:int
    calculation_unit_ratio:float


@dataclass_json
@dataclass
class ClickProduct:
    product_id:int
    producer_id:int
    group_id:int
    tax_id:int
    add_date:str
    edit_date:str
    other_price:float
    pkwiu:str
    unit_id:int
    dimension_w:float
    dimension_h:float
    dimension_l:float
    vol_weight:float
    category_id:int
    categories:List
    promo_price:float
    code:str
    ean:str
    stock:Stock
    translations:str

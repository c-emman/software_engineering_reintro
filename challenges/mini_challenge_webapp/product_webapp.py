from fastapi import FastAPI, HTTPException
from product_program import ProductProgram
from sqlalchemy import select
from models import VATRates, Products, ProductsPydantic, VATRatesPydantic
from typing import List

app = FastAPI()

product_app = ProductProgram(db_type='postgresql')


@app.on_event('startup')
def on_startup():
    product_app.program_initialise()


@app.post('/products/load')
def load_products(file_path: str):
    product_app.params = (file_path,)
    product_app.load_data()
    return {'message': 'Successfully loaded product data'}


@app.get('/products/', response_model=list[ProductsPydantic])
def read_all_products():
    result = product_app.table_query(select(Products))
    items_data = [product_app.row_to_dict(x) for x in result]
    return_val = [product_app.format_item(item) for item in items_data]
    return return_val

@app.post('/products/', response_model=list[ProductsPydantic])
def create_product_item(product_item: ProductsPydantic):
    product_item_input = Products(**product_item.dict())
    product_app.session.add(product_item_input)
    product_app.session.commit()
    return {'message': 'New product successfully added'}


@app.get('/products/cmp', response_model=set)
def read_item_properties_compare(compare_items: str):
    product_app.params = compare_items
    return product_app.fetch_item_properties()


@app.get('/products/len', response_model=int)
def products_list_length():
    return product_app.item_list_length()


@app.get('/products/cheapest', response_model=list[ProductsPydantic])
def read_cheapest_product():
    result = product_app.find_lower_price_min()
    return [product_app.format_item(item) for item in result]


@app.get('/products/expensive', response_model=list[ProductsPydantic])
def read_most_expensive_product():
    result = product_app.find_highest_price_max()
    return [product_app.format_item(item) for item in result]


@app.get('/products/category', response_model=list[ProductsPydantic])
def read_product_category(category: str):
    product_app.params = (category,)
    result = product_app.find_items_in_category()
    return [product_app.format_item(item) for item in result]


@app.get('/products/search', response_model=list[ProductsPydantic])
def products_search(search_term: str):
    product_app.params = (search_term,)
    result = product_app.full_text_search()
    return [product_app.format_item(item) for item in result]


@app.get('/products/{product_id}', response_model=list[ProductsPydantic])
def read_product_item(product_id: str):
    product_app.params = (product_id,)
    result = product_app.show_item_details()
    return [product_app.format_item(item) for item in result]


@app.delete('/products/{product_id}')
def delete_product_item(product_id: str):
    product_item = product_app.session.get(Products, int(product_id))
    if not product_item:
        raise HTTPException(status_code=404, detail='Product item not found')

    product_app.session.delete(product_item)
    product_app.session.commit()
    return {'message': 'VAT rate deleted successfully'}


@app.put('/products/{product_id}', response_model=list[ProductsPydantic])
def update_product_item(product_id: str, product_info: ProductsPydantic):
    product_item = product_app.session.get(Products, int(product_id))
    if not product_item:
        raise HTTPException(status_code=404, detail='Product item not found')

    updated_product_item = Products(**product_info.dict())
    product_app.session.merge(updated_product_item)
    product_app.session.commit()
    return {'message': 'Product information updated'}


@app.post('/vat/', response_model=VATRatesPydantic)
def create_vat_rate(vat_rate: VATRatesPydantic):
    db_vat_rate = VATRates(**vat_rate.dict())
    product_app.session.add(db_vat_rate)
    product_app.session.commit()
    return db_vat_rate


@app.get('/vat/', response_model=list[VATRatesPydantic])
def read_vat_rates():
    return product_app.table_query(select(VATRates))


@app.put('/vat/{category}', response_model=VATRatesPydantic)
def update_vat_rate(category: str, rate: float):
    db_vat_rate = product_app.session.get(VATRates, category)
    if not db_vat_rate:
        raise HTTPException(status_code=404, detail='VAT rate not found')

    db_vat_rate.rate = rate
    product_app.session.add(db_vat_rate)
    product_app.session.commit()
    return db_vat_rate


@app.delete('/vat/{category}')
def delete_vat_rate(category: str):
    db_vat_rate = product_app.session.get(VATRates, category)
    if not db_vat_rate:
        raise HTTPException(status_code=404, detail='VAT rate not found')

    product_app.session.delete(db_vat_rate)
    product_app.session.commit()
    return {'message': 'VAT rate deleted successfully'}

from models import VATRates, Products, ProductsPydantic, VATRatesPydantic, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from product_program import ProductProgram
from sqlalchemy import select
import os


# product_app = ProductProgram(db_type='postgresql')

@asynccontextmanager
async def lifespan(application: FastAPI):
    # Startup code
    try:
        # if os.getenv('TEST_MODE'):
        #     # mock_engine = create_engine("sqlite:///:memory:")
        #     # Base.metadata.create_all(mock_engine)
        #     # SessionLocal = sessionmaker(autoflush=False, bind=mock_engine)
        #     # session = SessionLocal()
        #     session = ...  # Obtain a test session
        #     product_app = ProductProgram(db_type='sqlite', session=session)
        # else:
        product_app = ProductProgram(db_type='postgresql')
        product_app.program_initialise()
        print("successfully initialised")
        yield {"db": product_app}
    finally:
        pass


# @app.on_event('startup')
# def on_startup():
#     product_app.program_initialise()

app = FastAPI(lifespan=lifespan)


@app.post('/products/load')
def load_products(file_path: str, request: Request):
    request.state.db.params = (file_path,)
    # product_app
    request.state.db.load_data()
    return {'message': 'Successfully loaded product data'}


@app.get('/products/', response_model=list[ProductsPydantic])
def read_all_products(request: Request):
    result = request.state.db.table_query(select(Products))
    items_data = [request.state.db.row_to_dict(x) for x in result]
    return_val = [request.state.db.format_item(item) for item in items_data]
    return return_val


@app.post('/products/', response_model=list[ProductsPydantic])
def create_product_item(product_item: ProductsPydantic, request: Request):
    product_item_input = Products(**product_item.dict())
    request.state.db.session.add(product_item_input)
    request.state.db.session.commit()
    return {'message': 'New product successfully added'}


@app.get('/products/cmp', response_model=set)
def read_item_properties_compare(compare_items: str, request: Request):
    request.state.db.params = compare_items
    return request.state.db.fetch_item_properties()


@app.get('/products/len', response_model=int)
def products_list_length(request: Request):
    return request.state.db.item_list_length()


@app.get('/products/cheapest', response_model=list[ProductsPydantic])
def read_cheapest_product(request: Request):
    result = request.state.db.find_lower_price_min()
    return [request.state.db.format_item(item) for item in result]


@app.get('/products/expensive', response_model=list[ProductsPydantic])
def read_most_expensive_product(request: Request):
    result = request.state.db.find_highest_price_max()
    return [request.state.db.format_item(item) for item in result]


@app.get('/products/category', response_model=list[ProductsPydantic])
def read_product_category(category: str, request: Request):
    request.state.db.params = (category,)
    result = request.state.db.find_items_in_category()
    return [request.state.db.format_item(item) for item in result]


@app.get('/products/search', response_model=list[ProductsPydantic])
def products_search(search_term: str, request: Request):
    request.state.db.params = (search_term,)
    result = request.state.db.full_text_search()
    return [request.state.db.format_item(item) for item in result]


@app.get('/products/{product_id}', response_model=list[ProductsPydantic])
def read_product_item(product_id: str, request: Request):
    request.state.db.params = (product_id,)
    result = request.state.db.show_item_details()
    return [request.state.db.format_item(item) for item in result]


@app.delete('/products/{product_id}')
def delete_product_item(product_id: str, request: Request):
    product_item = request.state.db.session.get(Products, int(product_id))
    if not product_item:
        raise HTTPException(status_code=404, detail='Product item not found')

    request.state.db.session.delete(product_item)
    request.state.db.session.commit()
    return {'message': 'VAT rate deleted successfully'}


@app.put('/products/{product_id}', response_model=list[ProductsPydantic])
def update_product_item(product_id: str, product_info: ProductsPydantic, request: Request):
    product_item = request.state.db.session.get(Products, int(product_id))
    if not product_item:
        raise HTTPException(status_code=404, detail='Product item not found')

    updated_product_item = Products(**product_info.dict())
    request.state.db.session.merge(updated_product_item)
    request.state.db.session.commit()
    return {'message': 'Product information updated'}


@app.post('/vat/', response_model=VATRatesPydantic)
def create_vat_rate(vat_rate: VATRatesPydantic, request: Request):
    db_vat_rate = VATRates(**vat_rate.dict())
    request.state.db.session.add(db_vat_rate)
    request.state.db.session.commit()
    return db_vat_rate


@app.get('/vat/', response_model=list[VATRatesPydantic])
def read_vat_rates(request: Request):
    return request.state.db.table_query(select(VATRates))


@app.put('/vat/{category}', response_model=VATRatesPydantic)
def update_vat_rate(category: str, rate: float, request: Request):
    db_vat_rate = request.state.db.session.get(VATRates, category)
    if not db_vat_rate:
        raise HTTPException(status_code=404, detail='VAT rate not found')

    db_vat_rate.rate = rate
    request.state.db.session.add(db_vat_rate)
    request.state.db.session.commit()
    return db_vat_rate


@app.delete('/vat/{category}')
def delete_vat_rate(category: str, request: Request):
    db_vat_rate = request.state.db.session.get(VATRates, category)
    if not db_vat_rate:
        raise HTTPException(status_code=404, detail='VAT rate not found')

    request.state.db.session.delete(db_vat_rate)
    request.state.db.session.commit()
    return {'message': 'VAT rate deleted successfully'}

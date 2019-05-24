from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import request, jsonify, redirect, url_for
from models.StoreFSN import StoreFSN
from models.MapiModel import MapiModel, ProductSummarySlot
import json
import requests
import webbrowser
import re

app = Flask(__name__)
Bootstrap(app)

themes = {
    "Best Rated Books": ["https://rukminim1.flixcart.com/image/100/100/jndhrbk0/book/4/6/4/the-girl-in-room-105-original-imafa2uy3zx8c7yn.jpeg?q=100",
                         "https://www.flipkart.com/books/~best-selling-books/pr?sid=bks&otracker=nmenu_sub_Sports%2C+Books+%26+More_0_Bestsellers+in+Books&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove"],
    "Party": ["https://rukminim1.flixcart.com/image/100/100/jqzitu80/aerated-drink/b/j/z/750-na-plastic-bottle-thums-up-original-imafcvvqmq5wq2vr.jpeg?q=70",
              "https://www.flipkart.com/grocery-supermart-store?marketplace=GROCERY&otracker=nmenu_Grocery"],
    "Tech": ["https://rukminim1.flixcart.com/flap/100/100/image/a70de78ec9d888d8.jpg?q=100",
             "https://www.flipkart.com/apple-products-store?otracker=nmenu_sub_Electronics_0_Apple%20Products"],
    "Flipkart Offers": ["https://rukminim1.flixcart.com/flap/100/100/image/7b82dcaa867dc935.jpg?q=100",
                        "https://www.flipkart.com/offers-store?otracker=nmenu_offer-zone"],
    "Summer": ["https://rukminim1.flixcart.com/image/100/100/jsw3yq80/air-conditioner-new/r/g/h/183-vdzu-r-410a-183-vdzu-2-r-410a-1-5-inverter-voltas-original-imafedyps8h8jmrs.jpeg?q=100",
               "https://www.flipkart.com/home-kitchen/~best-selling-air-conditioners/pr?sid=j9e&otracker=hp_bannerads_2_1.bannerAdCard.BANNERADS_HPW%2B2_OCIB6I2DTAZY"],
    "Diva": ["https://rukminim1.flixcart.com/image/100/100/jshtk7k0/sari/h/k/f/free-ds-1795-a-divastri-original-imafeywx4tmyuxbv.jpeg?q=100",
             "https://www.flipkart.com/divastri-store?otracker=nmenu_sub_Women_0_Divastri"],
}

def create_app(config_filename):

    app.config.from_object(config_filename)

    # from app import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    return app

@app.route('/')
def index():
    return render_template('index_test.html')


products = []
storepath = {'tyy': "mobiles", 'osp': "shoes", '2oq': "clothing", '6bo': "something", 'bks': "books"}
def fill_product_static():

    for el in storepath:
        r = requests.get("http://10.47.7.57:25280/sherlock/v1/stores/" + el + "/iterator")
        json_data = json.loads(r.text)["RESPONSE"]['products']['ids'][:5]
        products.append(StoreFSN(storepath[el], get_image(json_data)))


def get_queries():
    trending_queries = []
    r = requests.get("http://10.47.7.117/solr/intentmeta/select?q=*:*&fq=-id%3A%3Cmanual%3E*&sort=impressions+desc&rows=20&fl=query%2C+impressions%3Afield(impressions)&wt=json");
    query_list = json.loads(r.text)["response"]["docs"][:20]
    for el in query_list:
        q = el["query"].lower()
        if not q in storepath.values():
            trending_queries.append(q)
    return trending_queries


def get_image(fsn_list):
    product_image_dict = {}
    for fsn in fsn_list:
        headers = {'z-clientId': 'w3.sherlock', 'z-requestId':'bullshit', 'z-timestamp':'00:00:00'}
        r = requests.get("http://10.47.1.8:31200/views?viewNames=discovery_details&entityIds="+fsn, headers=headers)
        json_data = json.loads(r.text)["entityViews"][0]["view"]["primary_image_url"]
        json_data = re.sub(r"/image/[0-9]+/[0-9]+/", "/image/55/55/", json_data)
        json_data = re.sub(r"jpeg.*", "jpeg?q=100", json_data)
        product_image_dict[fsn] = [json_data, "https://www.flipkart.com/madhur-sugar/p/itmevjgp3vsgg77p?pid={}".format(fsn)]
    return product_image_dict


@app.route('/get_product_toolbar')
def get_product_toolbar():
    q = request.args.get('q')
    searchUrl = "https://www.flipkart.com/search?q="+q+"&marketplace=FLIPKART&sid=search.flipkart.com"
    headers = {
        'X-user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Mobile Safari/537.36 FKUA/msite/0.0.1/msite/Mobile',
        'Referer': searchUrl,
        'Origin': 'https://www.flipkart.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Mobile Safari/537.36',
        'Content-Type': 'application/json',
    }

    params = (
        ('reqhash', '3398057753'),
        ('cacheFirst', 'false'),
    )

    data = '{"pageUri":"/search?q='+q+'&marketplace=FLIPKART&sid=search.flipkart.com","pageType":"BROWSE_PAGE_/search?q=sarees&marketplace=FLIPKART&sid=search.flipkart.com","pageContext":{"pageNumber":1,"paginatedFetch":false,"paginationContextMap":{}},"requestContext":{"type":"BROWSE_PAGE","ssid":"hr9lmhvas0000000","sqid":"3zuwbpbvgg000000"},"locationContext":{"pincode":"560103"}}'

    response = requests.post('https://www.flipkart.com/api/4/page/fetch', headers=headers, params=params, data=data)
    response = json.loads(response.text)
    slots = response["RESPONSE"]["slots"]
    productCount = slots[0]["widget"]["data"]["productCount"]
    slots = slots[1:]
    productSummarySlots = [slot for slot in slots if slot["widget"]["type"] == "PRODUCT_SUMMARY"]
    productSummarySlotList = []
    index = 0
    productsShown = 0
    for productSummarySlot in productSummarySlots:
        products = productSummarySlot["widget"]["data"]["products"][:6]
        productsShown = len(products)
        for product in productSummarySlot["widget"]["data"]["products"]:
            productUrl = "https://www.flipkart.com" + product["productInfo"]["action"]["url"]
            imageUrl = product["productInfo"]["value"]["media"]["images"][0]["url"]
            imageUrl = imageUrl.replace("{@quality}", "100")
            imageUrl = imageUrl.replace("{@height}", "55")
            imageUrl = imageUrl.replace("{@width}", "55")
            isFAssured = False
            if product["productInfo"]["value"]["productCardTagDetails"] and len(
                    product["productInfo"]["value"]["productCardTagDetails"]) > 0:
                isFAssured = product["productInfo"]["value"]["productCardTagDetails"][0]["type"] == "F_ASSURED"
            rating = product["productInfo"]["value"]["rating"]["average"]
            reviewCount = product["productInfo"]["value"]["rating"]["reviewCount"]
            title = product["productInfo"]["value"]["titles"]["title"]
            totalDiscount = product["productInfo"]["value"]["pricing"]["totalDiscount"]
            mrp = product["productInfo"]["value"]["pricing"]["mrp"]["value"]
            finalPrice = product["productInfo"]["value"]["pricing"]["finalPrice"]["value"]
            productSummarySlotList.append(ProductSummarySlot(index, productUrl,
                                                             imageUrl, isFAssured, rating, reviewCount,
                                                             title,
                                                             totalDiscount,
                                                             mrp,
                                                             finalPrice))
            index += 1
    mapiModel = MapiModel(q, productsShown, searchUrl, productCount, productSummarySlotList)
    return render_template('sample_toolbar.html', result=jsonify(mapiModel.serialize()))

@app.route('/get_products', methods=['GET'])
def get_products():
    result = [e.serialize() for e in products]
    result = {"products": result, "trending_queries": get_queries(), "themes": themes}
    return render_template('product_light.html', result=jsonify(result))


@app.route('/search_fk', methods=['POST'])
def search_fk():
    raw_data = request.form.to_dict(flat=False)
    query = raw_data.get("search")[0]

    webbrowser.open_new_tab("https://www.flipkart.com/search?q="+ query)
    return redirect(url_for('get_products'))


if __name__ == "__main__":
    fill_product_static()
    app = create_app("config")

    context = ('/Users/dhruv.pancholi/hackday/search_hack_fk/cert.pem', '/Users/dhruv.pancholi/hackday/search_hack_fk/key.pem')
    app.run(debug=True, use_reloader=True, host="0.0.0.0",  ssl_context=context)

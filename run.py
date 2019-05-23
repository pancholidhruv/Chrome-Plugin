from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import request, jsonify
from models.StoreFSN import StoreFSN
from models.MapiModel import MapiModel, ProductSummarySlot
import json
from collections import OrderedDict
import urllib, json
import requests
import ast
import webbrowser

app = Flask(__name__)
Bootstrap(app)

def create_app(config_filename):

    app.config.from_object(config_filename)

    # from app import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    return app

@app.route('/')
def index():
    return render_template('index_test.html')


@app.route('/get_single_score', methods=['POST'])
def get_single_score():
    #path = request.form.to_dict(flat=False)
    data = request.data.decode("utf-8").split(",")
    images = OrderedDict()
    for img in data:
        images[img.split(":")[0]] = img.split(":")[1]

    print(images)
    result = {}
    for i in range(1, len(data)):
        diff = verify("fraud_detection/test/"+ data[i-1].split(":")[1], "fraud_detection/test/"+data[i].split(":")[1], FRmodel)
        result[i] = str(diff)

    return(jsonify(json.dumps(result)))
    #return verify("fraud_detection/test/tshirt2.jpeg","mobile6",database, FRmodel)
    #return render_template('index2.html', result=jsonify(get_score(path["files"][0]).serialize()))

products = []
def fill_product_static():
    storepath = {'tyy': "mobiles", 'osp': "shoes", '2oq': "clothing", '6bo': "something", 'bks': "books"}

    for el in storepath:
        r = requests.get("http://10.47.7.57:25280/sherlock/v1/stores/" + el + "/iterator")
        json_data = json.loads(r.text)["RESPONSE"]['products']['ids'][:5]
        products.append(StoreFSN(storepath[el], get_image(json_data)))


def get_image(fsn_list):
    product_image_dict = {}
    for fsn in fsn_list:
        headers = {'z-clientId': 'w3.sherlock', 'z-requestId':'bullshit', 'z-timestamp':'00:00:00'}
        r = requests.get("http://10.47.1.8:31200/views?viewNames=discovery_details&entityIds="+fsn, headers=headers)
        json_data = json.loads(r.text)["entityViews"][0]["view"]["primary_image_url"]
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
    return render_template('product_light.html', result=jsonify([e.serialize() for e in products]))


@app.route('/search_fk', methods=['POST'])
def search_fk():
    raw_data = request.form.to_dict(flat=False)
    query = raw_data.get("search")[0]

    webbrowser.open_new_tab("https://www.flipkart.com/search?q="+ query)
    return render_template('product_light.html', result=jsonify([e.serialize() for e in products]))


if __name__ == "__main__":
    fill_product_static()
    app = create_app("config")

    context = ('/Users/dhruv.pancholi/hackday/search_hack_fk/cert.pem', '/Users/dhruv.pancholi/hackday/search_hack_fk/key.pem')
    app.run(debug=True, use_reloader=True, host="0.0.0.0",  ssl_context=context)

import requests
from flask import Flask, request, jsonify,json
from db import insert_search_data,get_buyer_searches,get_top_searches,get_top_categories,create_new_user
from flask_cors import CORS
import csv
import os
app = Flask(__name__)
CORS(app)
url = "https://api.barcodelookup.com/v3/products"

searches = ["engine oil","24-inch tires","side mirrors","air conditioners","steering wheel","wiper fluid","mats","pressure pump","starter chords"]

punctuation_marks = [" ","-"]
# params = {
#     "category": "Vehicles & Parts > Vehicle Parts & Accessories",
#     "brand": "Toyota",
#     "title":"wipers"
#     "formatted": "y",
#     "page": "2",
#     "key": "ylz3m55bkyqowt36ozgkdvvico3lip"
# }
new_categories = {
    "performanceparts&accessories" : ["turbo", "exhaust", "supercharger", "intake","performance", "k&n", "spark", "plug", "premium", "filter", "protects", "models"],
    "tires&wheels" : ["tire", "wheel", "inflator","rim", "hubcap", "inch", "portable", "pressure", "compressor", "gauge", "pump", "valve", "stem", "tires", "astroai", "caps", "tool"],
"oils&fluids" : ["oil", "grease", "lubricant","coolant", "transmission fluid", "wiper fluid","engine oil", "transmission fluid", "brake fluid", "power steering fluid",
    "gear oil", "antifreeze", "oil additives"],
    "interioraccessories" : ["floor mat", "steering cover", "air freshener", "mats","organizer", "seat", "universal", "windshield", "fit", "hotor", "storage", "cushion", "card", "freshener"],
"carelectronics&accessories" : ["GPS", "radio", "stereo", "camera", "bluetooth","phone", "holder", "mount", "charger", "air", "vent", "wireless", "adapter", "airtag", "lisen", "dashboard", "carplay", "magsafe"],
"tools&equipment" : ["scanner","wrench", "jack", "screwdriver", "compressor","sockets", "screwdrivers", "floor jack", "torque wrench"],
"carcare" : ["cleaning", "wash","wax","polish", "kit", "foam", "microfiber", "chemical", "brush", "ceramic", "scratch", "interior", "armor", "plastic", "restorer", "trim", "coating", "compound", "remover", "shine"],
"exterioraccessories" : ["spoiler", "roof rack", "tint", "mud flaps","license", "plate", "bungee", "cords", "trailer", "frame", "twine", "silicone", "jar", "hooks", "steel", "straps"],
"heavyduty&commercialvehicleequipment" : ["truck", "trailer", "diesel","tester", "circuit", "light", "breaker", "finder", "digital", "outlet", "duty", "heavy", "triangles", "warning"],

"interioraccessories" : ["floor mat", "steering cover", "air freshener", "mats","organizer", "seat", "universal", "windshield", "fit", "hotor", "storage", "cushion", "card", "freshener"],

"lights&lightingaccessories" : ["led", "lights", "bulb", "LED", "partsam", "marker", "bulbs", "side", "amber", "truck", "long", "life", "replacement", "headlight", "inch", "clearance", "indicator", "bar", "miniature", "bright", "fog"],

"motorcycle&powersports" : ["motorcycle", "bike", "mask", "hydration", "ski", "kawasaki", "backpack","helmet", "gloves", "dirt bike parts", "atv tires", "chain lube", "saddlebags", "motorbike exhaust", "bike cover", "off-road gear"],

"paint&paintsupplies" : ["paint", "touch", "repair", "spray", "pen", "gun", "cars", "white", "gloss","primer", "clear coat"],

"replacementparts" : ["frame", "cabin", "wiper", "blades", "battery","alternator", "fuel pump", "radiator", "cv joints"],


}
categories = {
        "Car Care": ["wax", "polish", "cleaner", "shampoo", "detailing"],
        "Car Electronics & Accessories": ["GPS", "radio", "stereo", "camera", "bluetooth"],
        "Exterior Accessories": ["spoiler", "roof rack", "tint", "mud flaps"],
        "Interior Accessories": ["seat cover", "floor mat", "steering cover", "air freshener", "mats"],
        "Lights & Lighting Accessories": ["headlight", "taillight", "bulb", "LED", "fog light"],
        "Motorcycle & Powersports": ["helmet", "gloves", "jacket", "chain", "motorcycle"],
        "Oils & Fluids": ["engine oil", "brake fluid", "coolant", "transmission fluid", "wiper fluid"],
        "Paint & Paint Supplies": ["spray paint", "touch-up", "primer", "clear coat"],
        "Performance Parts & Accessories": ["turbo", "exhaust", "supercharger", "intake"],
        "Replacement Parts": ["brake pad", "spark plug", "battery", "alternator", "radiator", "side mirrors"],
        "RV Parts & Accessories": ["awning", "camper", "RV battery", "propane tank"],
        "Tires & Wheels": ["tire", "wheel", "rim", "hubcap", "inch"],
        "Tools & Equipment": ["wrench", "jack", "screwdriver", "compressor"],
        "Heavy Duty & Commercial Vehicle Equipment": ["truck", "trailer", "diesel"]
    }
car_brands = [
    # American Brands
    "Buick", "Cadillac", "Chevrolet", "Chrysler", "Dodge", 
    "Ford", "GMC", "Jeep", "Lincoln", "Ram", "Tesla",

    # Japanese Brands
    "Acura", "Honda", "Infiniti", "Lexus", "Mazda", 
    "Mitsubishi", "Nissan", "Subaru", "Toyota",

    # German Brands
    "Audi", "BMW", "Mercedes-Benz", "Porsche", "Volkswagen",

    # Korean Brands
    "Genesis", "Hyundai", "Kia",

    # British Brands
    "Aston Martin", "Bentley", "Jaguar", "Land Rover", 
    "Mini", "Rolls-Royce",

    # Italian Brands
    "Alfa Romeo", "Ferrari", "Fiat", "Lamborghini", "Maserati",

    # French Brands
    "Bugatti", "Peugeot", "Renault",

    # Swedish Brands
    "Polestar", "Volvo",

    # Chinese Brands
    "BYD", "Geely", "Nio", "XPeng",

    # Other Notable Brands
    "Lucid", "Rivian", "VinFast"
]
# category=Apparel%20%26%20Accessories%20%3E%20Shoes
@app.route('/record_search',methods=["POST"])
def record_search():
    data = request.get_json()
    print(data)
    search_phrase = data.get('search_phrase')
    year = data.get('year')
    carmodel = data.get('carmodel')
    user_id = data.get('user_id')
    category = get_category(search_phrase)
    search_phrase = year or "" + carmodel or "" + search_phrase
    response = insert_search_data(user_id,search_phrase,category if len(category)>1 else "")
    return jsonify({"status": response})


@app.route('/buyer_searches/<int:id>',methods=["GET"])
def show_searches(id):
    searches = get_buyer_searches(id)
    print(searches)
    return searches


@app.route('/get_category_recommendations',methods=['GET'])
def show_category_recommendations():
    data_str = request.headers.get('data')
    print(data_str)
    top_categories = json.loads(data_str)
    first_three = {} 
    

    for i, category in enumerate(top_categories):
        print(category)
        filepath = f"./amazon_data/{category['category']}.csv"
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8') as file:
                csvFile = csv.DictReader(file)
                first_three[category['category']] = list(csvFile)[:3]
        else:
            print(f"File not found: {filepath}")

    print(first_three)
    return first_three
@app.route('/create_user',methods=['POST'])
def create_user():
    data = request.get_json()
    email = data['email']
    number = data['phone_number']
    role = data['role']
    id = create_new_user(email,number,role)
    return "inserted" if id else "not inserted"


@app.route('/get_top_searches',methods=['GET'])
def get_highest_searches():
    searches = get_top_searches()
    top_searches = []
    for search in searches:
        item_info = call_new_api(search[0])
        print(item_info)
        if "error" not in item_info.keys():
            item_info["search_counter"] = search[1]
            top_searches.append(item_info)
    return top_searches
@app.route('/get_top_categories',methods=["GET"])
def get_highest_categories():
    categories = get_top_categories()
    print(categories)
    top_categories = []
    for category in categories:
        category_info = {}
        category_info["id"] = category[0]
        category_info["category"] = category[1]
        category_info["category_count"] = category[2]
        top_categories.append(category_info)
    print(top_categories)
    return top_categories
    
def get_category(search_term):
    
    
    matched_categories = []

    cleaned_search = search_term.replace("-", " ").lower()  # Normalize search terms
    for category, key_words in new_categories.items():
        if any(keyword in cleaned_search for keyword in key_words):
            matched_categories.append(category)
            print(category)
    print(matched_categories)
    return matched_categories[0] if matched_categories else ""
def find_category_recommendations(categories):
    first_three = {}
    for i,category in enumerate(categories):
        print(category)
        filepath = f"./amazon_data/{category['category']}.csv"
        if os.path.exists(filepath) and i<len(categories):
            with open(filepath, mode='r', encoding='utf-8') as file:
                csvFile = csv.DictReader(file)
                first_three[f"{category['category']}"] = list(csvFile)[:3]
                # first_three.append(list(csvFile)[i])
                if len(first_three) >= 3:
                        break 
        else:
             print(f"File not found: {filepath}")
    return first_three
def sort_user_recommendations(search):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
    params = {
    "category": "Vehicles & Parts > VehicleParts > Accessories",
    "search": f"{search}",
    "formatted": "y",
    "key": "ylz3m55bkyqowt36ozgkdvvico3lip"
}
    response = requests.get(url, params=params,headers=headers)
    product_info = {}
    if response.status_code == 200 and len(response.json())>0:
        products = response.json()["products"]
        for product in products:
            if len(product["stores"])>0:
                # print(product["last_update"])
                # print(product["title"])
                # print(product["brand"])
                # print(product["manufacturer"])
                # print(product["images"][0])
                # print(product["stores"][0]["price"])
                product_info["price"] = product["stores"][0]["price"]
                product_info["image_url"] = product["images"][0]
                product_info["search"] = search
        return product_info
    else:
        return {"error":"product not found"}

def call_new_api(search):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate'
    }

    params = {
        's': search
    }

    resp = requests.get('https://api.upcitemdb.com/prod/trial/search', headers=headers, params=params)
    data = json.loads(resp.text)

    if "items" not in data or not data["items"]:
        return {"error": "product not found"}

    # Now it's safe to access data["items"][0]
    print(json.dumps(data["items"][0]["offers"], indent=2))
    product_info = {}

    offers = data["items"][0].get("offers", [])

    if len(offers) == 1:
        product_info["search"] = search
        product_info["price"] = offers[0]["price"]
        return product_info
    elif len(offers) > 1:
        lowest_price = data["items"][0].get("lowest_recorded_price", offers[0]["price"])
        filtered = [offer["price"] for offer in offers if offer["price"] != lowest_price]
        if not filtered:
            return {"search": search, "price": lowest_price}
        next_lowest_price = min(filtered, key=lambda x: abs(x - lowest_price))
        product_info["search"] = search
        product_info["price"] = next_lowest_price
        return product_info
    else:
        return {"error": "no offers found"}

            

# sort_user_recommendations()


# get_category()

if __name__ == '__main__':
    app.run(debug=True)

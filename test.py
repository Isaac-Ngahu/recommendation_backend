import csv
import requests
import json
# keywords = {}
# new_titles = []
# punctuation_marks_and_joining_words = ['-','|',')','(',"'","car","and","for","all","with","&","+"]
# with open('./amazon_data/tools&equipment.csv', mode='w', encoding='utf-8') as file:
#     csvFile = csv.DictReader(file)
    
#     for lines in csvFile:
#         title = lines["title"].split(',')[0].lower()  # Extract first title part
        
#         for word in title.split(" "):  # Process each word in the title
#             keywords[word] = keywords.get(word, 0) + 1  # Count occurrences
                            
# for key in list(keywords.keys()):
#     if key in punctuation_marks_and_joining_words or len(key)< 3:
#         del keywords[key]

# sorted_items = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
# for item in sorted_items:
#     if item[1] > 2:
#         new_titles.append(item[0])
# print(new_titles)


# Read the original content




searches = ["engine oil","24-inch tires","side mirrors","air conditioners","steering wheel","wiper fluid","mats","pressure pump","starter chords","rim"]
def get_category():
    new_categories = {
"carcare" : ["cleaning", "wash", "kit", "foam", "microfiber", "chemical", "brush", "ceramic", "scratch", "interior", "armor", "plastic", "restorer", "trim", "coating", "compound", "remover", "shine"],

"carelectronics&accessories" : ["phone", "holder", "mount", "charger", "air", "vent", "wireless", "adapter", "airtag", "lisen", "dashboard", "carplay", "magsafe"],

"exterioraccessories" : ["license", "plate", "bungee", "cords", "trailer", "frame", "twine", "silicone", "jar", "hooks", "steel", "straps"],

"heavyduty&commercialvehicleequipment" : ["tester", "circuit", "light", "breaker", "finder", "digital", "outlet", "duty", "heavy", "triangles", "warning"],

"interioraccessories" : ["organizer", "seat", "universal", "windshield", "fit", "hotor", "storage", "cushion", "card", "freshener"],

"lights&lightingaccessories" : ["led", "lights", "bulb", "partsam", "marker", "bulbs", "side", "amber", "truck", "long", "life", "replacement", "headlight", "inch", "clearance", "indicator", "bar", "miniature", "bright", "fog"],

"motorcycle&powersports" : ["motorcycle", "bike", "mask", "hydration", "ski", "kawasaki", "backpack"],

"oils&fluids" : ["oil", "grease", "permatex", "marine", "lubricant", "engine"],

"paint&paintsupplies" : ["paint", "touch", "repair", "spray", "pen", "gun", "cars", "white", "gloss"],

"performanceparts&accessories" : ["performance", "compatible", "k&n", "spark", "plug", "premium", "filter", "protects", "vehicle", "models"],

"replacementparts" : ["frame", "cabin", "wiper", "blades", "battery"],

"tires&wheels" : ["tire", "wheel", "inflator", "portable", "pressure", "compressor", "gauge", "pump", "valve", "stem", "tires", "astroai", "caps", "tool"],

"tools&equipment" : ["scanner", "engine", "code", "scan", "reader", "diagnostic", "repair", "thermometer"]
}
    
    matched_categories = []
    for search_term in searches:
        cleaned_search = search_term.replace("-", " ").lower()  # Normalize search terms
        for category, key_words in new_categories.items():
            if any(keyword in cleaned_search for keyword in key_words):
                matched_categories.append(category)
                print(category)
    print(matched_categories)
    return matched_categories if matched_categories else {"Cannot be categorized"}

# get_category()
url = "https://api.barcodelookup.com/v3/products"
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
        print(products)
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
        print(product_info)
        return product_info
    else:
        return {"error":"product not found"}

# sort_user_recommendations("engine oil")


def call_new_api():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate'
    }

    params = {
        's': 'air freshener'  # 's' is the search keyword param
    }

    resp = requests.get('https://api.upcitemdb.com/prod/trial/search', headers=headers, params=params)
    data = json.loads(resp.text)
    print(resp.status_code)
    print(json.dumps(data["items"][0]["offers"], indent=2))  # pretty print

# call_new_api()

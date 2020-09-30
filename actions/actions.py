from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset, Restarted, UserUtteranceReverted
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
import requests
import json
import re
from requests.auth import HTTPBasicAuth

main_url = 'https://woocommerce.cedexdemo.in/'
key = 'ck_f62c0a35bce1c9db3e295c817df39ed2c71704b1'
secret = 'cs_bbc0ebcc2ab4cbe5ce5f1150474ccf8abd462f25'

TAG_RE = re.compile(r'<[^>]+>')

class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Sorry, I didn't understand. Can you please rephrase that once more..")
        return []

class AddressForm(FormAction):

    def name(self) -> Text:
        return "address_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["first_name", "last_name", "phno", "email", "address", "pincode", "city", "state", "country"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "first_name": self.from_text(),
            "last_name": self.from_text(),
            "phno": self.from_text(),
            "email": self.from_text(),
            "address": self.from_text(),
            "pincode": self.from_text(),
            "city": self.from_text(),
            "state": self.from_text(),
            "country": self.from_text()
        }

    def validate_first_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("fs")
        return {"first_name": value}

    def validate_last_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("ls")
        return {"last_name": value}

    def validate_phno(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("ph")
        x = re.search("^\+[1-9]{1}[0-9]{3,14}$", value)
        if x:
            return {"phno": value}
        else:
            dispatcher.utter_message(text="Invalid contact number!!")
            return {"phno": None}

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("email")
        x = re.search(
            "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$", value)
        if x:
            return {"email": value}
        else:
            dispatcher.utter_message(text="Invalid email-id!!")
            return {"email": None}

    def validate_address(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("addr")
        return {"address": value}

    def validate_city(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("city")
        return {"city": value}
    
    def validate_state(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("State")
        return {"state": value}

    def validate_pincode(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("pin")
        return {"pincode": value}

    def validate_country(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("country")
        return {"country": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        fn = tracker.get_slot('first_name')
        ln = tracker.get_slot('last_name')
        ph = tracker.get_slot('phno')
        em = tracker.get_slot('email')
        addr = tracker.get_slot('address')
        city = tracker.get_slot('city')
        state = tracker.get_slot('state')
        country = tracker.get_slot('country')
        pincode = tracker.get_slot('pincode')
        print("FirstName: ", fn)
        print("LastName: ", ln)
        print("Contact: ", ph)
        print("Email: ", em)
        print("Address: ", addr)
        print("City: ", city)
        print("State: ", state)
        print("Country: ", country)
        print("Pincode: ", pincode)
        return[]


class ActionCategory(Action):
    def name(self) -> Text:
        return "action_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        category_url = main_url + 'wp-json/wc/v3/products/categories'
        r = requests.get(category_url,auth=HTTPBasicAuth(key,secret))
        d = r.json()
        res = {"attachment": {"type": "template", "payload": {
            "template_type": "generic", "elements": []}}}
        for x in d:
            res["attachment"]["payload"]["elements"].append({
                "title": x["name"],
                "image_url": x["image"],
                "subtitle": TAG_RE.sub('',x["description"]),
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Select " + x["name"],
                        "payload": "Category id " + str(x["id"])
                    }
                ]
            })
        dispatcher.utter_message(text='Please choose a product category.')
        if tracker.get_latest_input_channel() == 'facebook':
            dispatcher.utter_message(json_message=res)
        else:
            dispatcher.utter_message(attachment=res["attachment"])
        return[]

class ActionProductByCategory(Action):
    def name(self) -> Text:
        return "action_prodbycat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productbycategory = main_url + 'wp-json/wc/v3/products'
        cat_id = tracker.get_slot('cat_id')
        print("Cat id: ",cat_id) 
        p = {"category":str(cat_id)}
        r = requests.get(productbycategory,auth=HTTPBasicAuth(key,secret),json=p)
        d = r.json()
        if d == []:
            dispatcher.utter_message(text="Sorry, currently there are no products under this category.")
            dispatcher.utter_message(template = 'utter_gotocart')
            return[SlotSet('cat_id',None)]
        res = {"attachment": {"type": "template", "payload": {
            "template_type": "generic", "elements": []}}}
        for x in d:
            res["attachment"]["payload"]["elements"].append({
                "title": str(x["name"]) + " £" + str(x["price"]),
                "image_url": x["images"][0]["src"],
                "subtitle": TAG_RE.sub('',x["short_description"]),
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Select " + x["name"],
                        "payload": "Product id " + str(x["id"])
                    }
                ]
            })
        dispatcher.utter_message(text='Please choose a product.')
        if tracker.get_latest_input_channel() == 'facebook':
            dispatcher.utter_message(json_message=res)
        else:
            dispatcher.utter_message(attachment=res["attachment"])
        return[]

class ActionFetchProduct(Action):
    def name(self) -> Text:
        return "action_prodbyid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pro_id = tracker.get_slot('pro_id')
        print("Product id: ",pro_id)
        productbyid = main_url + "wp-json/wc/v3/products/" + str(pro_id)
        r = requests.get(productbyid,auth=HTTPBasicAuth(key,secret))
        d = r.json()
        res = {"attachment": {"type": "template", "payload": {
            "template_type": "generic", "elements": [{
                "title": str(d["name"]) + " £" + str(d["price"]),
                "image_url": d["images"][0]["src"],
                "subtitle": TAG_RE.sub('',d["description"]),
                "buttons": [
                {
                    "type": "postback",
                    "title": "Add to cart",
                    "payload": "add to cart"
                }
            ]
        }]
        }}}
        if tracker.get_latest_input_channel() == 'facebook':
           dispatcher.utter_message(json_message=res)
        else:
           dispatcher.utter_message(attachment=res["attachment"])
        product = {
            "id" : pro_id,
            "title": d["name"],
            "image_url": d["images"][0]["src"],
            "subtitle": TAG_RE.sub('',d["description"]),
            "price": d["price"]
        }
        return[SlotSet('product',product)]

class QuantityForm(FormAction):

    def name(self) -> Text:
        return "quantity_form"

    @ staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["quantity"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "quantity": self.from_text()
        }

    @ staticmethod
    def is_int(string: Text) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if self.is_int(value) and int(value) > 0:
            return {"quantity": value}
        else:
            return {"quantity": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        quantity = tracker.get_slot('quantity')
        print("Quantity: ", quantity)
        return []

class KeywordForm(FormAction):

    def name(self) -> Text:
        return "keyword_form"

    @ staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["keyword"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "keyword": self.from_text()
        }

    def validate_keyword(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"keyword": value}
        

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        keyword = tracker.get_slot('keyword')
        print("Keyword: ", keyword)
        return []

class ActionAddToCart(Action):
    def name(self) -> Text:
        return "action_addtocart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product = tracker.get_slot('product')
        quantity = tracker.get_slot('quantity')
        cart = tracker.get_slot('cart')
        f = 0
        if cart == None or cart == {}:
            cart = {}
            cart['data'] = []
        else:
            for x in cart['data']:
                if x != {}:
                    if product['id'] == x['product']['id']:
                        x['quantity'] = int(x['quantity']) + int(quantity)
                        f = 1
        if f == 0:
            cart['data'].append({
                "product" : product,
                "quantity" : quantity
                })
        dispatcher.utter_message(text="Item was added to the cart.")
        print("Cart :",cart)
        return[SlotSet('cart',cart),SlotSet('pro_id',None),SlotSet('cat_id',None),SlotSet('quantity',None),SlotSet('keyword',None)]

class ActionGoToCart(Action):
    def name(self) -> Text:
        return "action_gotocart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cart = tracker.get_slot('cart')
        print("In Cart!!!")
        price = 0.0
        if cart == None or cart == {'data': []}:
            dispatcher.utter_message(text="Your cart is empty!!")
            dispatcher.utter_message(template = 'utter_gotocart')
        else:
            res = {"attachment": {"type": "template", "payload": {
                "template_type": "generic", "elements": []}}}
            for x in cart['data']:
                if x != {}:
                    price = price + float(x["quantity"]) * float(x["product"]["price"])
                    res["attachment"]["payload"]["elements"].append({
                        "title": str(x["product"]["title"]) + " £" + str(x["product"]["price"]),
                        "image_url": x["product"]["image_url"],
                        "subtitle": x["product"]["subtitle"],
                        "buttons": [
                        {
                            "type": "postback",
                            "title": "Remove",
                            "payload": "Remove from cart " + str(x["product"]["id"])
                        },
                        {
                            "type": "postback",
                            "title": "Edit Quantity (" + str(x["quantity"]) +")",
                            "payload": "Edit quantity " + str(x["product"]["id"])
                        }
                    ]
                })
            b = [{
                    "title": "Proceed to buy",
                    "payload": "place order"
                    }]
            if tracker.get_latest_input_channel() == 'facebook':
                dispatcher.utter_message(json_message=res)
            else:
                dispatcher.utter_message(attachment=res["attachment"])
            dispatcher.utter_message(text="Total Price = £" + str(price),buttons=b)
        return[SlotSet("total",price)]

class ActionRemoveFromCart(Action):
    def name(self) -> Text:
        return "action_remove_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cart = tracker.get_slot('cart')
        rid = tracker.get_slot('r_id')
        print("Remove Item:", rid)
        for x in cart['data']:
            if x != {}:
                if x['product']['id'] == rid:
                    x.pop('product')
                    x.pop('quantity')
        while {} in cart['data']:
            cart['data'].remove({})
        print("Cart after removing item: ",cart)
        dispatcher.utter_message(text="Item was removed from the cart.")
        return[SlotSet('cart',cart),SlotSet('pro_id',None),SlotSet('cat_id',None),SlotSet('quantity',None),SlotSet('r_id',None)]

class ActionEditCart(Action):
    def name(self) -> Text:
        return "action_edit_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cart = tracker.get_slot('cart')
        eid = tracker.get_slot('e_id')
        q = tracker.get_slot('quantity')
        print("New Quantity: ",q)
        for x in cart['data']:
            if x != {}:
                if x['product']['id'] == eid:
                    print("Product Found!!")
                    x['quantity'] = q
        print("Cart after updating item: ",cart)
        dispatcher.utter_message(text="Item was updated in the cart.")
        return[SlotSet('cart',cart),SlotSet('pro_id',None),SlotSet('cat_id',None),SlotSet('quantity',None),SlotSet('e_id',None)]

class ActionSearch(Action):
    def name(self) -> Text:
        return "action_search_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            skey = tracker.get_slot('keyword')
            p = {"search":str(skey)}
            searchbykeyword = main_url + 'wp-json/wc/v3/products'
            r = requests.get(searchbykeyword,auth=HTTPBasicAuth(key,secret),json=p)
            d = r.json()
            if d == []:
                dispatcher.utter_message(text="No results found. Please try some other keyword(eg. Hoodie).")
                dispatcher.utter_message(template='utter_gotocart')
            else:        
                print("data ",d)
                res = {"attachment": {"type": "template", "payload": {
                "template_type": "generic", "elements": []}}}
                for x in d:
                    res["attachment"]["payload"]["elements"].append({
                        "title": x["name"],
                        "image_url": x["images"][0]["src"],
                        "subtitle": TAG_RE.sub('',x["short_description"]),
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Select " + x["name"],
                                "payload": "Product id " + str(x["id"])
                            }
                        ]
                    })
                if tracker.get_latest_input_channel() == 'facebook':
                    dispatcher.utter_message(json_message=res)
                else:
                    dispatcher.utter_message(attachment=res["attachment"])
            return[]

class ActionFetchCoupon(Action):
    def name(self) -> Text:
        return "action_fetch_coupon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cart = tracker.get_slot('cart')
        if cart == None or cart == {'data': []}:
            dispatcher.utter_message(text="Cannot apply coupons, your cart is empty!!")
            dispatcher.utter_message(template = 'utter_gotocart')
        else:
            coupon_url = main_url + 'wp-json/wc/v3/coupons'
            r = requests.get(coupon_url,auth=HTTPBasicAuth(key,secret))
            d = r.json()
            b =[]
            for x in d:
                b.append({
                    "title": x["code"],
                    "payload": "Coupon code " + str(x["code"])
                })
            dispatcher.utter_message(text="Please select a coupon.", buttons=b)
            return[SlotSet('cp',None)]
        return[]

class ActionCouponCheck(Action):
    def name(self) -> Text:
        return "action_couponchk"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        code = tracker.get_slot('cp')
        total = float(tracker.get_slot('total'))
        coupon_url = main_url + 'wp-json/wc/v3/coupons'
        r = requests.get(coupon_url,auth=HTTPBasicAuth(key,secret))
        d = r.json()
        f = 0
        for x in d:
            if x["code"] == code:
                if float(x["minimum_amount"]) > total:
                    f = 1
        if f == 1: 
            dispatcher.utter_message("Coupon cannot be applied!! Minimum amout is " + str(x["minimum_amount"]))
            return[SlotSet('cp',None)]
        else:
            dispatcher.utter_message(template='utter_cp')
            return[] 

class ActionFetchPaymentMethods(Action):
    def name(self) -> Text:
        return "action_fetch_pm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pm_url = main_url +'wp-json/wc/v3/payment_gateways'
        r = requests.get(pm_url,auth=HTTPBasicAuth(key,secret))
        d = r.json()
        buttons = []
        for x in d:
            buttons.append({
                "title": x["title"],
                "payload": "payment method "+ str(x["title"]) + " " + str(x["id"])
            })
        dispatcher.utter_message(text="Please select a payment method.", buttons=buttons)
        return[]

class ActionFetchPlaceOrder(Action):
    def name(self) -> Text:
        return "action_placeorder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Placing Order")
        pmi = tracker.get_slot('pmi')
        pmt = tracker.get_slot('pmt')
        cp = tracker.get_slot("cp")
        print("Coupon Applied: ",cp)
        # tot = tracker.get_slot("total")
        fn = tracker.get_slot('first_name')
        ln = tracker.get_slot('last_name')
        ph = tracker.get_slot('phno')
        em = tracker.get_slot('email')
        addr = tracker.get_slot('address')
        city = tracker.get_slot('city')
        state = tracker.get_slot('state')
        country = tracker.get_slot('country')
        pincode = tracker.get_slot('pincode')
        place_order = main_url + 'wp-json/wc/v3/orders'
        cart = tracker.get_slot('cart')
        lt = []
        c = []
        if cp != None:
            c = [{
                "code" : cp
            }]
        for x in cart["data"]:
            lt.append({
                "product_id": x['product']['id'],
                "quantity": x["quantity"]
            })
        p = {
            "payment_method": pmi,
            "payment_method_title": pmt,
            "billing": {
                "first_name": fn,
                "last_name": ln,
                "address_1": addr,
                "address_2": "",
                "city": city,
                "state": state,
                "postcode": pincode,
                "country": country,
                "email": em,
                "phone": ph
            },
            "shipping": {
                "first_name": fn,
                "last_name": ln,
                "address_1": addr,
                "address_2": "",
                "city": city,
                "state": state,
                "postcode": pincode,
                "country": country
            },
            "line_items": lt,
            "coupon_lines": c,
            "shipping_lines": [
                        {
                        "method_id": "flat_rate",
                        "method_title": "Flat Rate",
                        "total": "10"
                        }
                    ]
            }
        print("Request :",p)
        r = requests.post(place_order,auth=HTTPBasicAuth(key,secret),json=p)
        d = r.json()
        print(d)
        if r.status_code == 201:
            dispatcher.utter_message(text="Your order is "+ str(d["status"]) +". Order number is " + str(d["number"]) + " with total cost £" + str(d["total"]) + ".")
            return[AllSlotsReset()]
        else:
            
            dispatcher.utter_message(text=d["message"])
            return[]

class TrakOrderForm(FormAction):

    def name(self) -> Text:
        return "trackorder_form"

    @ staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["email", "orno"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "email": self.from_text(),
            "orno": self.from_text()
        }

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("email")
        x = re.search(
            "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$", value)
        if x:
            return {"email": value}
        else:
            return {"email": None}

    def validate_orno(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"orno": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        orno = tracker.get_slot('orno')
        em = tracker.get_slot('email')
        print("Order number: ", orno)
        print("Email: ", em)
        return []

class ActionTrackOrder(Action):

    def name(self) -> Text:
        return "action_trackorder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ordno = tracker.get_slot('orno')
        em = tracker.get_slot('email')
        trackorder = main_url + 'wp-json/wc/v3/orders/' + str(ordno)
        r = requests.get(trackorder,auth=HTTPBasicAuth(key,secret))
        if r.status_code == 200:
            d = r.json()
            print(d)
            if em == d["billing"]["email"]:
                date = str(d["date_modified"]).split("T")
                print("Date: ",date[0])
                print("Time: ",date[1])
                dispatcher.utter_message(text="Hi " +str(d["billing"]["first_name"])+ ", your order is "+ str(d["status"]) +". Last updated on "+str(date[0])+" at "+str(date[1])+".")
                dispatcher.utter_message(template="utter_gotocart")
            else:
                dispatcher.utter_message(text="Information provided doesn't match our records.")
                dispatcher.utter_message(template="utter_gotocart")
        else:
            dispatcher.utter_message(text="No orders found with the provided order number. Please check and try again.")
            dispatcher.utter_message(template="utter_gotocart")
        return []
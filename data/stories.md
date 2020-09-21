## Category
* greet
  - utter_greet
> main_menu

## Shop
> main_menu
* shop
  - action_category

## Probycat
* productbycat{"cat_id":"19"}
  - slot{"cat_id":"19"}
  - action_prodbycat
* productbyID{"pro_id":"21"}
  - slot{"pro_id":"21"}
  - action_prodbyid
* addtocart
  - quantity_form
  - form{"name": "quantity_form"}
  - form{"name": null}
  - action_addtocart
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - utter_gotocart

## fullStory
* greet
  - utter_greet
* shop
  - action_category
* productbycat{"cat_id":"19"}
  - slot{"cat_id":"19"}
  - action_prodbycat
* productbyID{"pro_id":"21"}
  - slot{"pro_id":"21"}
  - action_prodbyid
* addtocart
  - quantity_form
  - form{"name": "quantity_form"}
  - form{"name": null}
  - action_addtocart
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - utter_gotocart

## SearchbyKeyword
> main_menu
* searchbykey
  - keyword_form
  - form{"name": "keyword_form"}
  - form{"name": null}
  - action_search_item
* productbyID{"pro_id":"21"}
  - slot{"pro_id":"21"}
  - action_prodbyid
* addtocart
  - quantity_form
  - form{"name": "quantity_form"}
  - form{"name": null}
  - action_addtocart
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - utter_gotocart

## GoToCart
* gotocart
  - action_gotocart
> checkit

## Removeitem
> checkit
* removefromcart{"r_id":"23"}
  - slot{"r_id":"23"}
  - action_remove_item
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - slot{"r_id": null}
  - utter_gotocart

## Edititem
> checkit
* edititem{"e_id":"23"}
  - slot{"e_id":"23"}
  - quantity_form
  - form{"name": "quantity_form"}
  - form{"name": null}
  - action_edit_item
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - slot{"e_id": null}
  - utter_gotocart

## PlaceOrder
> checkit
* placeorder
  - address_form
  - form{"name": "address_form"}
  - form{"name": null}
  - action_fetch_pm
* payment{"pmt":"PayPal","pmi":"paypal"}
  - slot{"pmt":"PayPal"}
  - slot{"pmi":"paypal"}
  - action_placeorder
  - utter_gotocart

## Coupons
> main_menu
* coupons
  - action_fetch_coupon
* getcoupon{"cp":"98wh4xvw"}
  - slot{"cp":"98wh4xvw"}
  - utter_cp
  - utter_gotocart

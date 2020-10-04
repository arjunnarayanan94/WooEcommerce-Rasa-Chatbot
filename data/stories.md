## OutofScope
* out_of_scope
  - action_fallback
  - utter_gotocart

## backtomenu
* backtomenu
  - action_goback

## greet
* greet
  - utter_greet
> main_menu

## TrackOrder
> main_menu
* trackorder
  - trackorder_form
  - form{"name": "trackorder_form"}
  - form{"name": null}
  - action_trackorder

## shop
> main_menu
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
  - slot{"cart":"{'data': [{'product': {'id': '32', 'title': 'Beanie with Logo', 'image_url': 'https://woocommerce.cedexdemo.in/wp-content/uploads/2020/09/beanie-with-logo-1.jpg', 'subtitle': 'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.\n', 'price': '18'}, 'quantity': '3'}]}"}
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
  - slot{"cart":"{'data': [{'product': {'id': '32', 'title': 'Beanie with Logo', 'image_url': 'https://woocommerce.cedexdemo.in/wp-content/uploads/2020/09/beanie-with-logo-1.jpg', 'subtitle': 'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.\n', 'price': '18'}, 'quantity': '3'}]}"}
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - slot{"keyword": null}
  - utter_gotocart

## Coupons
* coupons
  - action_fetch_coupon
  - slot{"cp":null}
* getcoupon{"cp":"98wh4xvw"}
  - slot{"cp":"98wh4xvw"}
  - action_couponchk
  - utter_gotocart

## InCart
* gotocart
  - action_gotocart
> cart_opt

## InCart-RemoveItem
> cart_opt
* removefromcart{"r_id":"23"}
  - slot{"r_id":"23"}
  - action_remove_item
  - slot{"cat_id": null}
  - slot{"pro_id": null}
  - slot{"quantity": null}
  - slot{"r_id": null}
  - utter_gotocart

## Incart-EditItem
> cart_opt
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

## Incart-PlaceOrder
> cart_opt
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
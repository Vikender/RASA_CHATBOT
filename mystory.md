
## Generated Story -4354567750172112750
* greet
    - utter_greet
* restaurant_search{"cuisine": "south indian"}
    - slot{"cuisine": "south indian"}
    - utter_ask_location
* restaurant_search{"location": "mumbai"}
    - slot{"location": "mumbai"}
    - action_check_location
    - slot{"location_status": "true"}
    - action_restaurant
    - utter_mail_permission
* deny
    - utter_goodbye
    - export


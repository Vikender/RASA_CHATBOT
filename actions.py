from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json
import smtplib

f = open(r"./data/locations.txt", "r")
cities=[line.strip().lower() for line in f.readlines()]

global restaurant_list

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"6ce88a5ec1419e335afa1c7f92f4b739"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		amount = tracker.get_slot('amount')
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]

		cuisines_dict={'american':1,'mexican':73,'cafe':30,'chinese':25,'north indian':50,'south indian':85}
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 10)
		d = json.loads(results)
		response=""

		minAmt = 0
		maxAmt = 100000

		if amount == "low":
			maxAmt = 300
		elif amount == "mid":
			minAmt = 300
			maxAmt = 700
		elif amount == "high":
			minAmt = 700
		else:
			minAmt = 100
			maxAmt = 1000

		if d['results_found'] == 0:
			response= "no results"
		else:
			count=0
			restaurant_list=""
			for restaurant in d['restaurants']:
				count=count+1
				itemCost = restaurant['restaurant']['average_cost_for_two']
				if itemCost <= maxAmt and itemCost >= minAmt:
				    if count < 6:
				        response=response+" found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated as "+  restaurant['restaurant']['user_rating']['aggregate_rating'] + "/5 " +"\n"
				        restaurant_list=response
				    else :
				        restaurant_list=restaurant_list+" found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated as "+  restaurant['restaurant']['user_rating']['aggregate_rating'] + "/5 " +"\n"

		dispatcher.utter_message("Showing you top rated restaurants \n"+response)
		return [SlotSet('location',loc)]

class ActionCheckLocation(Action):
    def name(self):
        return 'action_check_location'

    def run(self,dispatcher,tracker,domin):
        loc = tracker.get_slot('location')
        city = str(loc)
		# dispatcher.utter_message(city)

        if city.lower().strip() in cities:
            return [SlotSet('location_status',"true")]
        else:
             return [SlotSet('location_status',"false")]

class ActionSendMail(Action):
	def name(self):
		return 'action_send_mail'
		
	def run(self, dispatcher, tracker, domain):
		email = tracker.get_slot('mailId')

		s = smtplib.SMTP('smtp.gmail.com', 587) 
		s.starttls() 
		s.login("vikcysingh54@gmail.com", "Vikender#1995")
		message = "The details of all the restaurants you inquried \n \n"+restaurant_list
		message = message
		try:
			s.sendmail("vikcysingh54@gmail.com", str(email), message)
			s.quit()
		except:
			return [SlotSet('mail_status',"false")]

		restaurant_list = ""
		return [SlotSet('mail_status',"true")]


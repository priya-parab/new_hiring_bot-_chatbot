# import flask dependencies
from flask import Flask, request, make_response, jsonify
# from bot_helper import *
# import os
# import dialogflow
import requests
import json
import redis
import pickle
from pandas import read_excel
import random
import re
# import pusher


# initialize the flask app
app = Flask(__name__)

df=read_excel('./full_data.xlsx')
my_dict = dict(zip(df.Index,df.Questions))
count = 0

# default route
@app.route('/')
def index():
	return {'fulfillmentText': 'This is a response from webhook.'}


# function for responses
def results():
	# build a request object
	# actions = {"get_questions" : get_questions, "get_results" : get_results}
	r = redis. Redis()
	req = request.get_json(force=True)
	# print(req)
	split_result = (req["session"]).split("/")
	session_id = split_result[-1]
	print(session_id)
	# r. delete(session_id)
	dict_element = []

	for i in r.keys():
		element = i.decode("utf-8")
		dict_element.append(element)

	global count
	count = count + 1


	if session_id not in dict_element:
		count = 1
		session_id_dict = {'asked_question':'','all_question':[1,2,3,4,5],'question_id':0,'candidate_ans':{},'number_of_quest_asked':0}
		random_quest_no = random.sample(session_id_dict['all_question'],1)
		result_ = my_dict[random_quest_no[0]] + "?"
		session_id_dict['number_of_quest_asked'] = count
		session_id_dict['question_id'] = random_quest_no[0]
		session_id_dict['asked_question'] = my_dict[random_quest_no[0]]
		(session_id_dict['all_question']).remove(random_quest_no[0])
		p_session_id_dict = pickle.dumps(session_id_dict)
		r.set(session_id,p_session_id_dict)
		read_dict = r.get(session_id)
		yourdict = pickle.loads(read_dict)
		print(yourdict)
		print('count' , count)
		return {'fulfillmentText': result_}
	else:	
		if count < 4:
			
			candidate_answer = req.get('queryResult').get('queryText')
			read_dict = r.get(session_id)
			session_id_dict = pickle.loads(read_dict) 
			session_id_dict['candidate_ans'].update({session_id_dict['question_id']:candidate_answer})
			random_quest_no = random.sample(session_id_dict['all_question'],1) 
			result_ = my_dict[random_quest_no[0]] +	 "?"
			session_id_dict['number_of_quest_asked'] += 1
			session_id_dict['question_id'] = random_quest_no[0]
			session_id_dict['asked_question'] = my_dict[random_quest_no[0]]
			session_id_dict['all_question'].remove(random_quest_no[0])
			print("sessionid dict")
			print(session_id_dict)
			p_session_id_dict = pickle.dumps(session_id_dict)
			r.set(session_id,p_session_id_dict)
			# count = count + 1
			# read_dict = r.get(session_id)
			# yourdict = pickle.loads(read_dict)
			# print(yourdict)
			# print('count' , count)
			return {'fulfillmentText': result_}
		else:
			candidate_answer = req.get('queryResult').get('queryText')
			read_dict = r.get(session_id)
			session_id_dict = pickle.loads(read_dict) 
			session_id_dict['candidate_ans'].update({session_id_dict['question_id']:candidate_answer})
			# candidate_data = {'session_id':session_id,'answers':session_id_dict['candidate_ans']}
			# data = json.dumps(candidate_data)

			data = json.dumps(session_id_dict['candidate_ans'])
			headers = {"accept": "application/json", "Content-Type" : "application/json"}#

			res = requests.post("http://127.0.0.1:8000/prediction/", json = data)#headers = headers)
			score = res.json()
			score = score['score']
			# r.delete(session_id)
			p_session_id_dict = pickle.dumps(session_id_dict)
			# r.set(session_id,p_session_id_dict)
			# read_dict = r.get(session_id)
			# yourdict = pickle.loads(read_dict)
			# print(yourdict)
			print(score)
			result_ = 'Thank you for applying to NeoSOFT.Your score is {}'.format(score)
			return {'fulfillmentText': result_}
		
				   
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
# 	data = {'text':'hello'}
# # 	# headers = {"accept": "application/json", "Content-Type" : "application/json"}
# 	res = requests.post("http://127.0.0.1:8000/prediction/", json = json.dumps(data))#, headers = headers)
# 	# import pdb; pdb.set_trace()
# 	score = res.json()
# 	print(score)
	return  make_response(jsonify(results()))


# create a route for webhook
# @app.route('/webhook2', methods=['GET', 'POST'])
# def webhook2():
# # 	data = {'text':'hello'}
# # 	# headers = {"accept": "application/json", "Content-Type" : "application/json"}
# # 	res = requests.post("http://127.0.0.1:8000/prediction/", json = json.dumps(data))#, headers = headers)
# 	print("request from django")
# 	score = request.get_json(force=True)
# 	print(score)
# 	# return  make_response(jsonify(results()))


# run the app
if __name__ == '__main__':	
	app.run()


### request response
{
	"originalDetectIntentRequest": {
		"payload": {}
	},
	"queryResult": {
		"action": "get_results",
		"allRequiredParamsPresent": True,
		"fulfillmentMessages": [
			{
				"text": {
					"text": [
						"Thank you"
					]
				}
			}
		],
		"fulfillmentText": "Thank you",
		"intent": {
			"displayName": "welcome-yes-ask-questions",
			"name": "projects/loomi-ocjcpf/agent/intents/05122878-f02f-416e-80a5-ed9e3b8b3ec7"
		},
		"intentDetectionConfidence": 0.01,
		"languageCode": "en",
		"outputContexts": [
			{
				"lifespanCount": 1,
				"name": "projects/loomi-ocjcpf/agent/sessions/5b6b7ea4-f3c7-fb2d-1d0d-8fb5ed61caf3/contexts/defaultwelcomeintent-yes-followup",
				"parameters": {
					"Question_1": "a list is a changeable collection",
					"Question_1.original": "a list is a changeable collection",
					"Question_2": "a tuple is immmutable collection",
					"Question_2.original": "a tuple is immmutable collection",
					"Question_3": "an key value pair iterator",
					"Question_3.original": "an key value pair iterator",
					"Question_4": "a one line function",
					"Question_4.original": "a one line function"
				}
			},
			{
				"name": "projects/loomi-ocjcpf/agent/sessions/5b6b7ea4-f3c7-fb2d-1d0d-8fb5ed61caf3/contexts/defaultwelcomeintent-followup",
				"parameters": {
					"Question_1": "a list is a changeable collection",
					"Question_1.original": "a list is a changeable collection",
					"Question_2": "a tuple is immmutable collection",
					"Question_2.original": "a tuple is immmutable collection",
					"Question_3": "an key value pair iterator",
					"Question_3.original": "an key value pair iterator",
					"Question_4": "a one line function",
					"Question_4.original": "a one line function"
				}
			}
		],
		"parameters": {
			"Question_1": "a list is a changeable collection",
			"Question_2": "a tuple is immmutable collection",
			"Question_3": "an key value pair iterator",
			"Question_4": "a one line function"
		},
		"queryText": "a one line function"
	},
	"responseId": "8f50c239-0c9f-414c-8d86-7c2460f3e269-415208ed",
	"session": "projects/loomi-ocjcpf/agent/sessions/5b6b7ea4-f3c7-fb2d-1d0d-8fb5ed61caf3"
}
#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import infermedica_api
infermedica_api.configure(app_id='5298366e', app_key='386b8464a0b2f2e2aea0598cb64b7c96')

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    #if req.get("result").get("action") != "shipping.cost":
    #    return {}
    result = req.get("queryResult")
    text = result.get("queryText")
    #zone = parameters.get("queryText") #zone = parameters.get("bank-name")

    #cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}
    
    #speech = "The interest rate of " + zone + " is " + str(cost[zone])
    mylist = apiwork(text)
    #speech = "It is possible that you have " + " " + mylist[0]['name'] + " with probability " + str(mylist[0]['probability'])
    speech = "It is possible that you have "
    #for i in range (0,len(mylist)):
    # speech = speech + mylist[i]['name'] + " with probability " + str(mylist[i]['probability']) + " "
    #print("Response:")
    print(speech)
    return {
        "fulfillment_text": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "BankRates"
    }
def apiwork(str):
    api = infermedica_api.get_api()

    response = api.parse(str)
    mentions=response.mentions
 
    request = infermedica_api.Diagnosis(sex='male', age=35)

    for i in mentions:
        request.add_symptom(i.id, i.choice_id)

    response = api.diagnosis(request)
    symptom_list=[]
    k=0
    for i in response.conditions:
        k+=1
        p={}
        p={'id':i['id'],'name':i['name'],'probability':i['probability']}
        symptom_list.append(p)
        if(k==2):
            break
        print(symptom_list)
        return symptom_list

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')

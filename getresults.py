import infermedica_api

infermedica_api.configure(app_id='5298366e', app_key='386b8464a0b2f2e2aea0598cb64b7c96')


api = infermedica_api.get_api()

response = api.parse()
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
    p={'id':i['id'],'name':i['name'],'probablity':i['probability']}
    symptom_list.append(p)
    if(k==2):
        break

print(symptom_list)

# call diagnosis
# request = api.diagnosis(request)

# Access question asked by API
# print(request.question)
# print(request.question.text)  # actual text of the question
# print(request.question.items)  # list of related evidences with possible answers
# print(request.question.items[0]['id'])
# print(request.question.items[0]['name'])
# print(request.question.items[0]['choices'])  # list of possible answers
# print(request.question.items[0]['choices'][0]['id'])  # answer id
# print(request.question.items[0]['choices'][0]['label'])  # answer label

# Access list of conditions with probabilities
# print(request.conditions)
# print(request.conditions[0]['id'])
# print(request.conditions[0]['name'])
# print(request.conditions[0]['probability'])
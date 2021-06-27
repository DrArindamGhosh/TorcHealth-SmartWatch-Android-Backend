import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore

# Use a service account
cred = credentials.Certificate('/home/chiefai/firebaseTest/vitalsigns-d97ae-firebase-adminsdk-tlhpz-2916b2a50e.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

'''
#### READ DATA #####
#### STREAM DATA ####
users_ref1 = db.collection(u'BloodOxygen/Values/1njOjma35hhGUlQ5JAYT1gufiwE3') #### This line of code is working! ####
docs = users_ref1.stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
'''

'''
#### GET DATA ####
doc_ref1 = db.collection(u'BloodOxygen').document(u'Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1/gSeUWcG57xjDRBKTx824') #### This line of code is working! ####
doc = doc_ref1.get()
if doc.exists:
   a = doc.to_dict()['date']
   print(a)
   #print(f'Document data for Blood Oxygen: {doc.to_dict()['date']}')
   print(f'Document data for Blood Oxygen: {doc.to_dict()}')
else:
   print(u'No such document!')
'''

#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'time', u'==', u'17:0').stream()          #### This works ####
#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'date', u'==', u'2021-1-29').stream()     #### This works ####
#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'value', u'==', 98).stream()              #### This works ####
#for doc in docs:
#    print(f'{doc.id} => {doc.to_dict()}')

#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'time', u'==', u'17:0').get()             #### This works ####
#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'date', u'==', u'2021-1-29').get()        #### This works ####
#docs = db.collection(u'BloodOxygen/Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1').where(u'value', u'==', 98).get()                  #### This works ####
#
#####################################################################################################################################################

#### WRITE DATA ####
#data = {
#    u'name': u'Chief AI',
#    u'email id ': u'chiefai@chief.ai',
#    u'address': u'Manchester UK'
#}

# Add a new doc in collection 'cities' with ID 'LA'
#db.collection(u'Covid Risk').document(u'Records').set(data)
####################

#### ADD DATA INTO AN EXISTING DOCUMENT COLLECTION #####
#city_ref = db.collection(u'patients').document(u'newRecords')
#
#city_ref.set({
#    u'name': True
#}, merge=True)
#####################################################################################################################################################


'''
#### THE BELOW CODE IS WORKING AS INTENDED ####
collections = db.collection('User').document('Values').collections()
for collection in collections:
    for doc in collection.stream():
        print(f'{doc.id} => {doc.to_dict()}')
#####################
'''

'''
collections = db.collection('User').document('Values').collections()
for collection in collections:
    for doc in collection.stream():
        print(f'{doc.id}')
'''


'''
collections = db.collection_group(u'IwELeKkVaZYlF7BuytQQPq6jx503').where(u'gender', u'==', u'man') ## THIS LINE IS WORKING "0kYnCgZV8MQnaxqzNnveBjbQO6u1" ##
#collections = db.collection_group(u'User').where(u'gender', u'==', u'woman')  ## THIS LINE NOT WORKING ##
docs = collections.get()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
    print(f'{doc.id}')
'''

'''
#doc_ref1 = db.collection(u'User').document(u'Values').collection(u'0kYnCgZV8MQnaxqzNnveBjbQO6u1') ## THIS IS WORKKING ##
docs = db.collection(u'User').stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
'''


'''
doc_ref1 = db.collection(u'User') ## THIS LINE IS WORKKING ##
docs = doc_ref1.where(u'name', u'in', [u'wahab', u'Ceries solutions']).get()  ## THIS LINE IS WORKING " this is satisfying both condition against both names" ##
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
    print(f'{doc.id}')
'''

'''
collections = db.collection(u'User')
docs = collections.where(u'uid', u'==', u'ubT9ZLnU18fAaXg4THhQUw9N8ER2').stream()
for doc in docs:
    print(f'{doc.id}')
'''

'''
docs = db.collection_group(u'ubT9ZLnU18fAaXg4THhQUw9N8ER2').where(u'date', u'==', u'2021-2-16').get() ## THIS LINE IS ALSO WORKING BUT AFTER ADDING INDEXE ##
#docs = db.collection(u'BloodOxygen/Values/ubT9ZLnU18fAaXg4THhQUw9N8ER2').where(u'date', u'==', u'2021-2-16').get() ## THIS LINE IS WORKING ##
for doc in docs:
    #print(f'{doc.id}')
    print(f'{doc.id} => {doc.to_dict()}')
'''

'''
docs = db.collection_group(u'BloodPressure').where(u'Values', u'==', u'ubT9ZLnU18fAaXg4THhQUw9N8ER2').get()
for doc in docs:
    #print(f'{doc.id}')
    print(f'{doc.id} => {doc.to_dict()}')
'''



################### READ COVID RISK DATA ##########################
docs = db.collection(u'User').stream()
#docs = db.collection(u'User').stream()
for doc in docs:
    a = doc.to_dict()['uid']
    #print(a)
    print(f'Blood Oxygen Records')
    docs = db.collection(u'BloodOxygen').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        print(f'Blood Oxygen: {doc.id} => {doc.to_dict()}')

    print(f'Blood Pressure Records')
    docs = db.collection(u'BloodPressure').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        print(f'Blood Pressure: {doc.id} => {doc.to_dict()}')

    print(f'Hear Rate Records')
    docs = db.collection(u'HeartRate').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        print(f'Heart Rate{doc.id} => {doc.to_dict()}')
######################## WRITING THE DATA BACK ########################################################
    docs = db.collection(u'Covid Risk').document(u'Values').collection(a).add(doc.to_dict())
    print(f'Covid Risk')
    docs = db.collection(u'Inflammation Index').document(u'Values').collection(a).add(doc.to_dict())
    print(f'Inflammation')
    docs = db.collection(u'Immunity Index').document(u'Values').collection(a).add(doc.to_dict())
    print(f'Immunity Index')

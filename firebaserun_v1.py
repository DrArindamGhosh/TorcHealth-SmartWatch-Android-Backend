import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import os
#from google.cloud import firestore

# Use a service account
cred = credentials.Certificate('/home/chiefai/firebaseTest/vitalsigns-d97ae-firebase-adminsdk-afned-a8f8fff646.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:
            f.write('\n' + displayallresult)
    else:
        with open(filename, 'w') as f:
            f.write(displayallresult)

'''
#### READ DATA ##### - #### STREAM DATA ####
users_ref1 = db.collection(u'BloodOxygen/Values/1njOjma35hhGUlQ5JAYT1gufiwE3') #### This line of code is working! ####
docs = users_ref1.stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
'''
'''
#### READ DATA ##### - #### GET DATA ####
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
def pdocs = db.collection_group(u'ubT9ZLnU18fAaXg4THhQUw9N8ER2').where(u'date', u'==', u'2021-2-16').get() ## THIS LINE IS ALSO WORKING BUT AFTER ADDING INDEXE ##
#docs = db.collection(u'BloodOxygen/Values/ubT9ZLnU18fAaXg4THhQUw9N8ER2').where(u'date', u'==', u'2021-2-16').get() ## THIS LINE IS WORKING ##
for doc in docs:
    #print(f'{doc.id}')
    print(f'{doc.id} => {doc.to_dict()}')
'''

'''
docs = db.collection_group(u'BloodPressure').where(u'Values', u'==', u'ubT9ZLnU18fAaXg4THhQUw9N8ER2').get()
for doc in docs:
immunity_with_datetime    #print(f'{doc.id}')
    print(f'{doc.id} => {doc.to_dict()}')
'''

################### READ COVID RISK DATA ##########################
docs = db.collection(u'User').stream()
for doc in docs:
    globaloxygen = int()
    globaloxygenaverage = int()
    oxygencounter = 0

    globalheartrate = int()
    heartratearray = list()
    heartratecounter = 0

    globalbpsys = int()
    globalbpdia = int()

    ################## Display of NEW RECORD with CURENT DATE+TIME  #####################
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d-%m-%Y")
    data = " Current Date + Time = " + current_date + " - " + current_time
    print (" NEW RECORD: " + data)
    #Date = str(current_date)
    #Time = str(current_time)
    #####################################################################################

    a = doc.to_dict()['uid']
    print("uid is "+a)
    print("Blood Oxygen Records for user: " + a)
    docs = db.collection(u'BloodOxygen').document(u'Values').collection(a).stream()
    for doc in docs:
        #if date is within 10 days

        oxygen = doc.to_dict()['value']
        globaloxygen = globaloxygen + oxygen
        print("Oxygen: "+str(oxygen))
        #print(f'{doc.id}')
        oxygencounter = oxygencounter + 1
        print(f'Blood Oxygen: {doc.id} => {doc.to_dict()}')

    print("Blood Pressure Records for user: " + a)
    docs = db.collection(u'BloodPressure').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        bpsys = doc.to_dict()['highValue']
        bpdia = doc.to_dict()['lowValue']
        print(f'Blood Pressure: {doc.id} => {doc.to_dict()}')
        #print("Blood pressure: "+val)

    print("Heart Rate Records for user: " + a)
    docs = db.collection(u'HeartRate').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        heartrate = doc.to_dict()['value']
        globalheartrate = heartrate + heartrate
        heartratearray.append(heartrate)
        heartratecounter = heartratecounter + 1
        print("Heart rate: "+str(heartrate))
        print(f'Heart Rate: {doc.id} => {doc.to_dict()}')
######################## WRITING THE DATA BACK ########################################################
    covidrisk = 1-globaloxygen * globalheartrate
    avghr =  globalheartrate/heartratecounter
    heartrate10 = heartratearray[-10:]

    print("The last N elements of heartratearray are : " + str(heartrate10) + "\n")
    print("heartratecounter: " + str(heartratecounter) + "\n")
    print("avg heartrate: " + str(avghr) + "\n")
    print("globalheartrate: " + str(globalheartrate) + "\n")

    covid = {'covidrisk': 99}
    covid_with_datetime = {'covidrisk': 99, 'date': current_date, 'time': current_time}
    inflammation = {'inflammation': 50}
    inflammation_with_datetime = {'inflammation': 50, 'date': current_date, 'time': current_time}
    immunity = {'immunity': 60}
    immunity_with_datetime = {'immunity': 60, 'date': current_date, 'time': current_time}

    #docs = db.collection(u'Inflammation Index').document(u'Values').collection(a).add(doc.to_dict())
    docs = db.collection(u'Covid Risk').document(u'Values').collection(a).add(covid_with_datetime)
    #print(f'Covid Risk')
    #docs = db.collection(u'Inflammation Index').document(u'Values').collection(a).add(doc.to_dict())
    docs = db.collection(u'Inflammation Index').document(u'Values').collection(a).add(inflammation_with_datetime)
    #print(f'Inflammation')
    #docs = db.collection(u'Immunity Index').document(u'Values').collection(a).add(doc.to_dict())
    docs = db.collection(u'Immunity Index').document(u'Values').collection(a).add(immunity_with_datetime)
    #print(f'Immunity Index')
#####################################################

################## CURENT TIME  #####################
    now1 = datetime.now()
    current_time1 = now1.strftime("%H:%M")
    current_date1 = now1.strftime("%d-%m-%Y")
    data1 = " Current Date + Time = " + current_date1 + " - " + current_time1
    print (" NEW RECORD: " + data1)
#####################################################

#####################################################
    a = ("NOW BELOW READING IT FROM THE SAVED TEXT FILE" + " " + " " + "-" + " " + data1)
    b = str("Readig from the saved text file - The last N elements of heartratearray are : " + str(heartrate10))
    c = str("Readig from the saved text file - heartratecounter: " + str(heartratecounter))
    d = str("Readig from the saved text file - avg heartrate: " + str(avghr))
    e = str("Readig from the saved text file - globalheartrate: " + str(globalheartrate))
    f = str("Readig from the saved text file - covid: " + str(covid))
    g = str("Readig from the saved text file - inflammation: " + str(inflammation))
    h = str("Readig from the saved text file - immunity: " + str(immunity))
    displayallresult = a + '\n' + b + '\n' + c + '\n' + d + '\n' + e
############### FILE WRITE & READ ###################
    #f = open("/home/chiefai/firebaseTest/firebaserun-output.txt", "a")
    #f.write("Readig from the saved text file - The last N elements of heartratearray are : " + str(heartrate10) + "\n")
    #f.write("Readig from the saved text file - heartratecounter: "+str(heartratecounter) +  "\n")
    #f.write("Readig from the saved text file - avg heartrate: "+str(avghr) +  "\n")
    #f.write("Readig from the saved text file - globalheartrate: "+str(globalheartrate) +  "\n")
    #f.close()
#open and read the file after the appending:
    #f = open("/home/chiefai/firebaseTest/firebaserun-output.txt", "r")
    #print(f.read())
    write_file('/home/chiefai/firebaseTest/firebaserun-output.txt' , displayallresult)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import os
import math
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
    bpcounter = 0

    globaltemp = int()
    tempcounter = 0

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
        globalbpsys = globalbpsys + bpsys
        globalbpdia = globalbpdia + bpdia
        bpcounter = bpcounter + 1
        print(f'Blood Pressure: {doc.id} => {doc.to_dict()}')
        #print("Blood pressure: "+val)

    print("Heart Rate Records for user: " + a)
    docs = db.collection(u'HeartRate').document(u'Values').collection(a).stream()
    for doc in docs:
        #print(f'{doc.id}')
        heartrate = doc.to_dict()['value']
        globalheartrate = globalheartrate + heartrate
        heartratearray.append(heartrate)
        heartratecounter = heartratecounter + 1
        print("Heart rate: "+str(heartrate))
        print(f'Heart Rate: {doc.id} => {doc.to_dict()}')



    print("Temperature Records for user: " + a)
    docs = db.collection(u'SkinTemperature').document(u'Values').collection(a).stream()
    for doc in docs:
        #if date is within 10 days

        temperature = doc.to_dict()['value']
        globaltemp = globaltemp + temperature
        print("Temperature: "+str(oxygen))
        #print(f'{doc.id}')
        tempcounter = tempcounter + 1
        print(f'Temperature: {doc.id} => {doc.to_dict()}')
######################## WRITING THE DATA BACK ########################################################

   
    if heartratecounter > 0:
      avghr =  globalheartrate/heartratecounter
    elif heartratecounter == 0:
      avghr = 0

    heartrate10 = heartratearray[-10:]

    if bpcounter > 0:
      avgbpdia = globalbpdia / bpcounter
      avgbpsys = globalbpsys / bpcounter
    elif bpcounter == 0:
      avgbpdia = 0
      avgbpsys = 0

#calculate inflammation from heartrate and diastolic bp differentials vis a vis optimal values
    if ( (avgbpdia > 0) and (avghr > 0) ): 
      inflammation = math.trunc( (avghr - 75) * (avgbpdia - 70) ) 
    elif ( (avgbpdia == 0) or (avghr == 0) ):
      inflammation = 0

#differentials can be weighted. 100 - 70 = 30, as the denominator of the diastoic weight. this represents the allowable range of variation.
# in one example, 100 - avgbpdia = 10. 10/30 is or 0.30 is the bp health level
#in another example, 100 - avgbpdia = 25    25/30 is 0.7 is the bp health level

    if oxygencounter > 0:
      avgoxygen =  globaloxygen/oxygencounter
    elif oxygencounter == 0:
      avgoxygen = 0


    if tempcounter > 0:
      avgtemp =  globaltemp/tempcounter
    elif tempcounter == 0:
      avgtemp = 37
     
    if avgtemp > 37:
      increasedtemp = avgtemp - 37
    else: 
      increasedtemp = 0



#calculate immunity and covid risk from oxygen and inflammation metrics and temperature

    covidrisk = (100 - avgoxygen) * (inflammation + 1)  / 100

    immuneindex = 100 - 20 - covidrisk - ( abs(avgtemp - 36.5) ) /1000

    print("The last N elements of heartratearray are : " + str(heartrate10) + "\n")
    print("heartratecounter: " + str(heartratecounter) + "\n")
    print("avg heartrate: " + str(avghr) + "\n")
    print("globalheartrate: " + str(globalheartrate) + "\n")
    print("average bp systolic: " + str(avgbpsys) + "\n")
    print("average bp diastoic: " + str(avgbpdia) + "\n")
    print("inflammation index : " + str(inflammation) + "\n")
    print("average oxygen : " + str(avgoxygen) + "\n")
    print("immune index : " + str(immuneindex) + "\n")
    print("avg temp: " + str(avgtemp) + "\n")
    print("chronically increased temp: " + str(increasedtemp) + "\n")
    print("covidrisk index : " + str(covidrisk) + "\n")
     
    covid = {'covidrisk': 91}
    covid_with_datetime = {'covidrisk': covidrisk, 'date': current_date, 'time': current_time}
    inflammation = {'inflammation': 51}
    inflammation_with_datetime = {'inflammation': 51, 'date': current_date, 'time': current_time}
    immunity = {'immunity': 61}
    immunity_with_datetime = {'immunity': 61, 'date': current_date, 'time': current_time}

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

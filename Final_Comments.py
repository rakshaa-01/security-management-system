import face_recognition
import cv2
import os
import pickle
import time
import numpy as np
import smtplib
import imghdr
import datetime
import imaplib
import email
import shutil
import urllib2
from datetime import datetime
from zipfile import ZipFile
from email.message import EmailMessage

#Define Variables
body=''
image_dir='/home/jetsonnano/Desktop/final_fr/fr1/demoImages/known1'
Image_Id_Number=1 #Number of stored unknown image(to be sent by mail and encodable)
No_Enc_Count=1 #Number of stored unknown image(to be sent by mail and unencodable)
Unk_Date_Time=[] #list of dates of already seen people to send in mail.
#Login Credentials.
User_Email = "jetsonstypv@gmail.com"
Jetson_Email = "jetsonstypv@gmail.com"
Jetson_Password = 'STYPV@jetson'


def Internet_On():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

def Send_DB():
#send whole known database to owner via mail(as zip).
        with ZipFile('db.zip', 'w') as zipObj:
            dirName='/home/jetsonnano/Desktop/final_fr/fr1/demoImages'
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(dirName):
                print(filenames,subfolders) 
                for filename in filenames:
                   #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath,os.path.basename(filePath))
    
            #message defined.
            newMessage = EmailMessage()                        
            newMessage['Subject'] = "Database"
            newMessage['From'] = Jetson_Email                  
            newMessage['To'] = User_Email       

            newMessage.set_content('Database is attached below for your reference.')

            #Choose zip to send.
            with open('/home/jetsonnano/Desktop/final_fr/fr1/db.zip','rb') as f:
                file_data = f.read()
                file_name ='db.zip'

            newMessage.add_attachment(file_data, maintype='zip',subtype='', filename=file_name)

            #Send mail.
            if(not Internet_On()):
                return
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(User_Email, Jetson_Password)              
                smtp.send_message(newMessage)
        #Delete this mail.
        Del_Mail()  
        
def Del_Mail():
#Delete seen mails using this function.
    #Login Credentials.	
	imap = imaplib.IMAP4_SSL("imap.gmail.com")
	# authenticate
	imap.login(Jetson_Email, Jetson_Password)
	imap.select("INBOX")
	#Choose mails to delete.
	status, messages = imap.search(None, 'SEEN')
	messages = messages[0].split()
    #Flag mails to delete
	for num in messages:
		imap.store(num,'+FLAGS','\\Deleted')
    #Delete mails(Will move into bin only).
	imap.expunge()
	# close the mailbox
	imap.close()
	# logout from the account
	imap.logout()
	
def Get_Mail():
#Getting user mail and perfroming specified operations(Add,remove etc)
    # Making the variables global to access them inside this function
    global body
    Check_Mail = 0 #condition to train pickle
    global image_dir
    # specifying login credentials

    SERVER = 'imap.gmail.com'
    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    if(not Internet_On()):
        return
    mail.login(Jetson_Email, Jetson_Password)
    # choose inbox 
    mail.select('inbox')
    # if condition satisfied sends the known person images
    if(mail.search(None, 'SUBJECT','SHOW')!=('OK', [b''])):
        Send_DB()
    # include a unknown person image to known 
    if(mail.search(None, 'SUBJECT','ADD')!=('OK', [b''])):
        type, data = mail.search(None, 'SUBJECT','ADD')
        Add_From_Mail(mail,type,data)#calls Add_From_Mail function
        Check_Mail+=1
   
    # remove known person image  and send acknowledgements    
    if (mail.search(None, 'SUBJECT','REMOVE')!=('OK', [b''])):
        if(not os.listdir(image_dir)):
            Send_Acknowledgement('No such image in database')
            return
        type, data = mail.search(None, 'SUBJECT','REMOVE')
        Rem_From_Mail(mail,type,data)#calls Rem_From_Mail function
        Check_Mail+=1
    
    # Trains the pickle file again if known person is added or removed
    if(Check_Mail>0):
        Train_Pickle()
        Check_Mail=0

def Add_From_Mail(mail,type,data):
#Function to add photo to known data base via photo id sent by user.
#Respond via an acknowledgement to notify user
    
    #Data consists of the mail ids in inbox with the subject 'ADD'
    data= data[0].split()
    
     
    for i in range(len(data[0])): 
        #Traverse through the mails to fetch data and perform decoding operation.
        for num in data[i].split():
            typ, data = mail.fetch(num, '(RFC822)')
            raw_email = data[i][1]
        
        raw_email_string = raw_email.decode('utf-8')
        b = email.message_from_string(raw_email_string)
        
        # skip any text/plain (txt) attachments
        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        
        #The content of the mail is extracted separately as person name(body 2) and image id(body 1) 
        else:
                body = b.get_payload(decode=True)
        body=body.decode('utf-8')
        l=len(body)
        
        x= body.find(" ")
        body1 =body[0:x]    
        body2=body[x+1:l-2]
    
    #Transfer the image from the specified folder to known database
    #Send acknowledgement accordingly
        if(os.path.isfile(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{body1}.jpg')):
            o=f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{body1}.jpg'
            d=f'/home/jetsonnano/Desktop/final_fr/fr1/demoImages/known1/{body2}.jpg'
            
            shutil.copyfile(o,d)
            content = f"{body2} Added as Known."
            Send_Ackowledgement(content)  
        else:
            content = f"{body1} doesn't exist in database. -Try the format ----Image_id [space] Person_name----"
            Send_Ackowledgement(content)

    #Delete completed operation command_mail from inbox.        
    Del_Mail()

def Rem_From_Mail(mail,type,data):
#Function to remove photo from known data base via person_name sent by user.
#Respond via an acknowledgement to notify user


    #Data consists of the mail ids in inbox with the subject 'REMOVE' 
    data= data[0].split()
    for i in range(len(data[0])):

        #Traverse through the mails to fetch data and perform decoding operation.    
        for num in data[i].split():
            typ, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[i][1]
            
        raw_email_string = raw_email.decode('utf-8')
        b = email.message_from_string(raw_email_string)
        
        
           
        # skip any text/plain (txt) attachments
        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
            
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                   
                    break
        
        #The content of the mail is extracted separately as person name(body).
        else:
                body = b.get_payload(decode=True)
        body=body.decode('utf-8')
        l1=len(body)
        body1 =body[0:l1-2]

        #Remove the image from the known database.
        #Send acknowledgement accordingly
        if(os.path.isfile(f'/home/jetsonnano/Desktop/final_fr/fr1/demoImages/known1/{body1}.jpg')):
            os.remove(f'/home/jetsonnano/Desktop/final_fr/fr1/demoImages/known1/{body1}.jpg')
            content = f"{body1} Removed."
            Send_Ackowledgement(content)
        else:
            content = "No such person exists in database."
            Send_Ackowledgement(content)

    #Delete completed operation command_mail from inbox.         
    Del_Mail()

def Train_Pickle():
#Train pickle with known images.  
    #Define variables.
	Encodings=[]
	Names=[]
	global image_dir
    #Get encodings of every known image.
	for root, dirs, files in os.walk(image_dir):
		for file in files:
			path=os.path.join(root,file)
			name=os.path.splitext(file)[0]
			person=face_recognition.load_image_file(path)    
			encoding=face_recognition.face_encodings(person)[0]
			Encodings.append(encoding)
			Names.append(name)
    #Dump images into pickle file.
	with open('train1.pkl','wb') as f:
		pickle.dump(Encodings,f)
		pickle.dump(Names,f)
	print(Names)

def Cmp_Unk_Face_Ret_Count():
#compare faces to unknown face database and return the count(find number of times already seen for security purposes).
    #Define variables
    global Image_Id_Number
    global Unk_Date_Time
    Unk_Date_Time=[]
    Unk_Count=1  
    #Get recent frame.
    Recent_Frame_Unk=face_recognition.load_image_file(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{Image_Id_Number}.jpg')
    Recent_Frame_Unk_Enc=face_recognition.face_encodings(Recent_Frame_Unk)[0]
    image_dir='/home/jetsonnano/Desktop/final_fr/fr1/unknown'
    #Check recent frame with previous unknowns.
    for root, dirs, files in os.walk(image_dir):
        #Take each file in the unknown folder.
        for file in files:
                
            path=os.path.join(root,file)
            name=os.path.splitext(file)[0]
            Existing_Frame_Unk=face_recognition.load_image_file(path)
            Existing_Frame_Unk_Enc=face_recognition.face_encodings(Existing_Frame_Unk)[0]
            Check_For_Match=face_recognition.compare_faces([Existing_Frame_Unk_Enc],Recent_Frame_Unk_Enc) #Check for matches.
            if(Check_For_Match==[True]): #if true,add count and date.
                Unk_Date_Time.append(name)
                Unk_Count+=1
    return Unk_Count

def Send_Ackowledgement(content):
#Send acknowledgement mail to owner for a task done(Add,remove mails etc).

    #Message content.
    newMessage = EmailMessage()                        
    newMessage['Subject'] = "Acknowledgement Email."
    newMessage['From'] = Jetson_Email                 
    newMessage['To'] = User_Email      

    newMessage.set_content(content)
    #Send mail.
    if(not Internet_On()):
        return
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Jetson_Email, Jetson_Password)              
        smtp.send_message(newMessage)


def Send_Email(s2):
#Send mail if unknown
    #message defined.
    newMessage = EmailMessage()                        
    newMessage['Subject'] = "INTRUDER ALERT!!"
    newMessage['From'] = Jetson_Email                 
    newMessage['To'] = User_Email       

    newMessage.set_content(f'UNKNOWN PERSON OUTSIDE. Found {s2} times Before on these dates:{Unk_Date_Time}')

    #Choose image to send.
    with open(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{Image_Id_Number}.jpg','rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = str(Image_Id_Number)

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    #Send mail.
    if(not Internet_On()):
        return
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Jetson_Email, Jetson_Password)              
        smtp.send_message(newMessage)

def Send_Email_Unencodable():
#Send mail for unencodable images.
    #message defined.
    newMessage = EmailMessage()                        
    newMessage['Subject'] = "INTRUDER ALERT!!"
    newMessage['From'] =Jetson_Email                 
    newMessage['To'] = User_Email
    newMessage.set_content('Due to encoding issues, this image cannot be reused for adding.')

    #Choose image to send.
    with open(f'/home/jetsonnano/Desktop/final_fr/fr1/unknown1/{No_Enc_Count}.jpg','rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name ='Unknown Person'

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    if(not Internet_On()):
        return
    #Send mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Jetson_Email, Jetson_Password)              
        smtp.send_message(newMessage)
        
Check_Unkown=1 # 1 if only unknown,0 if known
def main():
#Main part of the program.
#Run on bootup.
    #Define variables  
    Encodings=[]
    Names=[]
    Check_Unkown=1 # 1 if only unknown,0 if known
    global Image_Id_Number
    global No_Enc_Count
    #Train known images.
    Train_Pickle()

    #Open already existing pickle to extract face encodings and names. 
    with open('train1.pkl','rb') as f:
        Encodings=pickle.load(f)
        Names=pickle.load(f)
    font=cv2.FONT_HERSHEY_SIMPLEX

    #Setting csi camera. 
    dispW=320
    dispH=240
    flip=2
    cap0 = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

    #Define Timers
    Unk_Timer=time.time() #timer for every 'n' seconds.
    Cur_Time=0 #dynamic timer
    Mail_Timer = Unk_Timer #Send mail for every 'n' seconds.

    name=""
    #Happens each frame 
    while True:
        
        Check_Unkown=1 #unknown by default.
        if(Cur_Time-Mail_Timer>100):
            Get_Mail()
            with open('train1.pkl','rb') as f:
                Encodings=pickle.load(f)
                Names=pickle.load(f)
            Mail_Timer=time.time()
        #get frame
        _,frame=cap0.read()  
        #Encode the frame.
        facePositions=face_recognition.face_locations(frame,model='cnn')
        allEncodings=face_recognition.face_encodings(frame,facePositions)
        #check frame with known database
        for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
            name='Unknown Person' #By default
            #matches = number of matches
            matches=face_recognition.compare_faces(Encodings,face_encoding)

            #if atleast one known, add name 
            if True in matches:
                Check_Unkown=0
                first_match_index=matches.index(True)
                name=Names[first_match_index]

            print(name)
            
            #condition for unknown person.
            if(Check_Unkown==1 and (Cur_Time-Unk_Timer)>5 ):
            
                z=datetime.now()
                z=z.replace(second=0, microsecond=0)
                #Check if encodable,and add unkown image. 
                if(face_recognition.face_encodings(frame)):

                    cv2.imwrite(f'/home/jetsonnano/Desktop/final_fr/fr1/unknown/{z}.jpg',frame) #add unknown image with name as date 
                    cv2.imwrite(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{Image_Id_Number}.jpg',frame) #add unknown image with name as arbitrary number.
                
                    Count=Cmp_Unk_Face_Ret_Count() #Call cmp Function
                    Send_Email(Count) 
                    Check_Unkown=0 #Shows face is unknown
                    Image_Id_Number+=1
                    Unk_Timer=time.time()

                else:

                    cv2.imwrite(f'/home/jetsonnano/Desktop/final_fr/fr1/unknown1/{No_Enc_Count}.jpg',frame) 
                    Send_Email_Unencodable() 
                    Check_Unkown=0 #Shows face is unknown
                    No_Enc_Count+=1

                    Unk_Timer=time.time()
                

        Cur_Time=time.time()
          
        if cv2.waitKey(1)==ord('q'):
            break
    
    cap0.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    
    main()

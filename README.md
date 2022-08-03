
# Security Management System | SIH 2022

- _Developed a smart surveillance system implementing a face recognition model using RaspberryPi which continuously monitors the region in front of the house and alerts the user if an intruderis present along with the number of times he/she has appeared previously_
- _New person’s image can be added as known by sending a command and the system is retrained immediately_


## Idea/ Approach Details:

With burglary rate shooting up every day, deploying a strong and affordable security surveillance system at home becomes imperative. In this work, a Raspberry-pi based intruder alert system is designed to
accomplish the above goal. <br/>
- This system works using the principle of **face recognition** and
continuously monitoring the area in front of the main door of the
home.
- When it identifies an intruder/burglar appearing in front of the door, it
immediately sends their picture to the owner through mail, in addition
to alerting him with an alert-notification.
- This device is intended to provide the best security to all at low cost. It
is a design that doesn’t compromise efficiency for cost

![flow](https://user-images.githubusercontent.com/97796804/182678956-53179ede-23f1-4049-9d5f-066b8c2323d4.JPG)
![table](https://user-images.githubusercontent.com/97796804/182678974-43b95d77-a896-48cc-9829-ac17cd48f2a6.JPG)


## Use Cases:
- The front door is under constant surveillance making it difficult for burglars to break-in
- Easily deployable in industries, restaurants, resorts
and other places
- Updates the user about security status regularly
- Enables remote monitoring of the properties

## Dependencies:
- Requires a constant power supply for operation of RPi
- High speed internet connectivity is recommended
- Relies on mail for alerting the user
- Constant running of the python code is essential

## Uniqueness of the proposed system:
- Whenever an unknown person appears in front of the door, the owner is alerted through the **eNotify
app** and the **picture of the intruder is sent to him through mail**
- In addition to sending an unknown person’s image, the ***number of times*** and the ***dates*** on which
he/she previously visited are also sent to the owner for reference, and take further actions, if
necessary
- If the owner decides to add a known person’s image to the ‘known’ list, it just requires him to send a
***command***, specifying the person’s name, to the system. He need not send that person’s image, as it
is already present in the device
- For every command sent by the owner, a reply or an ***acknowledgment mail*** is sent by the device, to
make sure that he knows what is happening inside the system
- This system makes use of multiple ***cutting edge technologies*** like ***IoT***, ***Motion sensors***, ***Face
Recognition*** and make it a robust security system completely not dependent on CCTV

## Key Software Tools Used:
- **OpenCV:** It is used extensively to set the camera to capture the video and do image processing on the
captured frames.
- **Face Recognition:** The face recognition modules are used to load the frames, encode, determine the
location of faces in the frame and compare faces.
- **SMTP:** *Simple Mail Transfer Protocol (SMTP)* is used to send the mail to the owner whenever a new
face is detected or when an acknowledgement needs to be sent or when the owner demands the
known images database to be sent to him as a zip file.
- **IMAP:** *Internet Message Access Protocol (IMAP)* is used to access the mail server, read mail from the
mailbox, add or remove images to/from the device for which the instructions are specified via mail.
- **Pickling:** Pickling is done here to dump the encoding and names of the images into a byte stream into
the pickle file.
- **File Handling:** It is primarily used here to read from and write into files in binary format compatible with
the pickle files.


## Snapshots of OUTPUT:
(+) Live running of code<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683227-f49df4db-3064-4810-bc3c-d11bdc3f0020.jpg">
</p>
(+) System detecting a known person<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683393-abc3bc12-d283-4c98-bb03-1bc3b8f3ee44.jpg">
</p>
(+) System detecting an unknown person<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683416-378d202c-1384-43cf-9282-9f0d323e9651.jpg">
</p>
(+) Unknown Person Detected - Email<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683470-69d52de2-c4cf-40ca-81d0-28601efe4d24.jpg">
</p>
(+) REMOVE command<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683521-8753eabc-c898-47c0-a3cc-a3ebb202285c.jpg">
</p>
(+) REMOVE Acknowledgement -Email<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683554-7191befe-16c8-48c1-b046-019937bba0f8.jpg">
</p>
(+) SHOW Command<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683591-c7b710c5-9f81-48c6-8e23-f943a9beec48.jpg">
</p>
(+) SHOW Acknowledgement -Email (With Database)<br/><br/>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/97796804/182683677-f2445295-10a8-40fc-ba28-0874c2745655.jpg">
</p>

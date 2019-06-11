# SpyCam with Android app

The main purpose of this project was to create a spycam and a mobile application based on the Android system that would enable remote control. 
It was assumed that the camera will be used to observe animals in their natural environment.
The Raspberry Pi platform and the Python programming language were used to design and implement it.
The main function of the device is to take pictures and send them to the user's e-mail address as notification of camera's activity. 
Photos are placed on Google's disk. The spycam communicates via bluetooth with the Android application,
which allows the user to choose one of several functionalities, such as:
* the type of camera activity (photo / series of photos or video), 
* e-mail to which the user will receive notification and the 
* option to add an attachment to mail in the form of a registered image.

![](images/Obraz1.jpg)

The project started with the construction of a photo-trap. For proper operation of the device, a camera and a motion sensor are required.
Used elements:
* Raspberry Pi model B v1.2
* RPicamera v1.2 
* To release the camera's shutter, the program must detect movement in its field of view. For this purpose, the PIR HC-SR501 motion detector was used.
* Powerbank Trust Urban primo 8800 mAh as part of the power supply
* LG K10 (2017) - smartphone with installed application

![](images/20190221_205252.jpg)


The most important data for the user is the e-mail address to which the message arrives about the activity of the camera trap. The person that operating the application can also decide whether the message should be sent with or without attachment and in what form the images from the camera are captured.

![](images/Screenshot_2019-02-13-18-00-50.png)

## Operations description
### Taking photos:
* A camera trap is a device that is in standby mode throughout its operation.
* The state of the sensor is checked in an infinite loop
* If no presence is detected, it is forced to wait 0.3 seconds for the next reading of the variable.
* PiCamera library was used to control the camera and to take pictures or video.
* Two methods have been created, run alternately, depending on the option chosen by the user: 
  - the takePic () method to take one or more photos 
  - takeVid () method for video recording.
* Pictures are placed on Google's disk and an email is sent
## Google cloud:
* Using the account created, the virtual disk assigned to it was used and the "RPi" folder was made available.
* To allow the python application to run from the Drive API from the Google website, the credentials.json configuration file was downloaded
* Using the google's quickstart.py program, the token.json file was automatically downloaded
* Google uses OAuth 2.0 in web server applications
* Pictures are copied from a folder on Raspberry Pi to Google Drive and placed in the "RPi" folder
## Bluetooth connection:
* Client-server architecture was used using a Bluetooth connection.
* The bluez package is used for configuration and use on Linux systems.
* Server was createdOn the Raspberry Pi platform, which will be responsible for receiving messages from the Android application.
* The program works in a loop expecting a connection from the client's side
* The client was created on the Android application.

Folder 'Raspberry Pi' has the python code that supports Raspberry Pi and Spy Cam.

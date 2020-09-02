Eye-Tracking Virtual Keyborad 
=============================
Was created with the help of 
[Ahmed Hafez](https://github.com/AhmedHafez98)
[Omar Ayman](https://github.com/OmarAymanMahfouz)
[Moamon Ahmed](https://github.com/MoamenAhmedMostafa)

Software description
--------------------
The main goal of our project is to help paralyzed people, who can’t make any gesture or express their feelings,
deal with other people and communicate with them using a virtual keyboard that is displayed on the monitor and
use their eyes as a mouse to choose letters from that keyboard in order to display the chosen letters as a meaningful word that express the patient needs.

Helps limit the spread of the Coronavirus by using the apps without having to touch the mouse and keyboard.

Main Functions
-
* User will be able to write on the virtual keyboard using his eyes 
* User will be able to control the mouse using his eyes.
* User will be able to convert text to speech.
* System provide word suggestion feature

How it works
-
In [EyeTrackerV2.py](https://github.com/AhmedHafez98/EyeTracker/blob/master/EyeTrackerV2.py)
* Using open CV, dlib and numpy module to detect the image.
* Eye blanking detection.
* Gaz Detection.
* Every 10 frames we locate the landmark points of the right and left eye.
* Send the eyes landmarks to Eye blanking detection and gaz detection to get eye state for each frame.
* Find most frequent state for each 10 frames as Eye State.
* Send this state to controller

In [WordPrediction.py](https://github.com/AhmedHafez98/EyeTracker/blob/master/WordPrediction.py)
* We use machine learning algorithm here.
* We Import big.txt (huge chunk of text).
* Clean the text using regular expression.
* Divide the text into inputs and outputs.
* We use one hot encoding to make the training easier.
* Now we move to building the model using embedding layer, LSTM layer and dense layers and train it for 500 epoch.
* take text input from the controller and we return the top 5 prediction from our model.

In [Threads.py](https://github.com/AhmedHafez98/EyeTracker/blob/master/Threads.py)

we distributed every main function into different threads so that they can work in parallel

In [Controller.py](https://github.com/AhmedHafez98/EyeTracker/blob/master/Controller.py)
* here we Design VK
* connect VK buttons to keyboard keys
* connect curser tracker
* connect with eye tracker
* control VK
* connect to text to speech
* connect to word prediction
* connect to mouse
* control Mouse Tracker
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About

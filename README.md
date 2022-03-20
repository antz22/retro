<br />

<p align="middle">
    <img src="https://github.com/antz22/rello/blob/master/screenshots/landing.png" width="100%" style="margin:0; padding: 0">
</p>

<br />

<p align="middle">
  Retro is an industry-changing application that provides valuable information to first responders in the case of emergency and decentralizes the storage of medical records. 
</p>


# Inspiration
Our inspiration for this project was twofold. First, we found that, during our education in health and first-aid, many tragedies and accidents could have been easily prevented if the first responders had greater access to the medical history of the patient. For instance, knowledge of a simple allergy or a serious leg injury would greatly guide the care of a physician. Second, in the realm of healthcare, many hospitals take advantage of patients by obstructing patients from gaining access to their medical records by charging expensive fees. By decentralizing the storage of medical records and giving more power to the patient, Retro is able to improve access to healthcare for minorities who may find it more difficult to pay fees and observe crucial information on their medical history.

# What it does
Retro is a multi-faceted app that extends to both users and observers. Users register to create a unique profile of their medical history and information, such as age, sex, height, weight, and more. Then, throughout their lifetime, users can add information to the app, including information on conditions, treatments, and blood tests. In a beautiful dashboard on the web app, users can see insights on their medical history and information. More importantly, however, the app generates unique qr codes for every user that, in the case of an emergency, can be scanned by first responders to gain more insights on how best to treat the patient. Both users and doctors can also upload important PDF files to keep track of past X-Ray scans, patient files, and more, in one place.

<p align="middle">
    <img src="https://github.com/antz22/rello/blob/master/screenshots/dashboard.png" width="100%" style="margin:0; padding: 0">
</p>

# How we built it
To build our app, we used HTML and CSS on frontend in conjunction with a Python Flask backend that interacts with a Firebase Realtime Database. We also used the MapBox API and QRCode library to generate the QR Codes and provide privacy checks for only people in the perimeter of the patient to scan their qrcode.

# Challenges we ran into
During our project, we faced several challenges with finding a suitable Map API that could determine the proximity of nearby hospitals based on latitude and longitude. We also had a difficult time in using the Python Flask library in conjunction with Firebase, a combination of technologies that was new to all of us.

# Accomplishments that we're proud of
We are particularly proud of the UI design and high level of customizability of our medical portal and dashboard. The dashboard provides numerous insights onto the user’s medical history. Additionally, the added level of security with the Map API’s proximity verification was a challenging feature but turned out very nicely in the end.

# What we learned
We learned a lot about how to integrate a service such as Firebase with a Python library like Flask. In particular, the Flask framework had many issues that we needed to work around in order to properly authenticate using Firebase authentication and data. We also learned about QR code generation and the true interconnectedness of the web.

# What's next for Retro
In the future, we plan to expand Retro to be a product used across ALL hospitals, and to add a system of doctor credential validation for entering more rigorous and detailed patient information. In this way, Retro could truly revolutionize the current system of withholding medical records from patients and usher in a new era of transparency between patients and care providers.

<p align="middle">
    <img src="https://github.com/antz22/rello/blob/master/screenshots/qrcode.png" width="100%" style="margin:0; padding: 0">
</p>

# Built With

```
bootstrap
css3
firebase
flask
html5
javascript
mapbox
python
qrcode
realtime-database
```
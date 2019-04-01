# PuppyZon 

Have you seen a picture of a cute, lovable dog that made you think "I want one just like it!"

With the help of our app, now you can a dog that looks just like it!

Visit our website at:
https://puppyzon.herokuapp.com/

## Our Process

We wanted an app where the user could upload a photo and then get information on where adoptable dogs that are the same breed are currently located at. 

To do this, we used flask to take the input from the website, save it into a folder, then have the flask process and send the photo to the machine learning segment.

The ML is done by VGG19, which then guesses on what breed the dog is and will return that breed to flask. Flask then runs a search for that breed through the Petfinder API/saved CSV and returns that to the HTML/CSS where the user can see it. 

While the website can work dynamically, we chose to instead save daily petfinder data to a CSV so we could make a single API call every day instead of trying to create a new API call everytime a user wants information. 

## Files

### Folders

**Images** is where we keep all of the testing mages used for the HTML and other non-training ML parts of our project. 

**Resources** is where our CSV files for the project are held. This is where the saved pet information and the addresses.csv are incase users want to limit their search based on their zip code.

**Static** has all of the CSS/HTML/JS files for the website. 
  * **css** contains the styling sheets for our HTML
  * **images** has the images used for the HTML webstie
  * **js** has the js files being ran on our HTML
  
**Templates**: This is where our website's pages are.

**Uploads** is where user uploaded photos will be kept in order for ML to be ran on them. 

### Files

**VGG19_model** files is where the code we used to interact with VGG19 are and also the code the flask will access. 

**App.py** is our flask app that makes everything work. It feels underappreciated sometimes. 

**config.py** is where our API keys are held. 

**getBreedlist** is the code for how we generated our breed list csv files. 

**PetfinderAPI** files are how we accessed the API and were able to get the information we needed from it such as PetID, locations, breed of particular pets, etc. 

**Petfinderallrecords** gets all of the information on a national scale. This is so our CSV has all the information on petfinder everytime it's called. 

## Limitation

Machine Learning was difficult to use and implement. We eventually went with VGG19 which was a pre-trained model to use for this project. But in the future, we hope to implement a better trained model that can also recognize cats better. 



#Flask App
import os
import io
import numpy as np
import pandas as pd
from VGG19_model import predict

from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def upload_file():


    # Plan B: use CSV
    #======================================================
    results = pd.read_csv("Resources/allpets0331.csv")
    #print(f"cats and dogs: {results}")

    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the uploads folder
            file.save(filepath)
            #put in a variable the result of the predict function
            breed = predict(filepath)
            #render the homepage but with breed ifo incuded
            return render_template("index.html", breed=breed)
    
    return render_template("index.html")
            
            
@app.route('/listings')
def listings():
    """
    image_size = (224, 224)
    im = keras.preprocessing.image.load_img(filepath,
                                                    target_size=image_size,
                                                    grayscale=False)
    # preprocess the image and prepare it for classification
    image = prepare_image(im)

    #Feed into model
    #Model returns animal type and breed type
    # Make API calls and store results in results 
    """ 
    
    breedParam = request.args.get('breed')   
    results = pd.read_csv("Resources/allpets0331.csv")
    #print(results)

    param = breedParam 
    breed = param.title() 
    
        
    filtered_results = results[results["primary breed"] == breed]
    #filter by breed and state
    #filtered_results = results[(results["primary breed"] == breed) & (results["state"] == "CA")]
    filtered_results = filtered_results.fillna("")

    #print(filtered_results["primary breed"])

    filtered_results.to_csv('Resources/filtered_results.csv', header=True, index=False) 
        
    columns = list(filtered_results.columns)
    #print(f"Column titles: {columns}")


    listings = []
    for index, row in filtered_results.iterrows():
        dictionary = {}
        for col in columns:
            #print(col)
            #print(type(col))
            #print(results[col][10])
            #print(filtered_results[col])
            #print(row[col])
            dictionary[col] = row[col]
        
        listings.append(dictionary)
    
    print(f"dictionary: {listings}")

    return jsonify(listings)


if __name__ == "__main__":
    app.run(debug=True)







        




import requests
from requests.auth import HTTPDigestAuth
import os
import json
import time
import pandas as pd
import time
from pprint import pprint
from config import pet_finder_api_key, pet_finder_secret_key, gmaps_api_key
import geocoder
error_count = 0
petfinder_base_url = "https://api.petfinder.com/v2/"

# dictionary contains the address/latlong key-valule pairs addresses already geocoded
# Example:  geomapped_addresses = { "123 Main Street": "34,-120", "555 Elm Street Escondido, CA" : "33.21,-110.123" }
geomapped_addresses = {}

# https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
# removes unwanted characters (prefix) from the beginning of a string (s)
def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s

#create function for geo coding addresses
# simple library for geocoding ----  https://geocoder.readthedocs.io/ 

def geomapper(address):
    try:
        # remove leading "," from the address
        address = remove_prefix(address, ',')
        # check if address has already been geocoded, if so return that value from the geomapped_addresses dictionary
        if (address in geomapped_addresses):
            return geomapped_addresses[address]
        g = geocoder.google(address, key=gmaps_api_key)
        lat = g.json['lat']
        long = g.json['lng']
        latlong = f'{lat},{long}'
        # store the lat/long in the geomapped_addresses dictionary so we don't run the API on it again
        geomapped_addresses[address] = latlong
        
        if (len(geomapped_addresses) % 100 == 0):
            print(f"{len(geomapped_addresses)} addresses processed")
            file_name = "Resources/geomapped_addresses_temp.json"
            with open(file_name, 'w') as fp:
                json.dump(geomapped_addresses, fp, sort_keys=True, indent=4)
        return latlong
    except:
        #error_count += 1
        return None

#Create function called locateAddresses that adds latitude and longitude columns for geomapping
#Assumes df have column "address"
def locateAddresses(df):
    # Load any already geocoded addresses into geomapped_addresses dictionary
    file_name = "Resources/geomapped_addresses.json"
    if (os.path.isfile(file_name)):
        print("reading geomapped_addresses.json")
        with open(file_name, 'r') as fp:
            geomapped_addresses.update(json.load(fp))
        print(f"loaded {len(geomapped_addresses)} addresses")
        
    # create a copy of the passed in dataframe so we can manipulate it without getting reference errors
    df_temp = pd.DataFrame(df)
    df_temp["geo"] = 0
    df_temp["geo"]= df_temp.address.apply(lambda x: geomapper(x))
    #split geo column to assign values in latitude and longitude 
    df_temp[['Lat', 'Lng']] = df_temp.geo.str.split(',', expand = True)
    # no longer need the geo column...
    del df_temp['geo']
    
    # Save the geomapped_addresses dictionary to a file so we don't ever have to geomap addresses already done
    print(f"saving geomapped_addresses.json")
    with open(file_name, 'w') as fp:
        json.dump(geomapped_addresses, fp, sort_keys=True, indent=4)
        
    # return our local copy of the dataframe.  make sure you assign the return value of this function to a new df.
    return df_temp

def getAccessToken():
    url = f'{petfinder_base_url}oauth2/token'
    #print(url)
    #format post request body data
    #https://www.geeksforgeeks.org/get-post-requests-using-python/
    # data to be sent to api; data is the POST body
    data = {'grant_type':"client_credentials", 
            'client_id':pet_finder_api_key, 
            'client_secret':pet_finder_secret_key
           }
    #print(data)
    #how to add headers in python POSTS
    #https://stackoverflow.com/questions/8685790/adding-header-to-python-requests-module
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data = data, headers=headers)
    #print(response)
    if(response.ok):
        jData = json.loads(response.content)
        #print(jData)
        return jData["access_token"]
    else:
        # If response code is not ok (200)
        return None

token = getAccessToken()
print(token)

#function to get total pages of results
def totalPages(animal_type,status,limit,location):
    url = f'{petfinder_base_url}animals?type={animal_type}&status={status}&limit={limit}&location={location}'
    print(url)
    #format for calls to animal api
    #https://api.petfinder.com/v2/animals?type=dog&page=2
    #headers: Authorization: Bearer eyJ0eXA...
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers )
    if(response.ok):
        jData = json.loads(response.content)
        return jData['pagination']['total_pages']
       
    else:
        print("Not found")
        return None

def fetchPet(animal_type,limit,status,page, location):
    url = f'{petfinder_base_url}animals?type={animal_type}&limit={limit}&status={status}&page={page}&location={location}'
    print(url)
    #format for calls to animal api
    #https://api.petfinder.com/v2/animals?type=dog&page=2
    #headers: Authorization: Bearer eyJ0eXA...
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers )
    if(response.ok):
        jData = json.loads(response.content)
        return jData

    else:
        print("Not found")
        return None   

#To get total records
def getData(animal_type, limit, status, location):
    pets = []
    total_pages = totalPages(animal_type,status, limit,location)
    for  page in range(1,total_pages):
        petData = fetchPet(animal_type,limit,status,page,location)
        #print(petData)
        #append to a list from another list
        #https://stackabuse.com/append-vs-extend-in-python-lists/
        #pets.extend(petData["animals"])
        
        for row in petData["animals"]:
            
            pet_dict= {
            'pet_id': row['id'],
            'organization_id': row['organization_id'],
            'url': row['url'],
            'type': row['type'],
            'primary breed': row['breeds']['primary'],
            'secondary breed': row['breeds']['secondary'],
            'mixed breed': row['breeds']['mixed'],
            'age': row['age'],
            'gender': row['gender'],
            'size': row['size'],
            'photo1': '',
            'photo2': '',
            'photo3': '',
            'address1': '',
            'address2':'',
            'city': '',
            'state': '',
            'postcode': '',
            'email': '',
            'phone': ''
            }
            
            if len(row['photos']) > 0:
                pet_dict['photo1'] = row['photos'][0]['full']
            if len(row['photos']) > 1:
                pet_dict['photo2'] = row['photos'][1]['full']
            if len(row['photos']) > 2:
                pet_dict['photo3'] = row['photos'][2]['full']
                
                
                
            if 'contact' in row:
                contact = row['contact']
                
                if 'email' in contact:
                    pet_dict['email'] = row['contact']['email']
                if 'phone' in contact:
                    pet_dict['phone'] = row['contact']['phone']
                
                if 'address' in contact:
                    address = row['contact']['address']
                    if 'address1' in address:
                        pet_dict['address1'] = row['contact']['address']['address1']
                    if 'address2' in address:
                        pet_dict['address2'] = row['contact']['address']['address2']
                    if 'city' in address:
                        pet_dict['city'] = row['contact']['address']['city']
                    if 'state' in address:
                        pet_dict['state'] = row['contact']['address']['state']
                    if 'postcode' in address:
                        pet_dict['postcode'] = row['contact']['address']['postcode']
                
            pets.append(pet_dict)
            
    pets_city_df = pd.DataFrame(pets)
    pets_city_df = pets_city_df[["pet_id", "type", "primary breed", "secondary breed", "mixed breed", "size", "gender", "age", "photo1", "photo2", "organization_id", "phone", "address1", "address2", "city", "state", "postcode", "email"]]
  
    return pets_city_df

# load csv files if exist otherwise create by calling function getData
location = "San Diego, CA"
cats_city_df = None
cats_file = "Resources/cats_city.csv"
if (os.path.isfile(cats_file)):
    cats_city_df = pd.read_csv(cats_file)
    cats_city_df = cats_city_df.fillna("")
else:
    cats_city_df = getData(animal_type= "cat",limit = 100, status = "adoptable", location= location)
    cats_city_df.to_csv(cats_file,header=True, index=False)

dogs_city_df = None
location = "San Diego, CA"
dogs_file = "Resources/dogs_city.csv"
if (os.path.isfile(dogs_file)):
    dogs_city_df = pd.read_csv(dogs_file)
    dogs_city_df = dogs_city_df.fillna("")
else:
    dogs_city_df = getData(animal_type= "dog",limit = 100, status = "adoptable", location= location)
    dogs_city_df.to_csv(dogs_file,header=True, index=False)

print(dogs_city_df.head())

#combine cats_df and dogs_df
cats_dogs_city_df = pd.concat([cats_city_df,dogs_city_df])
print(cats_dogs_city_df.head())

#Add create combined address column and long and lat columns
#df['Name'] = df['First'].str.cat(df['Last'],sep=" ")
#dogs_df['address'] = dogs_df['address1'].str.cat(['city'],['state'],['postcode'],sep=" ")
cats_dogs_city_df['address'] = cats_dogs_city_df['address1'].map(str) + ',' + cats_dogs_city_df['city'].map(str) + ',' \
    + cats_dogs_city_df['state'].map(str)+ ' ' + cats_dogs_city_df['postcode'].map(str)
print(cats_dogs_city_df.head())

print(len(cats_dogs_city_df["address"].unique()))

#Add latitude and longitude columns for gmapping using the locateAddresses function
city_all_pets_file = "Resources/city_allpets.csv"
citypets_geo_df = None
if (os.path.isfile(city_all_pets_file)):
    citypets_geo_df = pd.read_csv(city_all_pets_file)
else:
    citypets_geo_df = locateAddresses(cats_dogs_city_df)
    citypets_geo_df.to_csv(city_all_pets_file,header=True, index=False)
print(citypets_geo_df.head())


#TEST:  to return all results for a specific breed
breed = "Chihuahua"
state = "CA"
city = "San Diego"
citypets_geo_df =  citypets_geo_df.loc[(citypets_geo_df['primary breed']==breed)&(citypets_geo_df['city']==city ),:]
print(citypets_geo_df.head())




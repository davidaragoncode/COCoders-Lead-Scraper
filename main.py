import os
import requests
import json
import csv
import pandas as pd
from pandas import json_normalize



# Load Google Maps API key from environment variable
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
# read up on python interpretors

keywords_file_path = 'keywords_short.csv'
stored_data_file_path = "data.json"
exceptions_data_file_path = "exceptions.json"

storage_frame = None

place_details_base_url = 'https://maps.googleapis.com/maps/api/place/details/json'
place_detail_params = {
        'key': GOOGLE_MAPS_API_KEY,
        'place_id': None,
        'fields': 'name,formatted_address,formatted_phone_number,website',
    }
def get_place_details(place_id):
    place_detail_params['place_id'] = place_id
    try:
        response = requests.get(place_details_base_url, params=place_detail_params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK' and 'result' in data:
            place_details = data['result']
            return place_details
        else:
            return None
    except requests.exceptions.RequestException as error:
        print(f'Error getting place details: {error}')


def create_place_id_list(json_file_path):
    if os.path.exists(json_file_path):
        # If the file exists, read the existing JSON data and then append data to it
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            return_list = [item['place_id'] for item in existing_data]
    else:
        # If the file doesn't exist, start with an empty dictionary
        print("Theres no data file to read from, pay attention to where you've called this function")
    return return_list


def update_json_file(data_list, json_file_path="data.json"):
    """
    Update a JSON file with data from a list.

    Parameters:
    - data_list (list): List of data to be added or updated in the JSON file.
    - json_file_path (str): Path to the JSON file.

    Returns:
    - None
    """

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # If the file exists, read the existing JSON data and then append data to it
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            for item in data_list:
                existing_data.append(item)
            print("New data added to JSON file.")
            print(f"Current Stored List Length: {len(existing_data)}")
    else:
        # If the file doesn't exist, start with an empty dictionary
        print("Data added to JSON file.")
        existing_data = data_list

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)


def print_data_names(json_file_path):
    with open(json_file_path, 'r') as json_file:
        existing_data = json.load(json_file)
        print(len(existing_data))
        for index in existing_data:
            print(index['name'])


def get_keyword_list(file_path):
    keyword_list = []
    # opening the CSV file
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        keyword_list = [lines[0] for lines in csvFile]
    return keyword_list


def find_nearby_businesses(latitude, longitude, keyword):
    try:

        radius = 50000  # 1 mile in meters
        local_keyword = keyword  # Adjust this keyword based on your criteria
        print(local_keyword)
        response = requests.get(
            f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={local_keyword}&key={GOOGLE_MAPS_API_KEY}'
        )

        response.raise_for_status()
        # print(response)
        # print("response.status_code =", response.status_code)
        # # print("response.text= ", response.text)
        # # print(response.text['results'])
        # data2 = response.text
        # print(data2[0])
        data = response.json()
        # data_frame = pd.DataFrame(data)
        print(f"Results Length: {len(data['results'])}")

        # filtered_businesses = [
        #     pd.DataFrame(place) for place in data['results'] if (
        #             place.get('business_status') == 'OPERATIONAL' and
        #             not place.get('website')
        #     )
        # ]
        dict = {"business_status": "OPERATIONAL",
            "geometry": {
                "location": {
                    "lat": 39.7233677,
                    "lng": -104.6928107
                },
                "viewport": {
                    "northeast": {
                        "lat": 39.72471752989272,
                        "lng": -104.6915810701073
                    },
                    "southwest": {
                        "lat": 39.72201787010728,
                        "lng": -104.6942807298927
                    }
                }
            },
            "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png",
            "icon_background_color": "#7B9EB0",
            "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet",
            "name": "Mile High Business Solutions LLC",
            "opening_hours": {
                "open_now": True
            },
            "photos": [
                {
                    "height": 1280,
                    "html_attributions": [
                        "<a href=\"https://maps.google.com/maps/contrib/107051759630075740918\">A Google User</a>"
                    ],
                    "photo_reference": "AWU5eFjTKldVon_YNFSkhJhIbH9C-fUY_qAm0afdyTnWvTsQsV1qk2U4AU_5r9UBu0Zhi1zSRQZzj09gz8ww7m1g6P27_ObYkOXoPQ6jawiVFF47182E13RlRYI1mkNIQNa0T1DAU-iI-cT62MxWwlSSRu_2e6qQnjncHWMIh8rchzwAw5mR",
                    "width": 1280
                }
            ],
            "place_id": "ChIJsWd3b_9hbIcRHbHCIBjpFJA",
            "plus_code": {
                "compound_code": "P8F4+8V Aurora, Colorado",
                "global_code": "85FQP8F4+8V"
            },
            "rating": 0,
            "reference": "ChIJsWd3b_9hbIcRHbHCIBjpFJA",
            "scope": "GOOGLE",
            "types": [
                "accounting",
                "finance",
                "point_of_interest",
                "establishment"
            ],
            "user_ratings_total": 0,
            "vicinity": "452 N Jackson Gap Way 344 S 4th Ct, 452 N Jackson Gap Way, Aurora"
        }
        print("0")
        place_dataframe = {"business_status": None,
            "geometry": None ,
            "icon": None,
            "icon_background_color": None,
            "icon_mask_base_uri": None,
            "name": None,
            "opening_hours": None,
            "photos": None,
            "place_id": None,
            "plus_code": None,
            "rating": None,
            "reference": None,
            "scope": None,
            "types": None,
            "user_ratings_total": None,
            "vicinity": None
        }

        # {},[0]



        print("0.5")
        businesses = pd.DataFrame(place_dataframe,[0])
        print("1")
        for place in data['results']:
            Holder = place_dataframe
            print("2")
            print(place_dataframe)
            for k,v in place_dataframe.items():
                try:
                    Holder[k] = place[k]
                    print("2.5")
                except:
                    Holder[k] = None
                    print("2.6")
                else:
                    pass
            print("3")
            businesses.loc[len(businesses)]=Holder
        print(businesses['name'])
        #
        # empty_df = json_normalize(empty_dict)
        # filtered_businesses = json_normalize(dict)
        # print(type(filtered_businesses))
        # for place in data['results']:
        #     holder = empty_df
        #     if (place.get('business_status') == 'OPERATIONAL'):
        #         print("Triggered")
        #         to_add = json_normalize(place)
        #         # filtered_businesses = filtered_businesses.append(pd.Series(place), ignore_index=True)
        #         # test = filtered_businesses.merge(to_add, how='left', on='a')
        #         test = filtered_businesses.merge(pd.Series(place,name = "Place" ), how='left', on='a')
        #         print(test)
        #         # # pd.concat([filtered_businesses,to_add])
        #         # to_append = holder.add(to_add, axis='columns')
                # print(to_append)
                # print(to_append)
                # print(len(filtered_businesses))
                # print(len(to_add))
                # print(to_add)
                # # filtered_businesses.iloc[len(filtered_businesses)] = to_add
                # filtered_businesses.loc[len(filtered_businesses)] = to_add




        return businesses

    except requests.exceptions.RequestException as error:
        print(f'Error fetching nearby businesses: {error}')
        raise


# Finds a place based on specific keywords
def find_place(input_text, lat, long):
    base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    radius = 1600
    params = {
        'key': GOOGLE_MAPS_API_KEY,
        'input': input_text,
        'inputtype': 'textquery',
        'fields': 'name,formatted_address,place_id',
        # 'fields': 'name,formatted_address,formatted_phone_number,website',
        'circular': f"{radius}@{lat}.{long}"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK' and data.get('candidates'):
            place_info = data['candidates'][0]
            return place_info
        else:
            return None

    except requests.exceptions.RequestException as error:
        print(f'Error finding place: {error}')
        raise


# # Example usage:
# input_text = 'Space Needle, Seattle'  # Replace with the place you want to search
#
# try:
#     place_info = find_place(GOOGLE_MAPS_API_KEY, input_text)
#     if place_info:
#         print('Place Name:', place_info.get('name'))
#         print('Formatted Address:', place_info.get('formatted_address'))
#         print('Place ID:', place_info.get('place_id'))
#         print('Latitude:', place_info['geometry']['location']['lat'])
#         print('Longitude:', place_info['geometry']['location']['lng'])
#     else:
#         print('Place not found.')
#
# except Exception as error:
#     print(f'Error: {error}')


# Broomfield:
latitude = 39.890240  # Example latitude
longitude = -105.104759


# # San Fran
# latitude = 37.7749  # Example latitude
# longitude = -122.4194  # Example longitude

# def main():
#     try:
#         keyword_list = get_keyword_list(keywords_file_path)
#         for item in keyword_list:
#             businesses = find_place(item,latitude,longitude)
#             print(businesses)
#     except Exception as error:
#         print(f'Error: {error}')
#

def exception_finder(list_of_place_details):

    output_dict = {
        'Name': [''],
        'Website': [''],
        'Phone-number': ['']
    }

    place_site_name = "No Data"
    place_website = "No Data"
    place_telephone_number = "No Data"

    storage = pd.DataFrame(output_dict)

    for place_details in list_of_place_details:
        try:
            place_site_name = place_details['name']
            place_website = place_details['website']
            try:
                place_telephone_number = place_details['formatted_phone_number']
            except Exception("There do does appear to be a phone number for this Place"):
                storage.loc[len(storage.index)] = [place_site_name, "NO WEBSITE", "NO NUMBER"]
            else:
                pass
        except Exception:
            storage.loc[len(storage.index)] = [place_site_name, "NO WEBSITE", place_telephone_number]
        else:
            place_telephone_number = place_details['formatted_phone_number']

        # Line below adds non exceptions to return data frame
        # storage.loc[len(storage.index)] = [place_site_name, place_website, place_telephone_number]

    return storage


def main(kfp, sdfp):
    keyword_list = get_keyword_list(kfp)
    for item in keyword_list:
        list_of_places = find_nearby_businesses(latitude, longitude, item)
        update_json_file(list_of_places, sdfp)
        print("")



    with open(sdfp, 'r') as json_file:
        existing_data = json.load(json_file)
        df = pd.DataFrame(existing_data)
        print(df)
        # print(len(existing_data))
        # print(existing_data[0])
        ind = 0
        holder = place.Place()
        dict = {
        'business_status': [existing_data[ind]['business_status']],
        'geometry' : [existing_data[ind]['geometry']],
        'icon' : [existing_data[ind]['icon']],
        'icon_background_color' : [existing_data[ind]['icon_background_color']],
        'icon_mask_base_uri' : [existing_data[ind]['icon_mask_base_uri']],
        'name' : [existing_data[ind]['name']],
        'opening_hours' : [existing_data[ind]['opening_hours']],
        'place_id' : [existing_data[ind]['place_id']],
        'plus_code' : [existing_data[ind]['plus_code']],
        'rating' : [existing_data[ind]['rating']],
        'reference' : [existing_data[ind]['reference']],
        'scope' : [existing_data[ind]['scope']],
        'types' : [existing_data[ind]['types']],
        'user_ratings_total' : [existing_data[ind]['user_ratings_total']],
        'vicinity' : [existing_data[ind]['vicinity']],
        }




    list_of_places_ids = create_place_id_list(sdfp)


    # print(get_place_details(list_of_places_ids[0]))
    # test_frame = pd.DataFrame(get_place_details(list_of_places_ids[0]))
    # print(test_frame)


    list_of_place_details = [get_place_details(place_id) for place_id in list_of_places_ids]
    frame = exception_finder(list_of_place_details)
    print(frame)
    # previous main


def big_search():
    try:
        main(keywords_file_path, stored_data_file_path)

    except Exception as error:
        print(f'Error: {error}')


if input("Are you sure you want to run big search? (y/n)") == "y":
    big_search()

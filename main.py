import os
import requests
import json
import csv

# Load Google Maps API key from environment variable
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
#read up on python interpretors

keywords_file_path = 'keywords.csv'
stored_data_file_path = "data.json"
exceptions_data_file_path = "exceptions"







def get_place_details(place_id):
    base_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
    'key': GOOGLE_MAPS_API_KEY,
    'place_id': place_id,
    'fields': 'name,formatted_address,formatted_phone_number,website',
    }

    try:
        response = requests.get(base_url, params=params)
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



def update_json_file(data_list, json_file_path = "data.json"):
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
    with open(file_path, mode ='r')as file:
    # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        keyword_list = [lines[0] for lines in csvFile]
    return keyword_list


def find_nearby_businesses(latitude, longitude, keyword):
    try:

        radius = 50000 # 1 mile in meters
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
        print(f"Results Length: {len(data['results'])}")

        # filtered_businesses = [
        #     place for place in data['results'] if (
        #         place.get('business_status') == 'OPERATIONAL' and
        #         'establishment' in place.get('types', []) and
        #         'point_of_interest' in place.get('types', []) and
        #         'store' in place.get('types', []) and
        #         'restaurant' in place.get('types', []) and
        #         'food' in place.get('types', []) and
        #         'bar' in place.get('types', []) and
        #         'cafe' in place.get('types', []) and
        #         'lodging' in place.get('types', []) and
        #         place.get('employees', 0) < 10 and
        #         not place.get('website') and
        #         place.get('formatted_phone_number')
        #     )
        # ]
        # filtered_businesses = [
        #     place for place in data['results'] if (
        #             place.get('business_status') == 'OPERATIONAL'and
        #             not place.get('website') and
        #             place.get('formatted_phone_number')
        #     )
        #
        # ]
        filtered_businesses = [
            place for place in data['results'] if (
                    place.get('business_status') == 'OPERATIONAL' and
                    not place.get('website')
            )

        ]

        return filtered_businesses

    except requests.exceptions.RequestException as error:
        print(f'Error fetching nearby businesses: {error}')
        raise


# Finds a place based on specific keywords
def find_place(input_text,lat,long):
    base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    radius = 1600
    params = {
        'key': GOOGLE_MAPS_API_KEY,
        'input': input_text,
        'inputtype': 'textquery',
        'fields': 'name,formatted_address,place_id',
        # 'fields': 'name,formatted_address,formatted_phone_number,website',
        'circular':f"{radius}@{lat}.{long}"
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




#Broomfield:
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



#previous main
def big_search():
    try:
        keyword_list = get_keyword_list(keywords_file_path)
        for item in keyword_list:
            businesses = find_nearby_businesses(latitude, longitude, item)
            update_json_file(businesses, stored_data_file_path)
            print("")
        place_id_list = create_place_id_list(stored_data_file_path)
        place_details = [get_place_details(place_id)for place_id in place_id_list]
        # print(place_details)
        for item in place_details:
            try:
                place_site_name = item['name']
                place_telephone_number = item['formatted_phone_number']
                place_website = item['website']
            except Exception:
                print(f"Place Name: {item['name']}")
            else:
                print(f"Place Name: {place_site_name}, Place Number: {place_telephone_number}, Place Website: {place_website}")
    except Exception as error:
        print(f'Error: {error}')


if input("Are you sure you want to run big search? (y/n)")=="y":
    big_search()
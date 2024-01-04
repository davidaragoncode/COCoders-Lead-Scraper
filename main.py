import os
import requests
import json
import csv
import pandas as pd
import time
from pandas import json_normalize

# Load Google Maps API key from environment variable
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
NEARBY_SEARCH_ENDPOINT = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
# read up on python interpretors
chino_hills_machine_shop_search = (34.010770, -117.693511)

# keywords_file_path = 'keywords_short.csv'
# keywords_file_path = 'keywords.csv'
keywords_file_path = 'Machine_Shops.csv'
stored_data_file_path = "data.json"
exceptions_data_file_path = "exceptions.json"

storage_frame = None

place_details_base_url = 'https://maps.googleapis.com/maps/api/place/details/json'
place_detail_params = {
    'key': GOOGLE_MAPS_API_KEY,
    'place_id': None,
    'fields': 'name,formatted_address,formatted_phone_number,website',
}


def get_keyword_list(file_path):
    keyword_list = []
    # opening the CSV file
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        keyword_list = [lines[0] for lines in csvFile]
    return keyword_list


def find_nearby_businesses(location: tuple, keyword: str, fakeData: bool) -> pd.DataFrame:
    
# combine with next page to return maz results 
    search_radius = 20000  # meters
    max_search_radius = 50000  # meters

    api_params = {
        'location': f"{location[0]},{location[1]}",
        'radius': search_radius,
        'key': GOOGLE_MAPS_API_KEY,
        'keyword': keyword
    }
    #api_params.update({'pagetoken':data['next_page_token']})

    if fakeData:

        print('add data faking')

    else:
        try:
            response = requests.get(NEARBY_SEARCH_ENDPOINT, params=api_params)

            response.raise_for_status()
            # print(response)
            # print("response.status_code =", response.status_code)
            # print("response.text= ", response.text)

            data = response.json()
            print(f"Results Length: {len(data['results'])}")

            return data
            # return json_to_panda(data)

        except requests.exceptions.RequestException as error:
            print(f'Error fetching nearby businesses: {error}')
            empty_place_dataframe = {"business_status": None,
                                     "geometry": None,
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
            return json_to_panda(empty_place_dataframe)

        raise ("find_nearby_businesses function failed to return something")


def find_nearby_businesses_next_page(location: tuple, token:str) -> pd.DataFrame:
    search_radius = 20000  # meters
    max_search_radius = 50000  # meters

    api_params = {
        'location': f"{location[0]},{location[1]}",
        'radius': search_radius,
        'key': GOOGLE_MAPS_API_KEY,
        'token': token
    }

    # This is weird

    try:
        response = requests.get(NEARBY_SEARCH_ENDPOINT, params=api_params)

        response.raise_for_status()
        # print(response)
        # print("response.status_code =", response.status_code)
        # print("response.text= ", response.text)

        data = response.json()
        print(f"Results Length: {len(data['results'])}")

        return data
        # return json_to_panda(data)

    except requests.exceptions.RequestException as error:
        print(f'Error fetching nearby businesses: {error}')
        empty_place_dataframe = {"business_status": None,
                                 "geometry": None,
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
        return json_to_panda(empty_place_dataframe)

        raise ("find_nearby_businesses function failed to return something")


# No idea what this is
# def API_nearv(latitude, longitude, keyword)->pd.DataFrame:
#     try:


def update_json_file(data_list: pd.DataFrame, json_file_path="data.json"):
    """
    Update a JSON file with data from a list.

    Parameters:
    - data_list (list): List of data to be added or updated in the JSON file.
    - json_file_path (str): Path to the JSON file.

    Returns:
    - None
    """

    """
    Path\main.py:66: FutureWarning: Passing literal json to 'read_json' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.
    print(pd.read_json(data_list.to_json()))
    """

    """
    with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url) 
        if data:
            for product in data['products']:
                product['search_url'] = url
                print("Saving Product: %s"%product['title'])
                json.dump(product,outfile)
                outfile.write("\n")
                # sleep(5)
    """
    print("1")
    print(pd.read_json(data_list.to_json()))
    print("2")

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        print("3y")

        # with open(json_file_path, 'w') as json_file:
        #     json.dump(data_list.to_json(), json_file, indent=2)

        # If the file exists, read the existing JSON data and then append data to it
        with open(json_file_path, 'r') as json_file:

            print("4")
            print(json_file)
            existing_data = json.load(json_file)
            print('5')

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


def print_data_names(json_file_path):
    with open(json_file_path, 'r') as json_file:
        existing_data = json.load(json_file)
        print(len(existing_data))
        for index in existing_data:
            print(index['name'])


def json_to_panda(search_nearby_api_response: object) -> object:
    place_dataframe = {"business_status": None,
                       "geometry": None,
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

    businesses = pd.DataFrame(place_dataframe, [0])
    for place in search_nearby_api_response['results']:
        Holder = place_dataframe
        for k, v in place_dataframe.items():
            try:
                Holder[k] = place[k]
            except:
                Holder[k] = None
            else:
                pass
        businesses.loc[len(businesses)] = Holder

    return businesses


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
        list_of_places = find_nearby_businesses(latitude, longitude, item, False)
        update_json_file(list_of_places, sdfp)
        print("")

    with open(sdfp, 'r') as json_file:
        existing_data = json.load(json_file)
        df = pd.DataFrame(existing_data)
        print("in main open r")
        print(df)

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


if input(
        "Do you want to run a detailed search to find what businesses don't have websites in a very large area? (y/n)") == "y":
    big_search()
elif input("Do you want to read all place results for a specific keyword list in a smaller area? (y/n)") == "y":
    data = find_nearby_businesses(chino_hills_machine_shop_search, ['Machine Shop'], False)
    time.sleep(60)
    data2 = find_nearby_businesses_next_page(chino_hills_machine_shop_search, data['next_page_token'])
    time.sleep(60)
    data3 = find_nearby_businesses_next_page(chino_hills_machine_shop_search, data2['next_page_token'])
    # print("data")
    # print(data)
    # print("data2")
    # print(data2)
    print(data3)
    search_results = data['results']
    print(len(search_results))
    search_results = search_results + data2['results'] + data3['results']
    # for index in search_results:
    #     print(index)
    print(len(search_results))


    out = pd.DataFrame(search_results)
    print(out)
    compression_opts = dict(method='zip', archive_name='out.csv')
    out.to_csv('out.zip', index=False, compression=compression_opts)

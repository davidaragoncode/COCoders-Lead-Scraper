import os
import requests
import csv
import pandas as pd
import time
from web_stuff import has_careers_page

# Load Google Maps API key from environment variable
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
NEARBY_SEARCH_ENDPOINT = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
PLACE_DETAILS_ENDPOINT = 'https://maps.googleapis.com/maps/api/place/details/json'

chino_hills = (34.010770, -117.693511)

# keywords_file_path = 'keywords_short.csv'
# keywords_file_path = 'keywords.csv'
keywords_file_path = 'keywords_short.csv'


def get_keyword_list(file_path):
    # This function takes a keyword csv, single lines and make a list out of it.
    # a, b, c, -> [a,b,c]

    keyword_list = []
    # opening the CSV file
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        keyword_list = [lines[0] for lines in csvFile]
    return keyword_list


def response_check(response):
    print(response)
    print("response.status_code =", response.status_code)
    print("response.text= ", response.text)


def search_keyword_at_a_location(location: tuple, keyword: str, fake_data=False, max_results=60,
                                 search_radius=20000) -> list:
    # This is the main search function. Essentially just googles a keyword at a given location a returns results, not the response.
    # consider integrating type
    # combine with next page to return maz results
    # returns a list of places

    max_search_radius = 50000  # meters

    api_params = {
        'location': f"{location[0]},{location[1]}",
        'radius': search_radius,
        'key': GOOGLE_MAPS_API_KEY,
        'keyword': keyword
    }

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

    search_results = None

    # the

    if fake_data:
        print('add data faking')
    else:
        try:
            response = requests.get(NEARBY_SEARCH_ENDPOINT, params=api_params)
            response.raise_for_status()
            # response_check(response)
            data = response.json()
            next_page_token = data.get('next_page_token')
            search_results = data['results']
            # check to see if you want to return max results (60)
            if max_results <= 20:
                return search_results[:max_results]
            # check to see if there are any additonal results
            if next_page_token == None:
                return search_results[:max_results]
                # return data['results']
            else:
                npt = True
                while npt:
                    # the delay below is actually required. Google needs a bit of time to respond
                    time.sleep(2)

                    api_params.update({'pagetoken': next_page_token})
                    # running search again to find additional results
                    try:
                        response = requests.get(NEARBY_SEARCH_ENDPOINT, params=api_params)
                        response.raise_for_status()
                        additional_data = response.json()
                        search_results = search_results + additional_data['results']
                        next_page_token = additional_data.get('next_page_token')

                        # checking to see if there are even more results
                        if next_page_token == None:
                            npt = False
                            return search_results[:max_results]

                    except requests.exceptions.RequestException as error:
                        print(f'Error additional page results: {error}')
                        npt = False

            return search_results[:max_results]
            # return json_to_panda(data)

        except requests.exceptions.RequestException as error:
            print(f'Error fetching nearby businesses: {error}')
            return None

        raise ("search_keyword_at_a_location function failed to return something")


def search_a_list_of_places_for_details(list_of_places) -> list[dict]:
    list_of_places_ids = [i['place_id'] for i in list_of_places]
    list_of_place_details = [get_place_details(place_id) for place_id in list_of_places_ids]
    return list_of_place_details


def get_place_details(place_id):
    place_detail_params = {
        'key': GOOGLE_MAPS_API_KEY,
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,place_id',
    }

    try:
        response = requests.get(PLACE_DETAILS_ENDPOINT, params=place_detail_params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK' and 'result' in data:
            place_details = data['result']
            return place_details
        else:
            return None
    except requests.exceptions.RequestException as error:
        print(f'Error getting place details: {error}')


def make_out_file_mwah(data_to_export, export_file_name='out'):
    print("making out file")
    out = pd.DataFrame(data_to_export)
    out.to_csv(export_file_name, index=False)


def search_nearby_a_location_with_a_list_of_keywords(location: tuple,
                                                     keyword_list_file_path="keywords_short.csv") -> list:
    keyword_list = get_keyword_list(keyword_list_file_path)
    search_results = None
    for keyword in keyword_list:
        # this start of this block creates a csv of results for a specific keyword
        data = search_keyword_at_a_location(location, keyword)
        search_results = search_results + data['results']
    return search_results


# future job application automation
if input("simple code run? (y/n)") == "y":
    list_of_places = search_keyword_at_a_location(location=chino_hills, keyword='fastfood', max_results=5)
    list_of_places_details = search_a_list_of_places_for_details(list_of_places)

    list_of_places_with_websites = [i.get('website')
                                    for i in list_of_places_details
                                    if (not (i.get('website') == None))]
    # list_of_places_without_websites = [i.get('name') for i in list_of_places_details if (i.get('website') == None)]

    list_of_places_with_websites_with_career_sections = [j for j in list_of_places_with_websites
                                                         if (has_careers_page(j))]

    make_out_file_mwah(list_of_places_with_websites_with_career_sections,
                     'list_of_places_with_websites_with_career_sections_keyword_fast_food')

    print(list_of_places_with_websites_with_career_sections)

# if input("Do you want to read all place results for a specific keyword list in a smaller area? (y/n)") == "y":
#     data = search_nearby_a_location_with_a_list_of_keywords(chino_hills, keywords_file_path)
#     make_an_out_file(data, 'simple_search.csv')
#

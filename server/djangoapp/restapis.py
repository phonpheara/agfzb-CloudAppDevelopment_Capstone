import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("Y9YAwI-lLXGRtP0rqIiMitURXxA_2EHHWQBP1Jf6ssmj")
    print("GET from {} ".format(url))
    
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except requests.RequestException as e:
        # If any error occurs during the request
        print(f"Network exception occurred: {e}")
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))

    if response.text:
        try:
            json_data = json.loads(response.text)
            return json_data
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        # Handle empty response
        print("Empty response received")
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in 'doc' object
            dealer_doc = dealer
            # Create a CarDealer object with values in 'doc' object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                  id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], short_name=dealer_doc["short_name"],
                                  st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
        return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result and isinstance(json_result, list):
        reviews = json_result
        for dealer_review in reviews:
            if isinstance(dealer_review, dict):
                review_obj = DealerReview(
                    dealership=dealer_review.get("dealership", ""),
                    name=dealer_review.get("name", ""),
                    purchase=dealer_review.get("purchase", ""),
                    review=dealer_review.get("review", "")
                )
                if "id" in dealer_review:
                    review_obj.id = dealer_review["id"]
                if "purchase_date" in dealer_review:
                    review_obj.purchase_date = dealer_review["purchase_date"]
                if "car_make" in dealer_review:
                    review_obj.car_make = dealer_review["car_make"]
                if "car_model" in dealer_review:
                    review_obj.car_model = dealer_review["car_model"]
                if "car_year" in dealer_review:
                    review_obj.car_year = dealer_review["car_year"]

                sentiment = analyze_review_sentiments(review_obj.review)
                print(sentiment)
                review_obj.sentiment = sentiment
                results.append(review_obj)

    return results

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result and isinstance(json_result, list):
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            if isinstance(dealer, dict) and dealer.get("id") == id:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer.get("address", ""), 
                                       city=dealer.get("city", ""), 
                                       full_name=dealer.get("full_name", ""),
                                       id=dealer.get("id", ""), 
                                       lat=dealer.get("lat", ""), 
                                       long=dealer.get("long", ""),
                                       short_name=dealer.get("short_name", ""),
                                       st=dealer.get("st", ""), 
                                       zip=dealer.get("zip", ""))                    
                results.append(dealer_obj)

    return results[0] if results else None

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentimentssss(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6a7cbbea-386b-4980-a2d1-11477f8e6e19"
    api_key = "hLJR9ceiYZu0nTzjOQbDgYxfesSrtv7ujHcgdMh0ki-f"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/bb3023b7-ff44-45bb-938a-1373a05af3ae"
    api_key = "tsR0cp-DXyEHAKC8PMhfYtbM8Ek8q-LTqvpAjoAkNohx"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    try:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=[text]))
        ).get_result()
        label = response['sentiment']['document']['label']
    except Exception as e:
        print("Exception occurred during sentiment analysis:", str(e))
        label = "unknown"
    
    return label


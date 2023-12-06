import requests

url = "https://api.mixpanel.com/track"

payload = [
    {
        "event": "CompletedOrder",
        "properties": {
            "token": "4b1009bbca2c2045c5b045d9e75c6e49",
            "time": 1700795411.116,
            "distinct_id": "evans.menza374@gmail.com",
            "$browser": "Chorme",
            "$browser_version": 119,
            "$city": "Nairobi",
            "$current_url": "https://business.jungopharm.com/procurement/1536?bid=1273&name=Belea%20Pharmaceuticals%20Limited",
            "$device_id": "18bfc52cee13a8-0986b9c0c458428-e555620-100200-18bfc52cee13a8",
            "$email": "evans.menza374@gmail.com",
            "$initial_referrer": "$direct",
            "$initial_referring_domain": "$direct",
            "$insert_id": "mqzjfd41j0bqeoik",
            "$lib_version": "2.47.0",
            "$mp_api_endpoint": "api-js.mixpanel.com",
            "$mp_api_timestamp_ms": 1700745415334,
            "$name": "Evans Menza",
            "$os": "Windows",
            "$region": "Oslo County",
            "$screen_height": 768,
            "$screen_width": 1366,
            "$user_id": "evans.menza374@gmail.com",
            "businessname": "JAMON CHEMIST (Nairobi)",
            "businesstype": "PHARMACY",
            "mp_country_code": "KE",
            "mp_lib": "web",
            "mp_processing_time_ms": 1700745415523,
            "mp_sent_by_lib_version": "2.47.0",
            "nameofdistributor": "Belea Pharmaceuticals Limited",
            "paymentmethod": "MPESA",
            "phonenumber": "0728112423",
            "platform": "web",
            "totalamount": 32274.138,
            "usertype": "owner"
        }
    }
]

# def update_code(payload, event_change, new_country_code):
#     for event in payload:
#         if 'properties' in event and event_change in event['properties']:
#             event['properties'][event_change] = new_country_code
#     return payload
#
#
# # payload = update_code(body, 'mp_country_code', 'KE')
# # payload = update_code(payload, '$city', 'Nairobi')
# # payload = update_code(payload, '$region', 'Nairobi')
# # add new property in the payload             "token": "4b1009bbca2c2045c5b045d9e75c6e49",
#
# # for event in payload:
#     event['properties']['token'] = "4b1009bbca2c2045c5b045d9e75c6e49"

headers = {
    "accept": "text/plain",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
print(response.status_code)
print(response)
3
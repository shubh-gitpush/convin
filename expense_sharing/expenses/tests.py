
from django.test import Client

client = Client()
response = client.post('/api/add-expense/', {
    "total_amount": 3000,
    "description": "Dinner with friends",
    "participants": [
        {"user_id": 1, "split_method": "equal"},
        {"user_id": 2, "split_method": "equal"},
        {"user_id": 3, "split_method": "equal"}
    ]
}, content_type='application/json')

print(response.status_code)  # Should print 200 or 201 if successful
print(response.content)       # Print the response data


# Create your tests here.

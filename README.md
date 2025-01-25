# RoomieU
QHacks 2025

Note: For the below requests, the example IDs may be invalid if the database has changed. Use valid IDs (see database).

Add user:
```
curl -X POST http://127.0.0.1:5000/add_user -H "Content-Type: application/json" -d "{\"username\": \"john_doe\", \"email\": \"john@example.com\", \"password\": \"secure_password\", \"school\": \"Example University\", \"age\": 25, \"gender\": \"Male\", \"is_listing\": false}"
```

Add listing (replace USER_ID with the lister's user ID):
```
curl -X POST http://127.0.0.1:5000/add_house/USER_ID -H "Content-Type: application/json" -d "{ \"type\": \"Apartment\", \"rooms_available\": 2, \"rent\": 1200, \"utilities_included\": true }"
```
ex. USER_ID=679486f52cbb9e9a76e75104

Swipe (replace USER_ID with the swiper's user ID and TARGET_ID with the target/liked user's ID):
```
curl -X POST http://127.0.0.1:5000/swipe -H "Content-Type: application/json" -d "{ \"user_id\": \"679486f52cbb9e9a76e75104\", \"target_user_id\": \"TARGET_ID\", \"action\": \"like\" }"
```
ex. USER_ID=679486f52cbb9e9a76e75104, 67948c725412ccef7a098212

Get matches (replace USER_ID with the user ID):
```
curl -X GET http://127.0.0.1:5000/matches/USER_ID
```
ex. USER_ID=679486f52cbb9e9a76e75104

Send message (replace MATCH_ID, SENDER_ID, RECEIVER_ID):
```
curl -X POST http://127.0.0.1:5000/send_message -H "Content-Type: application/json" -d "{ \"match_id\": \"MATCH_ID\", \"sender_id\": \"SENDER_ID\", \"receiver_id\": \"RECEIVER_ID\", \"message\": \"Hey, how are you? winkyface\"}"
```
ex. MATCH_ID=67948cfccd3a78361e4bed1f, SENDER_ID=67948c725412ccef7a098212, RECEIVER_ID=679486f52cbb9e9a76e75104

Get chat messages (replace MATCH_ID):
```
curl -X GET http://127.0.0.1:5000/get_messages/MATCH_ID
```
ex. MATCH_ID=67948cfccd3a78361e4bed1f

# RoomieU
QHacks 2025

Add user:
```
curl -X POST http://127.0.0.1:5000/add_user -H "Content-Type: application/json" -d "{\"username\": \"john_doe\", \"email\": \"john@example.com\", \"password\": \"secure_password\", \"school\": \"Example University\", \"age\": 25, \"gender\": \"Male\", \"is_listing\": true, \"house_listing\": {\"type\": \"Apartment\", \"rooms_available\": 2, \"rent\": 1200, \"utilities_included\": true}}"
```

Add listing:
```
curl -X POST http://127.0.0.1:5000/add_house/679486f52cbb9e9a76e75104 -H "Content-Type: application/json" -d "{ \"type\": \"Apartment\", \"rooms_available\": 2, \"rent\": 1200, \"utilities_included\": true }"
```

Swipe:
```
curl -X POST http://127.0.0.1:5000/swipe -H "Content-Type: application/json" -d "{ \"user_id\": \"679486f52cbb9e9a76e75104\", \"target_user_id\": \"67948c725412ccef7a098212\", \"action\": \"like\" }"
```

Get matches:
```
curl -X GET http://127.0.0.1:5000/matches/679486f52cbb9e9a76e75104
```

Send message:
```
curl -X POST http://127.0.0.1:5000/send_message -H "Content-Type: application/json" -d "{ \"match_id\": \"67948cfccd3a78361e4bed1f\", \"sender_id\": \"67948c725412ccef7a098212\", \"receiver_id\": \"679486f52cbb9e9a76e75104\", \"message\": \"Hey, how are you? winkyface\"}"
```

Get chat messages:
```
curl -X GET http://127.0.0.1:5000/get_messages/67948cfccd3a78361e4bed1f
```
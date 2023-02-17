### Bugs: 
1. 'movies' app wasn't in INSTALLED_APPS list. 
2. Attribute of 'password' and 'password2' field from RegisterSerializer class changed from read_only=False to write_only=True
3. Wrong logic in validation error check from RegisterSerializer class. It's not necessary actually. 


Super User Credentials:
```
UserName: su
Email: su@gmail.com
Password: su
```

# System Description and Use Cases(Implemented):

## Authentication

1. User can login both using email and username. 
   - **Request**
    ```
   URL: localhost:8000/api/v1/auth/token/
   Method: POST
   Payload:
    {
        "username": "su",
        "password": "su",
    }
    ```
   OR
    ```
   Payload: 
    {
        "email": "su@gmail.com",
        "password": "su",
    }
    ```
   - **Response:**
   ```
   Status Code: 200
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjcxMTU4NiwianRpIjoiMWFhOWQyMjQ0MTcxNGM2NGI2YjhkNDE3NDRjYmUyNmMiLCJ1c2VyX2lkIjoxfQ.hkLJsAO57GIZDpryKwtURSVZhVDxe6enT0UzBv-6xp8",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NjI1NDg2LCJqdGkiOiIyZWIxZmZjMWE1MmU0Y2Q3YjdkNzU2ZjNjYjE3ODk2NiIsInVzZXJfaWQiOjF9.MOzZkedKK0FFZTy39QkQNN-SsgMZ7neY0kuEVbdkggU"
    }
    
    ```

    - 
2. Only Admin User can register new User.

   - **Request**
   ```
   URL: localhost:8000/api/v1/auth/register/
   Method: POST
   Payload:
    {
        "first_name":"test",
        "last_name":"test",
        "username":"test",
        "password":"Test!1234",
        "password2":"Test!1234",
        "email":"test@gmail.com"
    }
    ```
   - **Response***
   ```
   Status Code: 201
    {
    "username": "test",
    "email": "test@gmail.com",
    "first_name": "test",
    "last_name": "test"
    }

    ```
3. User can refresh and generate and new access token 
***Request***
```
   URL: localhost:8000/api/v1/auth/token/refresh/
   Method: POST
   Payload:
   {
       "refresh": {{Existing Refresh Token}}
   }

```
***Response***
```
   Status Code: 200
   {
       "access": {{Generated Access Token}}
   }
```


## Movies

1. User can create movie

- **Request**
```
   URL: localhost:8000/api/v1/movies/
   Method: POST
   PayLoad: 
   {
       "title": "Interstellar 2",
       "genre": "Sci-fi/Adventuree",
       "year": 2014
   }
```

- **Response**
```
   Status Code: 201
   {
       "id": 4,
       "title": "Interstellar 3",
       "genre": "Sci-fi/Adventuree",
       "year": 2014,
       "creator": "su",
       "avg_rating": null
   }
```

2. User can see movies list 

- **Request**
```
   URL: localhost:8000/api/v1/movies/ 
   Method: GET
   Payload: Null
```
- **Response**
```
   Status Code: 200
   [
       {
           "id": 4,
           "title": "Interstellar 3",
           "genre": "Sci-fi/Adventuree",
           "year": 2014,
           "creator": "su",
           "avg_rating": null
       },
       {
           "id": 3,
           "title": "Interstellar 2",
           "genre": "Sci-fi/Adventuree",
           "year": 2014,
           "creator": "su",
           "avg_rating": null
       },
       {
           "id": 2,
           "title": "Interstellar",
           "genre": "Sci-fi/Adventuree",
           "year": 2014,
           "creator": "mahin",
           "avg_rating": 2.25
       },
       {
           "id": 1,
           "title": "Inceptionn",
           "genre": "Action/Sci-fi",
           "year": 2010,
           "creator": "mahin",
           "avg_rating": 8.8
       }
   ]
```


3. User can see movie details that contains avg_rating and creator:

- **Request**
```
   URL: localhost:8000/api/v1/movies/2
   Method: GET
   Payload: Null
```
- **Response**
```
   Status Code: 200
   {
       "id": 2,
       "title": "Interstellar",
       "genre": "Sci-fi/Adventuree",
       "year": 2014,
       "creator": "mahin",
       "avg_rating": 2.25
   }
```

5.Only Admin User can create review list

- **Request**
```
   URL: localhost:8000/api/v1/movies/review/
   Method: POST
   Payload: 
   {
       "movie": 1,
       "score": 4
   }
```
- **Response**
```

   - If Rating is not valid:
   Status Code: 400
   [
       "Rating range is 1-5 inclusive"
   ]
   
   - If already rating provided by same user:
   Status Code: 400
   [
       "You have already rated this movie"
   ]
   
   Status Code: 201

   {
       "id": 22,
       "movie": 1,
       "score": 3,
       "reviewer": "su"
   }
```

6. Only Admin User can see review list

- **Request**
```
   URL: localhost:8000/api/v1/movies/review/
   Method: GET
   Payload: Null

```
- **Response**
```
   Status Code: 200
   [
       {
           "id": 15,
           "movie": 2,
           "score": 1,
           "reviewer": "mahin11"
       },
       {
           "id": 16,
           "movie": 2,
           "score": 2,
           "reviewer": "mahin"
       },
       {
           "id": 17,
           "movie": 2,
           "score": 5,
           "reviewer": "mahin1"
       },
       {
           "id": 21,
           "movie": 2,
           "score": 1,
           "reviewer": "su"
       }
   ]

```







# All Bug List and Solution

# User Authentication

## No-1: Run Time Error 
```
RuntimeError: Model class movies.models.Movie doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.

```
### No-1: Solution  
```
- add movies in `INSTALLED_APPS` in settings.py file

  INSTALLED_APPS = [
    '...'

    'movies',
  ]
```
#

## No-2: Run Time Error 
```
In movie.avg_rating in not Found. Makemigration Need. In reReview
```

### No-2: Solution  

```
- python manage.py makemigrations
- python manage.py migrate
```
#

## No-3: API Error 

This API in existing code - `/auth/token/`, login with email only.


### No-3: Solution  

- Solution Add in `authentication/views.py` in : `LoginViewSet` class

#

## No-4: API Error 

This API in existing code - `/auth/register/`, When Input All The Correct Information...
```
{
  "password": [
    "Password fields didn't match."
  ]
}
```


### No-4: Solution  

- Solution Add in `authentication/views.py` in : `RegisterView` class with Proper Error Message.

#
## No-5: Extra API Ready  

- API Ready for Get Authenticated User Info- `/auth/user_details/`, in `UserProfileViewSet` class.

#
# Movie

## No-6: Extra Respone Add API  

- Extra Creator information Pass in `MovieSerializer` class,  for Get Authenticated Creator Info in - `/movies/` API.

#
## No-7: Error Movie Update API  

- Movie can only be updated by its creator. And Also Check Other Authentication in  `RetrieveUpdateDestroyMovieAPIView` class, in - `/movies/{id}/` API.
#
## No-8: Extra Respone Add API  

- Proper Error and Success message pass after delete movie in `RetrieveUpdateDestroyMovieAPIView` class, by - `/movies/{id}/` API with `delete` Function
#
# Rating

## No-9: API Error

- This API in existing code - `/movies/review/`, When Input All The Correct Information. This error is Show

```
{
  "detail": "Method \"POST\" not allowed."
}
```
### No-9: API Solve

- Change the Url Name in - `/movies/` to `/review/rating/` API.  and also add `delete` Method

#

## No-10: API Error

- Any Authenticate User Can Update Rating. This API in existing code - `/movies/review/{id}/`

### No-10: API Solve

- And Modify the Update fuction for rating update by Only Rating Owner

#
# Report

## No-11: Model 

- -  `Report` Model is Ready in  `movies/model.py`

## Extra API List
- `Get : /movies/movie/report/`
- `Post :  /movies/movie/report/`
- `Get: /movies/movie/report/{id}/`
- `Patch: /movies/movie/report/{id}/`
- `Delete: /movies/movie/report/{id}/`


#
# Extar Work

## No-12: For API List 

- I am Usign Swagger For API Documentation
```
http://127.0.0.1:8000/

```
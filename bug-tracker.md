### Bug Report

This document contains the list of bugs that were present in the initial version of the application along with the cause of the individual bug. I have also summarized how I addressed these bugs to resolve them so that the API can become fully functioning.

#### Bug#1

In `api_crud/settings.py`, there is a config variable called *INSTALLED_APPS* which contains the names of each application used in the API. The `movie` app was not included in this list which would not allow anything implemented in that app to be part of the API (migrations will not take place, endpoints will not show on documentation, admin site will not contain the tables).

* **Solution**: Adding the `"movies"` at the end of the *INSTALLED_APPS* list will resolve the issue.

#### Bug#2

In `authentication/views.py`, register route should be open to everyone, but it is restricted with the permission class `IsAdminUser` which makes it usable only by an admin user when logged in.

* **Solution**: Replacing the *IsAdminUser* with `AllowAny` will make the endpoint public and resolve the issue.

#### Bug#3

In `authentication/serializers.py`, the `RegisterSerializer` class has a field called `password2` which is not a model field in the `User` model or a database table column, making it unreadable from the backends.

* **Solution**: Removing `read_only=False` and replacing it with `write_only=True` ignores this field from being read and resolves the error.

#### Bug#4

In `authentication/serializers.py`, the `RegisterSerializer` class has a method called `validate` which checks if `password` and `password2` contains the same string, but the method raises `ValidationError` on both equality and inequality of the strings which leads to not being able to sign up.

* **Solution**: Removing or commenting out the 1st if statement that checks for equality will resolve this bug.

#### Bug#5

In `movies/admin.py`, the `Rating` and `Report` model classes are not registered to the admin site which leads to not showing the corresponding tables on the admin site.

* **Solution**: Register these model classes on the admin site.

#### Bug#6

In `movies/filters.py`, the `year__gt` and `year__lt` fields does not have a `lookup_expr` assigned, so the filters fall back to the default equality check.

* **Solution**: adding the corresponding `lookup_expr` for these fields will allow filtering based on *greater than* (for `year__gt` with `lookup_expr="gt"`) or *less than* (for `year__lt` with `lookup_expr="lt"`) respectively.

#### Bug#7

In `movies/models.py`, the `Rating` model has a field called `reviewer` which raises error because of the `.creator` attribute access in the `IsOwnerOrReadOnly` permission class from `movies/permissions.py`.

* **Solution**: Renaming this field name to `creator` will solve the issue, corresponding changes need to be made in the `ReviewSerializer` class in `movies/serializers.py` and the `ListCreateReviewAPIView` class in `movies/views.py` where ORM filter method is being used with `reviewer` attribute.

#### Bug#8

In `movies/models.py`, the `Rating` model has a field called `score` does not have necessary constraints in place to verify that the value is within 1 to 5.

* **Solution**: Adding `MinValueValidator` and `MaxValueValidator` instances with 1 and 5 as the attributes respectively will resolve the issue.

#### Bug#9

In `movies/serializers.py`, the `username` source in the `creator` field from `MovieSerializer` class does not exist in the `Movie` model as a direct attribute, but rather it is a nested attribute for the `creator` attribute which is a foreign key referencing the `auth.User` model which has the `username` attribute.

* **Solution**: Replacing `source="username"` with `source="creator.username"` will trace the right data and resolve the issue.

#### Bug#10

In `movies/views.py`, the `permission_classes` set in the `RetrieveUpdateDestroyMovieAPIView` class allows any authenticated user to update a movie information, but it should only be allowed for the user who created that movie record.

* **Solution**: Replacing `IsAuthenticated` with `IsOwnerOrReadOnly` will implement the intended access control and resolve the bug.

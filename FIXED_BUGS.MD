# NUMBER OF BUGS THAT HAS BEEN SOLVED

1. Model class movies.models.Movie doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.

   - Added the app name to the INSTALLED_APPS list.

   ```python
   INSTALLED_APPS = [
   	.....
       'movies',
   ]
   ```

1. Removed the condition from `RegisterSerializer` that restricts user registration event after similar password (password, password2) is provided:

   ```python
   if attrs['password'] == attrs['password2']:
               raise serializers.ValidationError({"password": "Password fields didn't match."})
   ```

1. `RegisterSerializer`'s password and password2 fields were set to `read_only=True`.

   ```python
   password = serializers.CharField(
           write_only=True, required=True, validators=[validate_password],
           style={'input_type': 'password', 'placeholder': 'Password'}
       )
   password2 = serializers.CharField(
           write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
       )
   ```

1. Missing column `avg_rating` Bug fixed for `Movies` model by generating new migrations.
1. Movie Retrieve and Update API permission was changed to `IsOwnerOrReadOnly` in order to ensure updating user is the owner of the movie.
1. Dynamic URL for movie retrieve object moved to the bottom or the URL list on `movie.urls.py`
1. Dynamic routes brought down to the list to avoid auto redirection
1. Default value given to movie's avg_rating since every move will have a score.
1. Validator added for rating score validation
1. On rating creation or updating movie's avg_rating filed will be re-calculated
1. Serializer’s `source=username` fixed to `source=creator.username`.
1. MovieSerializer’s missing avg_rating field was added to the serializer

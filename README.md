# Lanking Backend API
> Django API app that stores database models of users, landlords, ratings, and properties and allows them to be created and queried through API endpoints.

This app uses Django Rest Framework and TokenAuthentication, with help from the following [tutorial](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5).

![](header.png)

## Get Started

Make sure to download Django and Django Rest Framework:
```sh
pip install django
```
```sh
pip install djangorestframework
```

You can clone the project and create a file called settings.py in the lanking_api/ folder, which should be the same as the example settings.py file in the folder, but include a [secret key](https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key) and the [proper database settings](https://docs.djangoproject.com/en/2.2/ref/settings/#databases). Personally I used MAMP so that I could use MySQL for this project. 

## API Endpoints

The implemented API endpoints are the following:

| HTTP METHOD  | POST            | GET       | 
| ------------ | --------------- | --------- | 
| CRUD OP      | CREATE          | READ      | 
| /user        | Create new user | N/A       | 
| /user/login  | Login user, return token | N/A  | 
| /user/ratings?id=### | N/A         | Return ratings that user ### wrote | 
| /landlord    | Create new landlord | Query landlord with first and last url query parameters | 
| /landlord/id/?id=###&get_ratings   | N/A  | Return ratings of landlord with id ### | 
| /landlord/id/?id=###&get_properties| N/A  | Return properties of landlord with id ### | 
| /rating      | Create new rating   | N/A   | 
| /property    | Create new property | Query property with address, state, city, zip url query parameters |  
| /property/id/?id=### | N/A         | Return landlord of property with id ###   | 

For the rating endpoint, you must include an Authentication HTTP header formatted as:
```sh
Authentication: Token -authtoken-
```
where -authtoken- should be replaced with an authentication token that you can get through the login endpoint.

## Tests

Run the tests by executing the following command:

```sh
python manage.py test
```



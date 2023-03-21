# Reliving the Life

The system consists of 2 phases, detection of any dizziness, anxiety by observing the physical movement of the person. And then if something severe turns out, stopping the vehicle in time and informing the concerned authorities (hospitals, police - if accident happens - etc.).


### Why Django?
1. Django actually takes the concept ideas from just concepts to concrete ideas in a matter of hours.
2. It saves much of our hassle of development.

### Deploying the code on a web-based API using Django
The following steps can be taken to create a web-based API within a couple of hours (at most):
1. Create a new Django project using the 'django-admin' command.
2. Create a new Django app, typically named after the api (eg. faint_api).
3. Open the 'setting.py' in your project directory and add this app into the 'INSTALLED APPS' list. The one that contains some preinstalled apps.
4. Create a new file called 'urls.py' inside 'faint_api' app directory, and add the required code to it.
5. Create another file 'views.py' inside 'faint_api' and add the required code to it.
6. Run the development server using 'python manage.py runserver' command and test the API by sending POST requests to the following URLs:
 a. http://localhost:8000/faint_detection
 b. http://localhost:8000/get_location
 c. http://localhost:8000/nearby_places
A tool similar to Postman can be used to handle the requests and see the JSON responses.

Here you have the very basic idea of how to create the API.
For more references, you may click here: https://www.geeksforgeeks.org/how-to-create-a-basic-api-using-django-rest-framework/

As and when the need to change/delete/update the code arises, it will be taken care of via Open Source Contributions. We would love to hear all the suggestions from you. Please make a fork of this branch and experiment with it individually.

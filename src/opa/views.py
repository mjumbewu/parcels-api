from django.http import HttpResponse
import requests

def opa_proxy(request, path):
    response = requests.get('http://api.phillyaddress.com/' + path)
    
    django_response = HttpResponse(
        response.content, 
        content_type=response.headers['content-type'],
        status=response.status_code)
    
    # Enable CORS
    django_response['Access-Control-Allow-Origin'] = '*'
    
    return django_response

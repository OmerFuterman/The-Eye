from django.http.response import HttpResponseBadRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import event
from django.core import serializers
import json
import datetime

@csrf_exempt
def add_info(request):
        # If wrong method used, send back 400 error
        if request.method != 'POST':
            return HttpResponseBadRequest('Error: incorrect method, please use POST')

        # Process payload
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        # Check for valid payload information
        payloadCheck = payloadChecker(payload)
        if payloadCheck:
            return payloadCheck

        # Create event from payload
        t = event(
            session_id=payload.get('session_id'),
            category=payload.get('category'), 
            name=payload.get('name'), 
            meta_data=payload.get('data'), 
            timestamp=payload.get('timestamp')
        )

        # Save to db
        t.save()

        return HttpResponse('Success: added record to database')

@csrf_exempt
def db_query(request):
    # If wrong method used, send back 400 error
    if request.method != 'GET':
        return HttpResponseBadRequest('Error: incorrect method, please use GET')

    # Serialize db info into python
    object_list = serializers.serialize('python', event.objects.all())

    # Create object and add items from db into it
    res={}
    for object in object_list:
        temp={}
        for field_name, field_value in object['fields'].items():
            if isinstance(field_value, datetime.date):
                date = field_value
                date = date.strftime('%m:%d:%Y')
                temp[field_name]=date
            else:
                temp[field_name]=field_value
        res[object['fields']['session_id']]=temp

    # Make res object into json and return
    return HttpResponse(json.dumps(res))

    

def payloadChecker(payload):
    # Payload information checks
    if not payload.get('session_id'):
        return HttpResponseBadRequest('Error: No session id specified in payload')
    if type(payload.get('session_id')) is not str:
        return HttpResponseBadRequest('Error: Wrong value type for session id')
    if not payload.get('category'):
        return HttpResponseBadRequest('Error: No category specified in payload')
    if type(payload.get('category')) is not str:
        return HttpResponseBadRequest('Error: Wrong value type for category')
    if not payload.get('name'):
        return HttpResponseBadRequest('Error: No name specified in payload')
    if type(payload.get('name')) is not str:
        return HttpResponseBadRequest('Error: Wrong value type for name')
    if not payload.get('data'):
        return HttpResponseBadRequest('Error: No data specified in payload')
    if not payload.get('timestamp'):
        return HttpResponseBadRequest('Error: No timestamp specified in payload')
    if type(payload.get('timestamp')) is not str:
        return HttpResponseBadRequest('Error: Wrong value type for timestamp')

    return False
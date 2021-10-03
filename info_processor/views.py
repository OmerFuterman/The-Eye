from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import event
from django.core import serializers
import json

@csrf_exempt
def add_info(request):
        # If wrong method used, send back 400 error
        if request.method != 'POST':
            return HttpResponseBadRequest('Error: incorrect method')

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


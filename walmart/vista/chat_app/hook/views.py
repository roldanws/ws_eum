from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.generic import View
from braces.views import CsrfExemptMixin
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from chat_app import consumers
class ProcessHookView(CsrfExemptMixin, View):
    

    #@method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        #print("cicle")
        #print( request.body))
        conv = request.body.decode('utf-8').replace('\0', '')
        #print(json.loads(conv))
        message = json.loads(conv)
        #message = "{'nombre': 'rodrigo', 'mensaje': 'que hubo'}"
        message = str(message).replace("'",'"')
        #print(message)
        #message = '{"nombre":"r","mensaje":"xyz"}'
        #consumers.ws_add(message)
        consumers.ws_message(message)

        '''string = request.read().decode('utf-8')
        json_obj = json.loads(string)
        print(string) # prints the string with 'source_name' key'''
        #print(json.loads(request.read().decode(request.body)))
        
        '''
        if 'json' in request.headers.get('Content-Type'):
            js =request.json()
        else:
            print('Response content is not in JSON format.',request.headers.get('Content-Type'))
            js = 'spam'
        '''
        if "esta" in message:
            return HttpResponse('{"status":"ok"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failed"}', content_type='application/json')
# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets, views, generics
from .models import Superfrog, Admin, Customer, Event, Appearance, Superfrog, SuperfrogAppearance, User
from .serializers import SuperfrogSerializer, AdminSerializer, CustomerSerializer, EventSerializer, AppearanceSerializer,AppearanceShortSerializer,CustomerAppearanceSerializer, SuperfrogAppearanceSerializer
from rest_framework import viewsets, views, generics, status
from .models import Superfrog, Admin, Customer, Event, Appearance
from .serializers import SuperfrogSerializer, AdminSerializer, CustomerSerializer, EventSerializer, AppearanceSerializer,AppearanceShortSerializer, UserSerializer, SuperfrogLandingSerializer,PayrollSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action, list_route
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from datetimerange import DateTimeRange
from collections import defaultdict, OrderedDict
from django.contrib.auth import authenticate, login
import pdfrw
import os
from django.template.loader import render_to_string, get_template
import datetime
from time import strftime
import json

# class AppearanceViewSet(viewsets.ViewSet):
#     queryset = Appearance.objects.all()
#     serializer_class = AppearanceSerializer

#     def list(self,request, *args, **kwargs ):
#         appearances = Appearance.objects.all()
#         serializer = AppearanceShortSerializer(appearances, many=True)
#         return Response(serializer.data)

#     @list_route(methods=['get'])
#     def list_by_status(self, request, status_id):
#         appearances = queryset.filter(status=status_id)
#         serializer = AppearanceShortSerializer(appearances, many=True)
#         return Response(serializer.data)

#     serializer = AppearanceShortSerializer

INVOICE_TEMPLATE_PATH = 'Honorarium_Request_Final.pdf'
#INVOICE_OUTPUT_PATH = 'fillform.pdf'

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY='/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_kEY='/Widget'

def write_fillable_pdf(input_pdf_path,output_pdf_path,data_dict):
    template_pdf=pdfrw.PdfReader(input_pdf_path)
    annotations=template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY]==WIDGET_SUBTYPE_kEY:
            if(annotation[ANNOT_FIELD_KEY]):
                print(annotation[ANNOT_FIELD_KEY])
                key=annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )

    pdfrw.PdfWriter().write(output_pdf_path,template_pdf)
@csrf_exempt 
def generatePayroll(request, SFAid = None, adminID = None):
    if request.method == 'PATCH':
        admin_id = Admin.objects.get(pk = adminID)
        print(admin_id)
        superfrog_appearance = SuperfrogAppearance.objects.get(pk = SFAid)
        print(superfrog_appearance)
        INVOICE_OUTPUT_PATH = superfrog_appearance.appearance.name + '.pdf'
        a = superfrog_appearance.appearance.start_time
        b = superfrog_appearance.appearance.end_time
        dates = superfrog_appearance.appearance.date
        datesS = dates.strftime('%Y/%m/%d')
        aT = a.strftime('%I:%M')
        bT = b.strftime('%I:%M')
        deltaA = datetime.timedelta(hours=a.hour, minutes = a.minute)
        deltaB = datetime.timedelta(hours=b.hour, minutes= b.minute)
        dA = deltaA
        dB = deltaB
        delta = dB - dA
        deltaSec = delta.total_seconds()
        deltaHour = deltaSec / 3600
        mile = superfrog_appearance.appearance.mileage
        amount = deltaHour* 25 + mile * .5
        data_dict = {
            'Name' : superfrog_appearance.superfrog.user.first_name + superfrog_appearance.superfrog.user.last_name,
            'Permanentaddress 2' : superfrog_appearance.superfrog.street+ ' ' + superfrog_appearance.superfrog.city+ ' ' + superfrog_appearance.superfrog.state+ ' ' + superfrog_appearance.superfrog.zipCode,
            '1 Attach a copy of written agreement or explain the nature and DATE OF SERVICES performed 1' : 'Appearance Name: '+superfrog_appearance.appearance.name + ', ' + 'Appearance Date: '+datesS + ', ' + 'Appearance Location '+superfrog_appearance.appearance.location+ ', ' + 'Appearance Time: '+aT + '-' + bT,
            'Amount' : amount,
            '3g' : admin_id.user.first_name + ' ' + admin_id.user.last_name
        }
        print(data_dict)
        write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict)
        
        superfrog_appearance.appearance.status = "Completed"
        superfrog_appearance.appearance.save()
        return HttpResponse(superfrog_appearance, status= 201)

# def pdf_view(request):
#     with open('/path/to/my/file.pdf', 'r') as pdf:
#         response = HttpResponse(pdf.read(), mimetype='application/pdf')
#         response['Content-Disposition'] = 'inline;filename=some_file.pdf'
#         return response
#     pdf.closed

# def home(request):
# image_data = open(“/path/to/my/image.pdf”, “rb”).read()
# return HttpResponse(image_data, mimetype=”application/pdf”)

def list_by_status(request, status=None):
    if request.method == 'GET':
        print('we did it')
        queryset = Appearance.objects.filter(status=status)
        serializer = AppearanceShortSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()
def list_by_status_superfrog(request, status=None, sId= None):
    if request.method == 'GET':
        queryset = SuperfrogAppearance.objects.filter(superfrog = sId , appearance__status = status)
        serializer = SuperfrogLandingSerializer(queryset, many = True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()

def list_SuperfrogAppearance_by_Status(request, status=None):
    if request.method == 'GET':
        print('we did it')
        queryset = SuperfrogAppearance.objects.filter(appearance__status=status)
        serializer = SuperfrogAppearanceSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()

def Appearance_to_Change(request, AID):
    if request.method == 'GET':
        queryset = SuperfrogAppearance.objects.get(pk=AID )
        serializer = SuperfrogAppearanceSerializer(queryset, many=False)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()
#def addEmployee(request):
#    if request.method == 'POST:
#        user = User.objects.create_user('') 

def getEmployee(request):
    if request.method == 'GET':
        queryset = Superfrog.objects.all()
        serializer = SuperfrogSerializer(queryset, many= True)
        return HttpResponse(JSONRenderer().render(serializer.data))
@csrf_exempt
def appearances(request):
    print('hi')
    if request.method == 'GET':
        queryset = Appearance.objects.all()
        serializer = AppearanceShortSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    #save information from form into appearance request
    elif request.method=='POST':
        data = json.loads(request.body)
        print(data)
        appearance_serializer = AppearanceSerializer(data=data['appearance'])
        if appearance_serializer.is_valid():
            appearance = appearance_serializer.save()
            appearance_serializer = AppearanceSerializer(appearance)
            print(appearance_serializer.data)
            
            
        else:
            print(appearance_serializer.errors)
            return HttpResponse(appearance_serializer.errors, status = 400)
                
        customer_serializer = CustomerSerializer(data=data['customer'])
        #after adding customer to db, send confirmation email to customer confirming contact information and event information.
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            customer.save()
            appearance.customer = customer
            appearance.save()
            html_message = render_to_string(
                'customer_confirmation.html',
                {
                    'first_name': customer.first_name,
                    'last_name':  customer.last_name,
                    'phone': customer.phone,
                    'email': customer.email,
                    'organization': appearance.organization,
                    'location': appearance.location,
                    'description': appearance.description,
                    'status': appearance.status,
                    'special_instructions': appearance.special_instructions,
                    'expenses_and_benefits': appearance.expenses_and_benefits,
                    'cheerleaders': appearance.cheerleaders,
                    'showgirls': appearance.showgirls, 
                    'parking_info': appearance.parking_info,
                    'outside_orgs': appearance.outside_orgs,
                    'performance_required': appearance.performance_required,
                }
            )
            send_mail('Event request confirmation',
            'Thanks for requesting a Superfrog appearance! Here is a confirmation message for the event request: \n' +
             '\n' + 'Customer Contact Information \n' + 
             'Customer Name: ' + customer.first_name + 
             ' ' + customer.last_name + '\n' + 
             'Phone Number: ' + str(customer.phone) + 
             '\n' + 'Customer email: ' + customer.email + 
             '\n' + ' \n' + 'Appearance Information \n' + 
             'Organization requesting event: ' + appearance.organization + '\n' + 
             'Location: ' + appearance.location + '\n' + 
             'Description: ' + appearance.description + '\n' + 
             'Status: ' + appearance.status + '\n' +
             'Special Instructions: ' + appearance.special_instructions +  '\n' + 
             'Expenses and Benefits: ' + appearance.expenses_and_benefits + '\n' +
             'Cheerleaders: ' + appearance.cheerleaders + ' Showgirls: ' + appearance.showgirls + '\n' + '\n' +
             'Our team will review your request within the next two weeks. You will receive an email updating you on our decision when it is made. Thanks and Go Frogs!' ,
             'superfrog@scheduler.com',
             [customer.email],
             fail_silently = False,
             html_message = html_message)
        else:
            print(customer_serializer.errors)
            return HttpResponse(appearance_serializer.errors, status = 400)
        appearance_serializer = AppearanceSerializer(appearance)
        return HttpResponse(status = 200)
    else:
        return HttpResponseBadRequest()

def detail(request, id=None):
    if request.method == 'GET':
        queryset = Appearance.objects.get(pk=id)
        serializer = CustomerAppearanceSerializer(queryset, many=False)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()
def payroll_appearance(request,status=None):
    if request.method == 'GET': 
        queryset = SuperfrogAppearance.objects.filter( appearance__status=status)
        serializer = PayrollSerializer(queryset, many = True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()

def payroll_detail(request, id=None):
    if request.method == 'GET':
        queryset = SuperfrogAppearance.objects.get(pk=id)
        serializer = PayrollSerializer(queryset, many=False)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()

def superfrog_appearance_detail(request, id=None):
    if request.method == 'GET':
        queryset = SuperfrogAppearance.objects.get(pk=id)
        serializer = SuperfrogAppearanceSerializer(queryset, many=False)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()
def create(request):
    if request.method=='POST':
        data = JSONParser().parse(request.body)
        serializer = AppearanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status = 201)
        return HttpResponse(serializer.errors, status = 400)
    else:
        return HttpResponseBadRequest()
@csrf_exempt
def update_appearance(request):
    if request.method=='PATCH':
        data = json.loads(request.body)
        print(data)
        appearance_serializer = AppearanceShortSerializer(data=data['appearance'])
        if appearance_serializer.is_valid():
            appearance_serializer.save()
        return HttpResponse(status= 200)
    else:
        print(appearance_serializer.errors)
        return HttpResponse(appearance_serializer.errors, status = 400)
@csrf_exempt
def signUp(request, id=None, sId = None):
    if request.method=='PATCH':
        appearance_id = Appearance.objects.get(pk=id)
        superfrog_id = Superfrog.objects.get(user_id = sId)
        superfrog_appearance = SuperfrogAppearance(superfrog=superfrog_id, appearance=appearance_id)
        superfrog_appearance.save()
        appearance_id.status = "Assigned"
        appearance_id.save()
        #superfrog email confirming sign up
        superfrog_message = render_to_string(
                'superfrog_confirmation.html',
                {
                    'first_name': appearance_id.customer.first_name,
                    'last_name':  appearance_id.customer.last_name,
                    'phone': appearance_id.customer.phone,
                    'email': appearance_id.customer.email,
                    'organization': appearance_id.organization,
                    'location': appearance_id.location,
                    'description': appearance_id.description,
                    'status': appearance_id.status,
                    'special_instructions': appearance_id.special_instructions,
                    'expenses_and_benefits': appearance_id.expenses_and_benefits,
                    'cheerleaders': appearance_id.cheerleaders,
                    'showgirls': appearance_id.showgirls, 
                    'parking_info': appearance_id.parking_info,
                    'outside_orgs': appearance_id.outside_orgs,
                    'performance_required': appearance_id.performance_required,
                }
            )
        #customer email confirming appearance
        customer_message = render_to_string(
                'appearance_confirmation.html',
                {
                    'first_name': appearance_id.customer.first_name,
                    'last_name':  appearance_id.customer.last_name,
                    'phone': appearance_id.customer.phone,
                    'email': appearance_id.customer.email,
                    'organization': appearance_id.organization,
                    'location': appearance_id.location,
                    'description': appearance_id.description,
                    'status': appearance_id.status,
                    'special_instructions': appearance_id.special_instructions,
                    'expenses_and_benefits': appearance_id.expenses_and_benefits,
                    'cheerleaders': appearance_id.cheerleaders,
                    'showgirls': appearance_id.showgirls, 
                    'parking_info': appearance_id.parking_info,
                    'outside_orgs': appearance_id.outside_orgs,
                    'performance_required': appearance_id.performance_required,
                }
            )
        #admin email
        send_mail('Appearance Confirmation','You are scheduled to appear at an event! Here is the appearance info: \n' + 
         '\n' + 'Customer Contact Information \n' 
        + 'Customer Name: ' 
        + appearance_id.customer.first_name 
        + ' ' + appearance_id.customer.last_name 
        + '\n' + 'Phone Number: ' 
        + str(appearance_id.customer.phone) 
        + '\n' + 'Customer email: ' 
        + appearance_id.customer.email 
        + '\n' + ' \n' + 'Appearance Information \n' 
        + 'Organization requesting event: ' + appearance_id.organization 
        + '\n' + 'Location: ' + appearance_id.location +
        '\n' + 'Description: ' + appearance_id.description 
        + '\n' + 'Status: ' + appearance_id.status + '\n' + '\n' + 'Thanks and Go Frogs!' 
        ,'superfrog@scheduler.com',
        [User.objects.get(pk=sId).email],
        fail_silently = False,
        html_message = superfrog_message)
        #
        send_mail('Superfrog Appearance Confirmation',
        'Your event has been accepted- and Superfrog will be there! Here is the appearance info confirmation: \n' +
        '\n' + 'Customer Contact Information \n' +
        'Customer Name: ' + appearance_id.customer.first_name +
        ' ' + appearance_id.customer.last_name + '\n' +
        'Phone Number: ' + str(appearance_id.customer.phone) +
        '\n' + 'Customer email: ' + appearance_id.customer.email +
        '\n' + ' \n' + 'Appearance Information \n' +
        'Organization requesting event: ' + appearance_id.organization +
        '\n' + 'Location: ' + appearance_id.location + '\n' +
        'Description: ' + appearance_id.description + '\n' + 'Status: ' +
        appearance_id.status + '\n' + '\n' + 'Thanks and Go Frogs!' ,
        'superfrog@scheduler.com',
        [appearance_id.customer.email],
        fail_silently = False,
        html_message = customer_message)
        return HttpResponse(superfrog_appearance, status= 201)

@csrf_exempt
def acceptAppearance(request, id=None):
    if request.method=='PATCH':
        appearance_id = Appearance.objects.get(pk=id)
        appearance_id.status = "Accepted"
        appearance_id.save()
        #superfrog email
        return HttpResponse( status=201)

@csrf_exempt
def rejectAppearance(request, id = None):
    if request.method=='DELETE':
        appearance_id = Appearance.objects.get(pk=id)
        appearance_id.delete()
        #customer email
        return HttpResponse(status = 201)

def events(request):
    if request.method == 'GET':
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        print(serializer.data)
        print(type(serializer.data))
        return HttpResponse(JSONRenderer().render(serializer.data))    

def toDateRange(date, start, end):
    startstr = str(date)+"T"+str(start)
    endstr = str(date)+"T"+str(end)
    return DateTimeRange(startstr,endstr)

def events_customer_monthly(request, year, month):
    events = defaultdict(list)
    queryset = Event.objects.filter(date__year = year, date__month = month).order_by('date', 'start_time', 'end_time')
    for event in queryset:
        dtr = toDateRange(event.date, event.start_time, event.end_time)
        if not events[event.date]:
            events[event.date].append(dtr)
        else:
            inserted = False
            for i in range(len(events[event.date])):
                e =  events[event.date][i]
                if e.is_intersection(dtr):
                    events[event.date][i] = e.encompass(dtr)
                    inserted = True
                    break
            if not inserted:
                events[event.date].append(dtr)
    response = []
    for day in events:
        for event in events[day]:
            event.start_time_format = '%H:%M:%S'
            event.end_time_format = '%H:%M:%S'
            response.append(OrderedDict([('start', str(day) + " "+ event.get_start_time_str()), ('end',  str(day) + " "+ event.get_end_time_str()), ('editable', False)]))
    return HttpResponse(JSONRenderer().render(response))


def list_by_status_list(request, status=None, sID=None):
    if request.method == 'GET':
        queryset = SuperfrogAppearance.objects.filter(appearance__status=status, superfrog=sID)
        serializer = SuperfrogAppearanceSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data))
    else:
        return HttpResponseBadRequest()
        
@csrf_exempt
def email(request):
    subject = 'You have submitted an appearance request'
    message = 'We will review your request for a superfrog appearance and get back to you within the next 2 weeks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['allensarahanne@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('/customer-confirmation')

#Login View
class LoginView(views.APIView):
    #override post function
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        #authenticate user
        user = authenticate(email=email, password=password)

        #authenticate() looks for an user in database using email and then verify if the password matches
        if user is not None:
            if user.is_active:
                #login() create a new session for this user
                login(request, user)
                serializer = UserSerializer(user, context={'request': request})
                #return the user information using the serializer in form of a JSON object
                return Response(serializer.data,status=status.HTTP_200_OK)
            else: #inactive user account
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This user has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else: #no matched user 
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

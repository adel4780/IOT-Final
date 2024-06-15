from django.shortcuts import render
from .models import values

def firstPage(request):
    if request.method == 'GET':
        timeOn = request.GET.get('On')
        timeOff = request.GET.get('Off')
        saveValues(request , timeOn , timeOff)
        return render(request , 'GUI.html')
    else:
        return render(request , 'abc.html')

def saveValues(request, timeOn, timeOff):
    if request.method == 'GET':
        count = values.objects.all().count()
        if count != 0:
            v = values.objects.filter(id = 1)
            for i in v:
                status = checkInputs(timeOn , timeOff)
                if status:
                    On = int(timeOn)
                    Off = int(timeOff)
                    i.timeOn = On
                    i.timeOff = Off
                    i.save()
        else:
            On = 500
            Off = 500
            v = values(timeOn = On , timeOff = Off)
            v.save()

def checkInputs(timeOn , timeOff):
    if(timeOn != None and timeOff != None):
        if(timeOn.isnumeric() and timeOff.isnumeric()):
            return True
    return False


def getValues(request):
    v = values.objects.filter(id = 1)
    On = 0
    Off = 0
    for i in v:
        On = i.timeOn
        Off = i.timeOff
    return render(request, 'getValues.html', {"On": On, "Off": Off})

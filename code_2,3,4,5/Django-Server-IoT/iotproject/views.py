from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest

# Global variables for status and scheduling
current_status = 'OFF'
current_time_on = 0
current_time_off = 0

def firstPage(request):
    if request.method == 'GET':
        return render(request, 'GUI.html')
    else:
        return render(request, 'abc.html')

def get_on(request):
    global current_status, current_time_on, current_time_off
    current_status = 'ON'
    current_time_on = 0
    current_time_off = 0
    return JsonResponse({'status': current_status, 'time_on': current_time_on, 'time_off': current_time_off})

def get_off(request):
    global current_status, current_time_on, current_time_off
    current_status = 'OFF'
    current_time_on = 0
    current_time_off = 0
    return JsonResponse({'status': current_status, 'time_on': current_time_on, 'time_off': current_time_off})

def schedule(request):
    global current_time_on, current_time_off, current_status

    # Handle GET request to set time_on and time_off
    if request.method == 'GET':
        try:
            time_on_ms = int(request.GET.get('ON', '0'))
            time_off_ms = int(request.GET.get('OFF', '0'))
            current_time_on = time_on_ms
            current_time_off = time_off_ms
            current_status = 'Blink'
            response_data = {
                'status': current_status,
                'scheduling': {
                    'time_on': current_time_on,
                    'time_off': current_time_off
                }
            }
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            else:
                return render(request, 'GUI.html')
        except ValueError as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid integer values for ON and OFF parameters'}, status=400)
            else:
                return HttpResponseBadRequest('Invalid integer values for ON and OFF parameters')
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def getStatus(request):
    global current_status, current_time_on, current_time_off
    if current_status == 'ON' or current_status == 'OFF':
        time_on = 0
        time_off = 0
    elif current_status == 'Blink':
        time_on = current_time_on
        time_off = current_time_off

    response_data = {
        'status': current_status,
        'scheduling': {
            'time_on': time_on,
            'time_off': time_off
        }
    }
    return JsonResponse(response_data)

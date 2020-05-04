from django.shortcuts import render, redirect
import os
from django.core.wsgi import get_wsgi_application
#from numpy.lib.function_base import vectorize

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
application = get_wsgi_application()
from django.http import HttpResponse
from datetime import datetime
from ble import models
from django.db.models import Q
import json
def get_input(request):
    if request.method == 'POST':
        your_name = request.POST.get('your_name')
        print(your_name)
        return HttpResponse("Hello " + your_name + '!')
    return render(request, "input.html")
def device_list(request):
    list = []
    all_device = models.DevicesGateway.objects.all()
    for d in all_device:
        data = {}
        data["device_id"] = d.device_id
        # data["device_address"] = d.device_address
        data["device_name"]= d.device_name
        # if d.device_name == "00000000-0000-0000-0000-000000000003":
        #     data["device_name"] = "Ibeacon03"
        data["device_description"] = d.device_description
        list.append(data)
    if "btnNew" in request.POST:
        return redirect('newDevice')
    if "btnEdit" in request.POST:
        for d in all_device:
            if request.POST.get('%d' %d.device_id):
                return redirect('editDevice', device_id=d.device_id)
    if "btnDelete" in request.POST:
        pass
    return render(request, "device_list.html", {"list":list})
def device_register(request):
    data = {}
    error = {}
    if request.method == 'POST':
        data["device_address"] = request.POST.get('device_address')
        data["device_name"] = request.POST.get('device_name')
        data["device_description"] = request.POST.get('device_description')
        print(data["device_address"])
        cnt = models.Devices.objects.filter(device_address=data["device_address"]).count()
        if(cnt > 0):
            error["message"] = "This address is already exist!"
        else:
            d = models.Devices(device_address=data["device_address"], 
                                device_name=data["device_name"],
                                device_description=data["device_description"],
                                registration_time=datetime.now())
            d.save()
            return redirect('listDevice')
    return render(request, "device_register.html", error)

def device_edit(request, device_id):
    print(device_id)
    device = models.Devices.objects.get(device_id=device_id)

    data = {}
    data["device_address"] = device.device_address
    data["device_name"] = device.device_name
    data["device_description"] = device.device_description

    if request.method == 'POST':
        data["device_address"] = request.POST.get('device_address')
        data["device_name"] = request.POST.get('device_name')
        data["device_description"] = request.POST.get('device_description')
        device.device_address = data["device_address"]
        device.device_name = data["device_name"]
        device.device_description = data["device_description"]
        device.save()
        return redirect('listDevice')
    return render(request, "device_register.html", {'data':data})

def get_rssi(request):
    loc = 0
    device_id = 0
    arr = {"data":[]}
    a = []
    if request.method == "GET":
        loc = request.GET.get("loc")
        device_id = request.GET.get("device_id")
    data_list = models.Data.objects.filter(device_id=device_id)
    for document in data_list:
        t = document.timestamp
        a = [int(t.year), int(t.month), int(t.day), int(t.hour), int(t.minute), int(t.second), int(document.rssi)]
        arr["data"].append(a)
    return HttpResponse(json.dumps(arr["data"][int(loc):]), content_type='application/json')
def show_rssi(request, device_id):
    all_data = models.Data.objects.all()
    total = 0
    cnt = all_data.count()
    for d in all_data:
        total = total + d.rssi
    avg_rssi = float(total) / cnt
    return render(request, "chart.html", {"device_id":device_id, 'avg_rssi':avg_rssi})
def get_avg_rssi(request):
    all_data = models.Data.objects.all()
    total = 0
    cnt = all_data.count()
    for d in all_data:
        total = total + d.rssi
    avg_rssi = float(total)/cnt
    return HttpResponse(json.dumps({"avg_rssi":avg_rssi}), content_type='application/json')

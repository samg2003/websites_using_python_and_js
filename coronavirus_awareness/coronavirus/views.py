from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
import requests
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse("info"))

def info(request):
    try:
        res = requests.get("https://covid2019-api.herokuapp.com/confirmed")
    except:
        context = {
            "total_cases": "Sorry Api this is using is currently down"
        }
        return render(request, "info/info.html", context = context)
    if res.status_code != 200:
        context = {
            "total_cases": "Apology Data Could not be found"
        }
        return render(request, "info/info.html", context = context)
    data = res.json()
    context = {
        "total_cases": data["confirmed"]
    }
    return render(request, "info/info.html", context = context)

def live(request):
    res = requests.get("https://covid2019-api.herokuapp.com/countries")
    if res.status_code != 200:
        context = {
            "countries": "Apology Data Could not be found",
            "confirmed": "apology Api is currently down wait for 12  minutes",
            "deaths": "apology Api is currently down wait for 12  minutes"
        }
        return render(request, "info/live.html", context = context)
    data = res.json()
    context = {
        "countries" : data["countries"]
    }
    try:
        res = requests.get("https://covid2019-api.herokuapp.com/v2/deaths")
        res0 = requests.get("https://covid2019-api.herokuapp.com/confirmed")
    except:
        context["deaths"] = "apology Api is currently down wait for 12  minutes"
        context["confirmed"] = "apology Api is currently down wait for 12  minutes"
        return render(request, "info/live.html", context = context)
    data = res.json()
    data0 = res0.json()
    context["confirmed"] = data0["confirmed"]
    context["deaths"] = data["data"]
    return render(request, "info/live.html", context = context)

@csrf_exempt
def data(request):
    country = request.POST['country']
    try:
        res = requests.get(f"https://covid2019-api.herokuapp.com/country/{country}")
    except:
        return JsonResponse({"success": False})
    if res.status_code != 200:
          return JsonResponse({"success": False})
    data = res.json()
    if country not in data:
        return JsonResponse({"success": False})
    return JsonResponse({"success": True, "country":country, "confirmed": data[country]["confirmed"], "deaths": data[country]["deaths"], "recovered": data[country]["recovered"],"date":data["dt"]})

def symptoms(request):
    try:
        age = int(request.POST["age"])
        symptoms = request.POST.getlist("symptoms-list")
    except:
        return render(request, "info/symptoms.html")
    if age < 50:
        message1 = "COVID-19 patients of your age group has less than 1% death rate"
    elif age<60:
        message1 = "COVID-19 patients of your age group has 1.3% death rate"
    elif age<70:
        message1 = "COVID-19 patients of your age group has 3.6% death rate"
    elif age<80:
        message1 = "COVID-19 patients of your age group has 8% death rate"
    else:
        message1 = "COVID-19 patients of your age group has more than 14% death rate"
    for i in range(len(symptoms)):
        symptoms[i] = int(symptoms[i])
        if symptoms[i] <0:
            message3 = "You have serious vulnerability against COVID-19 self-isolate as much as possible"

    sum = 0
    for i in symptoms:
        if i >0:
            sum += i
    if sum >60:
        message2 = "Goto doctor right way Its extremely possible that you have COVID-19"
    elif sum > 25:
        message2 = "Goto doctor its highly recommended to have checkup"
    elif sum > 10:
        message2 = "Its no harm to get checkup though chances are slim"
    else:
        message2 = "Its advisable to just quarantine yourself its unlikely for you to have coronavirus"
    try:
        waste = message3 + "j"
    except:
        context  = {
        "message1":message1,
        "message2":message2
        }
        return render(request, "info/symptoms.html", context = context)
    context = {
        "message1":message1,
        "message2":message2,
        "message3":message3
    }
    return render(request, "info/symptoms.html", context = context)

def quiz(request):
    key = ["4","3","1","3","2"]
    score = 0
    context = {
    "answer1":0,
    "answer2":0,
    "answer3":0,
    "answer4":0,
    "answer5":0,
    "score":0,
    }
    try:
        answers = request.POST.getlist("answers")
    except:
        return render(request, "info/quiz.html")
    if request.method != "POST":
        return render(request, "info/quiz.html")

    for i in range(len(answers)):
        if key[i] == answers[i]:
            context[f"answer{i+1}"] = 1
            score += 1
    context["score"] = score

    return render(request, "info/quiz.html", context=context)

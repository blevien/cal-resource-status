from django.shortcuts import render
from schedule.calAPI import EventsAPI
import re
from .models import Calendar, Event, Display, Location
from datetime import datetime, timedelta
from django.db.models import Exists, OuterRef

# Create your views here.
# TODO User Friendly Location Names
# location_regex = "(?<=\-)[A-Z](.*?)(?= \()"

def index(request):
    """View function for home page of site."""

    API = EventsAPI()
    
    calendar = API.get_events()

    base = datetime.today().date()
    date_list = [base + timedelta(days=x) for x in range(5)]

    days = []
    locations = Location.objects.all().order_by('name')

    for date in date_list:
        day_events = {"date": date, "locations": []}
        for location in locations:
            location_events = Event.objects.filter(locations=location,start__year=date.year, start__month=date.month, start__day=date.day)
            #location_string = re.findall(location_regex, location.name)[0]
            if location_events:
                day_events["locations"].append({"name": location, "events": location_events})
        days.append(day_events)
            
    context = {
        "title": calendar["summary"],
        "days": days,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index_cards.html', context=context)
from django.shortcuts import render
from schedule.calAPI import EventsAPI
import re
from .models import Calendar, Event, Display, Location
from datetime import datetime, timedelta
from django.db.models import Exists, OuterRef

# Create your views here.
# TODO User Friendly Location Names
# location_regex = "(?<=\-)[A-Z](.*?)(?= \()"

def index(request, display):
    """View function for home page of site."""

    # Gets events from Google & adds or updates in DB
    API = EventsAPI()
    calendar = Display.objects.get(id=int(display)).calendar
    API.get_events(calendar.summary)

    display = Display.objects.get(id=int(display))
    locations = Location.objects.filter(name__startswith=display.name).order_by('name')

    # Controls how many and which dates to ssend to template
    base = datetime.today().date()
    date_list = [base + timedelta(days=x) for x in range(7)]
    days = []

    for date in date_list:
        day_events = {"date": date, "locations": []}
        for location in locations:
            location_events = Event.objects.filter(locations=location,start__year=date.year, start__month=date.month, start__day=date.day)
            # Remove Occupancy, Building & Floor for display
            cleaned_name = re.sub("[\(\[].*?[\)\]]", "", location.name)
            cleaned_name = re.sub("[A-Z].+-", "", cleaned_name)
            day_events["locations"].append({"name": cleaned_name, "events": location_events})
        days.append(day_events)
            
    context = {
        "title": calendar.summary,
        "days": days,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index_cards2.html', context=context)
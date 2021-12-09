#! /usr/bin/python3

import requests
import re
from datetime import datetime
import json
import pytz
import html

# URL needs to be Google Calendar HTML embed URL.

# To get it, go to your Google Calendar, click on the options menu
# next to the calendar in the sidebar. Choose 'Settings and sharing.'
# Scroll down to 'Integrate calendar' and grab the Embed code HTML.
# Embedded within the 'src' tag will be a URL. This is what you want.

# 1. Change the '/embed?' string to 'htmlembed?'
# 2. Add 'mode=AGENDA' to the end
# 3. Change the string following 'ctz' to be UTC
# 4. Paste the result into the url variable below

# It should look something like:
# https://calendar.google.com/calendar/u/0/htmlembed?src=
# yourdomain.com_ackpthstring3943943949@group.calendar.google.com&
# ctz=UTC&mode=AGENDA

url = ('url-goes-here')

response = requests.get(url)
response.raise_for_status()
theHTML = response.text
theEventsList = [ ]
thePost = 'Upcoming calendar events:\n'

# You'll need to create a slack app and install it in your Slack
# and point it at a particular channel in order to get a
# webhook URL to paste below. For more info, read:
# https://api.slack.com/messaging/webhooks

webhook_url = ('slack-webhook-URL-goes-here')

# This script only parses a single page of the agenda.
# If you want to constrain the script to a single day or three
# days or whatever, you can do it by changing this variable.
# Default is two weeks.

daysToList = 14

# Find every date iteration

theDays = re.findall('<div class="date">([^<]+)</div>\n'
    '(<table class="events">(<tr class="event">'
    '<td class="event-time">([^<]+)</td>\n'
    '<td class="event-eventInfo"><div class="event-summary">'
    '<a class="event-link" href="[^"]+" target="_blank">'
    '<span class="event-summary">([^<]+)</span></a></div></td>'
    '</tr> ?)+)</table>', theHTML)

for item in theDays:

    # cycle through the days

    myDay = item[0]

    # extract each event in a day

    theEvents = re.findall('<tr class="event"><td class="event-time">([^<]+)</td>\n<td class="event-eventInfo"><div class="event-summary"><a class="event-link" href="[^"]+" target="_blank"><span class="event-summary">([^<]+)</span></a></div></td></tr>', item[1])

    # loop through each event in a day; usually there's only one but not always!

    for eventItem in theEvents:

        myDaytime = eventItem[0]
        if ":" not in myDaytime:
            myTimematch = re.search('([0-9]+)(am|pm)', myDaytime)
            myDaytime = myTimematch[1] + ":00" + myTimematch[2]

        # print (myDaytime)

        myDaydate = (myDay + ' ' + myDaytime)

        eventDate = datetime.strptime(myDaydate, '%a %b %d, %Y %I:%M%p')
        eventTitle = html.unescape(eventItem[1])

        currentTime = datetime.utcnow()
        timeDiff =  eventDate - currentTime
        minutesAway = round(timeDiff.total_seconds() / 60)

        thisEvent = list((eventTitle, eventDate))
        theEventsList.append(thisEvent)

        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(eventDate)
        pacific_tzinfo = pytz.timezone("US/Pacific")
        pacific_time = with_timezone.astimezone(pacific_tzinfo)
        pt_string = pacific_time.strftime('%a %b %d at %-I:%M %p PT')
        unixTime = str(round(pacific_time.timestamp()))

        if -60 <= minutesAway <= (daysToList * 1440) :
            thePost = thePost + ('*' + eventTitle + '* - <!date^' +
            unixTime + '^{date_pretty} at {time}|' + pt_string + '>\n')

thePost = thePost + '_(Times in your local time zone unless otherwise stated.)_'
slack_data = {'text': thePost}

response = requests.post(
    webhook_url, data =json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
)

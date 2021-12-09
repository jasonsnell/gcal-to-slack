# Google Calendar to Slack

Jason Snell <jsnell@sixcolors.com>

This Python script takes upcoming items from a Google Calendar and posts them to Slack.

The result looks kind of like this:

<img src="https://www.theincomparable.com/imgs/episodes/incomparabot-ep.jpg" width="600" />

You'll need a Google Calendar HTML embed URL.

To get it, go to your Google Calendar, click on the options menu next to the calendar in the sidebar. 

* Choose 'Settings and sharing.'
* Scroll down to 'Integrate calendar' and grab the Embed code HTML.
* Embedded within the 'src' tag will be a URL. This is what you want.

1. Change the '/embed?' string to 'htmlembed?'
2. Add 'mode=AGENDA' to the end
3. Change the string following 'ctz' to be UTC
4. Paste the result into the url variable below

It should look something like:
`https://calendar.google.com/calendar/u/0/htmlembed?src=yourdomain.com_biglonggarbagestring99@group.calendar.google.com&ctz=UTC&mode=AGENDA`

You'll need to create a Slack app and install it in your Slack and point it at a particular channel in order to get a webhook URL for userin the script.

For more info, read [how to do this from Slack itself](https://api.slack.com/messaging/webhooks)


# GoogleCalendarWeeklyFiller
A program which can fill the gaps in someone's google calendar with randomly chosen events from a list you set. Perfect to be run once a week.

Prerequisites to running:

1. Need to get personalized credentials.json file by following the instructions on the following site: https://developers.google.com/calendar/quickstart/python

2. Install the dependencies with ```pip install -r requirements.txt```


3. Within ```weeklyCalendarFiller.py``` file, set the following parameters to determine the system's behavior:
- EVENTS: The list of possible events you can fill the calendar with
- GAP_HOURS: Set the minimum gap in your calendar that there needs to be to insert an event
- START_HR: First Hour to consider filling in the google calendar system
- END_HR: Last Hour to consider filling in the google calendar system


4. Run the script with ```python3 weeklyCalendarFiller.py``` and check your calendar to see the effects!



### Possible extension
To make this run in a more robust way, putting this script on a pipeline or a cron job can be very helpful. 
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User
from calendar import HTMLCalendar
from .models import Event, EventMember
from django.db.models import Q
from django.shortcuts import get_object_or_404


def get_current_user():
	active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
	user_id_list = []
	for session in active_sessions:
		data = session.get_decoded()
		user_id_list.append(data.get('_auth_user_id', None))
	userid = user_id_list[-1]
	# user = get_object_or_404(User, id=userid)
	return userid

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events, eventmember):
		if eventmember.exists():
			# print("here in formatday: ",eventmember[0].event_id)
			eventid = eventmember[0].event_id
		else:
			eventid = 9999
		userid=get_current_user()
		events_per_day = events.filter(      Q(Q(start_time__day=day))  & Q(Q(id = eventid)| Q(user_id =userid))  )      #兩種情況的其中一種
		d = "<div>"
		
		for event in events_per_day:
			d += f"<div class='event begin end'> {event.get_html_url} </div>"
		d += '</div>'
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events,eventmember):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events,eventmember)
		return f"<tr> {week} </tr>"

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		# print("here current user: ",get_current_user())
		eventmember = EventMember.objects.filter(user_id=get_current_user())
		cal =f'<table border="0" cellpadding="0" cellspacing="0" class=" calendar calendar-table table table-condensed table-tight">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events,eventmember)}\n'
		return cal

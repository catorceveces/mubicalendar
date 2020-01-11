from datetime import datetime, timedelta
from cal_setup import get_calendar_service
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# now showing in mubi

mubi_web = 'https://mubi.com/es/showing'

uClient = uReq(mubi_web)
website = soup(uClient.read(), 'html.parser')
uClient.close()

# grab the movie title and other info

new_movie = website.find('div', class_='showing-page-hero-tile__body-inner')
get_resume = website.find('p', class_='showing-page-hero-tile__our-take light-on-dark u-simple-formatting')

title = new_movie.h2.text
director = new_movie.h3.text
resume = get_resume.text

# working on the google calendar

def main():

   service = get_calendar_service()

   # set the dates of new release and expiration

   d = datetime.now().date()
   today = datetime(d.year, d.month, d.day, 7)
   expiration = datetime(d.year, d.month, d.day, 7)+timedelta(days=29)
   t_start = today.isoformat()
   t_end = (today + timedelta(hours=1)).isoformat()
   e_start = expiration.isoformat()
   e_end = (expiration + timedelta(hours=1)).isoformat()

   # create an event of new release at 07 AM

   t_event = service.events().insert(calendarId='7inlsk349lq5fvf2vorls9mpe8@group.calendar.google.com',
       body={
           "summary": "Hoy se estrena: " + "'" + title + "'",
           "description": director + resume,
           "start": {"dateTime": t_start, "timeZone": 'America/Buenos_Aires'},
           "end": {"dateTime": t_end, "timeZone": 'America/Buenos_Aires'},
       }
   ).execute()

   # create an event of expiration date 29 days after at the same time

   e_event = service.events().insert(calendarId='7inlsk349lq5fvf2vorls9mpe8@group.calendar.google.com',
        body={
            "summary": "Hoy expira: " + "'" + title + "'",
            "description": director + resume,
            "start": {"dateTime": e_start, "timeZone": 'America/Buenos_Aires'},
            "end": {"dateTime": e_end, "timeZone": 'America/Buenos_Aires'},
        }
   ).execute()

if __name__ == '__main__':
   main()

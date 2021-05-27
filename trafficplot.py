'''
This is a script I wrote to aid in apartment hunting by plotting commute times
between potential apartments and work. It uses the google maps api to get
the time it would take to get to work during the morning and then the time it
would take to get home during the afternoon/evening. Traffic is accounted for.
Once rush hour is over a plot of the data is made so you can see when traffic
starts to get worse. Requires matplotlib, googlemaps api, datetime, numpy,
and simplejson
'''

import matplotlib.pyplot as plt
import googlemaps
from datetime import datetime
from time import sleep
import simplejson
import urllib.request
import numpy as np

gmaps = googlemaps.Client(key ='#Enter your google maps api key here' )
API = #Enter api key here again

#enter in apartment/home address and work address
start_address = # "#Enter your start address here "
end_address = # "Enter your end address here"

#get latitude and longitude for both start and end address
start_geocode = gmaps.geocode(start_address)

start_lat = start_geocode[0]["geometry"]["location"]["lat"]
start_lng = start_geocode[0]["geometry"]["location"]["lng"]

start = str(start_lat) + ',' + str(start_lng)

end_geocode = gmaps.geocode(end_address)

end_lat = end_geocode[0]["geometry"]["location"]["lat"]
end_lng = end_geocode[0]["geometry"]["location"]["lng"]

end = str(end_lat) + ',' + str(end_lng)

#hours you consider to be rush hour or times you might go to or from work
am, pm = [6,7,8],[15,16,17]
commute_time = []

while True:
    if datetime.now().hour in am or datetime.now().hour in pm:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + start + "&destinations=" + end + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API
        result = simplejson.load(urllib.request.urlopen(url))
        driving_time_seconds = result['rows'][0]['elements'][0]['duration_in_traffic']['value']
        minutes = driving_time_seconds/60
        commute_time.append(minutes)

        #once rush hour is over, make plot of commute time vs time
        if len(commute_time)>175:
            if datetime.now().hour < 12:
                mode = 'Morning'
            else:
                mode = 'Afternoon'
            time_array = np.linspace(0,len(commute_time)-1,num=len(commute_time))
            plt.plot(time_array,commute_time)
            plt.xlabel('Time (minutes)')
            plt.ylabel('Commute time (minutes)')
            plt.title('Traffic for ' + mode + ' of ' + str(datetime.now().month) + '/'+ str(datetime.now().day))
            plt.grid(True)
            plt.savefig(str(datetime.now().month) + '-' + str(datetime.now().day) +'-'+ mode + '.png')
            break
        sleep(60)
    else:
        pass
        print("Current time is " +str(datetime.now().hour) + ":" + str(datetime.now().minute))
        sleep(60)

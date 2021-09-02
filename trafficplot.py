
import matplotlib.pyplot as plt
import googlemaps
from datetime import datetime
from time import sleep
import simplejson
import urllib.request
import numpy as np
import pandas as pd
import os

gmaps = googlemaps.Client(key ='#Enter your google maps api key here' )
API = #Enter api key here again

#enter in apartment/home address and work address
start_address = # "Enter your start address here "
end_address = # "Enter your end address here"

#get latitude and longitude for both start and end address
start_geocode = gmaps.geocode(start_address)

start_lat = start_geocode[0]["geometry"]["location"]["lat"]
start_lng = start_geocode[0]["geometry"]["location"]["lng"]

start = str(start_lat) + ',' + str(start_lng)
start_temp = start

end_geocode = gmaps.geocode(end_address)

end_lat = end_geocode[0]["geometry"]["location"]["lat"]
end_lng = end_geocode[0]["geometry"]["location"]["lng"]

end = str(end_lat) + ',' + str(end_lng)
end_temp = end

#hours you consider to be rush hour or times you might go to or from work
rush_hours = [6,7,8,15,16,17]
commute_time = []

while True:
    if datetime.now().hour in rush_hours:
        if datetime.now().hour < 12:
            start = start
            end = end
        else:
            start = end_temp
            end = start_temp

        '''
        idx = pd.date_range(datetime.now(), datetime.now()+timedelta(minutes = 179), freq='min')
        df = pd.DataFrame(index = idx, columns=['commute time'])
        i = 0


        '''

        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + start + "&destinations=" + end + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API
        result = simplejson.load(urllib.request.urlopen(url))
        driving_time_seconds = result['rows'][0]['elements'][0]['duration_in_traffic']['value']
        minutes = driving_time_seconds/60
        commute_time.append(minutes)


        '''
        df['commute time'][i] = minutes

        i = i + 1
        '''


        #once rush hour is over, make plot of commute time vs time
        if datetime.now().minute == 59 and datetime.now().hours+1 not in rush_hours:
            if datetime.now().hour < 12:
                mode = 'Morning'
            else:
                mode = 'Afternoon'
            time_array = np.linspace(0,len(commute_time)-1,num=len(commute_time))
            plt.plot(time_array,commute_time)
            plt.xlabel('Time (minutes)')
            plt.ylabel('Commute time (minutes)')
            if mode == 'Morning':
                plt.title('Traffic for ' + mode + ' of ' + str(datetime.now().month) + '/'+ str(datetime.now().day)+ "\nStart = " + start_address + "\nEnd = " + end_address)
            else:
                plt.title('Traffic for ' + mode + ' of ' + str(datetime.now().month) + '/'+ str(datetime.now().day) + "\nStart = " + end_address + "\nEnd = " + start_address)
            plt.grid(True)
            plt.savefig(str(datetime.now().month) + '-' + str(datetime.now().day) +'-'+ mode + '.png')
            commute_time.clear()


            '''
            fig, ax = plt.subplots()
            hours = mdates.HourLocator(interval=1)
            h_fmt = mdates.DateFormatter('%H:%M:%S')

            ax.plot(df.index,df['commute time'].values)

            ax.xaxis.set_major_locator(hours)
            ax.xaxis.set_major_formatter(h_fmt)

            ax.set_ylabel("Commute time (minutes)")
            if mode == 'Morning':
                ax.set_title('Traffic for ' + mode + ' of ' + str(datetime.now().month) + '/'+ str(datetime.now().day) + "\nStart = " + start_address + "\nEnd = " + end_address)
            else:
                ax.set_title('Traffic for ' + mode + ' of ' + str(datetime.now().month) + '/'+ str(datetime.now().day) + "\nStart = " + end_address + "\nEnd = " + start_address)
            plt.grid(True)
            plt.savefig(str(datetime.now().month) + '-' + str(datetime.now().day) +'-'+ mode + '.png')
            del df

            '''
        sleep(60)
    else:
        os.system('clear')
        print("Not collecting data right now; waiting for rush hour")
        sleep(60)

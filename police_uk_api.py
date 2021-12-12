import requests, datetime,time
import pandas as pd

api_locations = {
    '572809' : 'Crewe',
    '699411' : 'Mistley',
    '793830' : 'Hatfield',
    '880870' : 'Wigston',
    '929681' : 'Surbiton',
    '955110' : 'Beckton - Home',
    '962370' : 'Beckton', #Nigtingale Way
    '979396' : 'Wealdstone'
    }

time_now = datetime.datetime.now()
api_dates = []
for i in range(2019,time_now.year):
    for j in range(1,13):
        api_dates.append( str(i)+'-'+str(j) )

while True:
    
    maindf = pd.DataFrame(columns=('month','category','area'))
    time_now = datetime.datetime.now()

    for j in range(1,time_now.month):
        api_dates.append( str(time_now.year)+'-'+str(j) )
    
    base_url = 'https://data.police.uk/api/crimes-at-location'

    for api_date in api_dates:
        for api_location in api_locations:
                  
            filters = [
                'date={}'.format(api_date),
                'location_id={}'.format(api_location)
                ]

            api_filters = str.join("&", filters)
           
            with requests.get(base_url, params=api_filters, timeout=10) as api_response:
                                           
                if api_response.status_code == 200 and api_response.content.decode() != '[]':
                    print("data")    
                    subdf = pd.DataFrame(pd.read_json(api_response.content.decode()), columns = ('month', 'category')) #converting json into pd obj for pd df
                    subdf.insert(2, "area", (1+subdf.last_valid_index())*[api_locations.get(api_location)]) #adding a column with area name
                    maindf = maindf.append(subdf, ignore_index = True)
                    del subdf
                else:
                    print("no data for {} in {}".format(api_locations.get(api_location),api_date))
    
    maindf.to_csv(r'/media/ubuntu/524A9ACC4A9AABEB/Fileshare - Pi Laptop/DB.PythonDatasets/api_policeUK/police_api_output_'+str(time_now.strftime('%Y-%m-%d'))+'.csv', \
                  encoding='utf-8',index=False, header=True, mode="w")
    print(maindf)
    del maindf
    
    this_run = datetime.datetime.now()
    next_run = datetime.datetime(this_run.year,this_run.month,20) + datetime.timedelta(days=30)
    pause = int((next_run-this_run).total_seconds())
    print('next run will be {} in {} seconds'.format(next_run, pause))
    
    time.sleep(pause)

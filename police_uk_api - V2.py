import requests, datetime,time
import pandas as pd

api_locations = {
    '699411' : 'Mistley',
    '793830' : 'Hatfield',
    '880870' : 'Wigston',
    '929681' : 'Surbiton',
    '955110' : 'Beckton',
    '979396' : 'Wealdstone',
    }

api_dates = []
for i in range(2019,2021):
    for j in range(1,13):
        api_dates.append( str(i)+'-'+str(j) )

while True:

    time_now = datetime.datetime.now()

    for j in range(1,time_now.month):
        api_dates.append( str(time_now.year)+'-'+str(j) )
    
    #https://data.police.uk/api/crimes-at-location?date=2017-02&location_id=884227
    base_url = 'https://data.police.uk/api/crimes-at-location'

    for api_date in api_dates:
        for api_location in api_locations:
                  
            filters = [
                'date={}'.format(api_date),
                'location_id={}'.format(api_location)
                ]

            api_filters = str.join("&", filters)
            
            api_response = requests.get(base_url, params=api_filters, timeout=10).content.decode() #returned a list
            
            if api_response != '[]':
                print("data")    
                df = pd.DataFrame(pd.read_json(api_response), columns = ('month', 'category')) #converting json into pd obj for pd df
                df.insert(2, "area", (1+df.last_valid_index())*[api_locations.get(api_location)]) #adding a column with area name
                df.to_csv('police_api_output_'+str(time_now.strftime('%Y-%m-%d'))+'.csv', encoding='utf-8',index=False, header=False, mode="a")
                print(df)
            elif api_response == '[]':
                print("no data for {} in {}".format(api_locations.get(api_location),api_date))
    
    this_run = datetime.datetime.now()
    next_run = datetime.datetime(this_run.year,this_run.month,20) + datetime.timedelta(days=30)
    pause = int((next_run-this_run).total_seconds())
    print('next run will be {} in {} seconds'.format(next_run, pause))
    
    time.sleep(pause)

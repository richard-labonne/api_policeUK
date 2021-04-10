import requests, datetime, time, os, dropbox
import pandas as pd

locations = files_in_main_dir = []

while True:
    this_run = datetime.datetime.now()

    for year in range(2019,this_run.year):
        for month in range(1,13): #12 months
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.9400123&lng=1.0602633') #mistley
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.511663&lng=0.044980') #here
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=52.5944465&lng=-1.1159519') #wigston
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.5972548&lng=-0.3300578') #wealdstone
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.3782438&lng=-0.2938748') #surbiton
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.7454526&lng=-0.2343447') #hatfield
            
    for year in [this_run.year]:
        for month in range(1, this_run.month): #current month data unavailable
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.9400123&lng=1.0602633') #mistley
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.511663&lng=0.044980') #here
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=52.5944465&lng=-1.1159519') #wigston
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.5972548&lng=-0.3300578') #wealdstone
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.3782438&lng=-0.2938748') #surbiton
            locations.append('https://data.police.uk/api/crimes-at-location?date='+str(year)+'-'+str(month)+'&lat=51.7454526&lng=-0.2343447') #hatfield
    for URL in locations:
        data = requests.get(URL).text
        df = pd.read_json(data)
        df.to_csv('police_api_ad_hoc_'+str(this_run.strftime('%Y-%m-%d'))+'.csv', encoding='utf-8',index=False, header=False, mode="a")

    files_in_main_dir = os.listdir('/media/pi/524A9ACC4A9AABEB/Fileshare - Pi Laptop/police_uk_api//')
    
    for file in files_in_main_dir:
        
        overwrite = dropbox.files.WriteMode.overwrite
        dropbox_access_token = "s51dOPNg5sUAAAAAAAAAAaj28WYp4SVh5X01n7TyXJewi8P9UPvI1iUyLVD99U8l" #App: Weather Model
        
        files_in_main_dir = os.listdir('/media/pi/524A9ACC4A9AABEB/Fileshare - Pi Laptop/police_uk_api//')
        source_file = '/media/pi/524A9ACC4A9AABEB/Fileshare - Pi Laptop/police_uk_api//' + file
        sink_file = '/Study/Python/programs/showcase programs/police_uk_api/' + file
        
        with dropbox.Dropbox(dropbox_access_token) as rl_dropbox:
            with open(source_file,"rb") as payload:
                rl_dropbox.files_upload(payload.read(), sink_file, overwrite)
        
    next_run = datetime.datetime(this_run.year,this_run.month,20) + datetime.timedelta(days=30)
    pause = int((next_run-this_run).total_seconds())
    print('next run will be {} in {} seconds'.format(next_run, pause))
    print(len(locations))
    locations.clear()
    files_in_main_dir.clear()
    time.sleep(pause)

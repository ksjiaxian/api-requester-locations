import requests
import csv


with open('files/affiliationnamefreq100_withlocations_BING.tsv', encoding='latin-1') as tsvfile:
    with open('files/affiliationnamefreq100_fullLocations_BING.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            print(cnt)
            address = str(row['affiliationname'])
            
            #google
            #response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    #params={"key":"ADD_KEY_HERE", 
                            #"address":address})
            
            #bing
            response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + address,
                        params={"include":"queryParse",
                                "key":"ADD KEY HERE"})

            try:
                #google
                #data = response.json()
                #lat = data['results'][0]['geometry']['location']['lat']
                #lng = data['results'][0]['geometry']['location']['lng']
                
                #bing
                data = response.json()
                lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                
                tsv_writer.writerow([address, row['freq'], str(lat), str(lng)])
            except:
                tsv_writer.writerow([address, row['freq'], "N/A", "N/A"])
            
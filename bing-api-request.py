import requests
import csv


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/affiliationnamefreq100_fullLocations_BING.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            print(cnt)
            address = str(row['affiliationname'])
            
            #bing
            response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + address,
                        params={"include":"queryParse",
                                "key":"PUT KEY HERE"})

            try:
                #bing
                data = response.json()
                lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                
                tsv_writer.writerow([address, row['freq'], str(lat), str(lng)])
            except:
                tsv_writer.writerow([address, row['freq'], "N/A", "N/A"])
            
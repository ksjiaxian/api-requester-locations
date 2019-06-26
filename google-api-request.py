import requests
import csv


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/affiliationnamefreq100_fullLocations_GOOGLE.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', "full_address", 'street_address', 'city', 'country', 'postal_code', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            print(cnt)
            row_information = []
            
            input_name = str(row['affiliationname'])
            row_information.append(input_name)
            
            freq = row['freq']
            row_information.append(freq)
            
            #google
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    params={"key":"PUT KEY HERE", 
                            "address":address})
            
            

            try:
                data = response.json()
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
            except:
                lat = "N/A"
                lng = "N/A"
                
            row_information.append(lat)
            row_information.append(lng)
                
                
                
                
            tsv_writer.writerow(row_information)
            
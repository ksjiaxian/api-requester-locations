import requests
import csv


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/affiliationnamefreq100_fullLocations_GOOGLE.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            print(cnt)
            address = str(row['affiliationname'])
            
            #google
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    params={"key":"AIzaSyCRi5yASpUL9tw6HRN-0KnNgk5JWCdul0M", 
                            "address":address})

            try:
                #google
                data = response.json()
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                
                
                tsv_writer.writerow([address, row['freq'], str(lat), str(lng)])
            except:
                tsv_writer.writerow([address, row['freq'], "N/A", "N/A"])
            
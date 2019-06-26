import requests
import csv


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/google_output.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', "formatted_address",'locality', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            if cnt < 20000 or cnt > 20001:
                continue
            
            print(cnt)
            row_information = []
            
            input_name = str(row['affiliationname'])
            row_information.append(input_name)
            
            freq = row['freq']
            row_information.append(freq)
            
            #google
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    params={"key":"AIzaSyCcsjo5ZQvWGpzRfyY2sslPaSESogu0JrQ", 
                            "address":input_name})
            
            try:
                data = response.json()
                print(data)
            
                #get the formatted address
                try:
                    formatted_address = data['results'][0]['formatted_address']
                except:
                    formatted_address = "N/A"
                    
                row_information.append(formatted_address)
                    
                #get locality
                locality = "N/A"
                try:
                    for component in data['results'][0]['address_components']:
                        if 'locality' in component['types'] or 'sublocality' in component['types']:
                            locality = component['long_name']
                    row_information.append(locality)
                except:
                    row_information.append(locality)
                            
                #get the country
                country = "N/A"
                try:
                    for component in data['results'][0]['address_components']:
                        if 'country' in component['types']:
                            country = component['long_name']
                    row_information.append(country)
                except:        
                    row_information.append(country)
                    
                try:
                    
                    lat = data['results'][0]['geometry']['location']['lat']
                    lng = data['results'][0]['geometry']['location']['lng']
                except:
                    lat = "N/A"
                    lng = "N/A"
                    
                row_information.append(lat)
                row_information.append(lng)
                
                tsv_writer.writerow(row_information)
            
            except:
                tsv_writer.writerow([input_name, freq, "N/A", "N/A", "N/A", "N/A", "N/A"])
            
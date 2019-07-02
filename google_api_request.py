import requests
import csv
from unidecode import unidecode


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/google_writeup_output.tsv', 'w', newline="\n", encoding='utf-8') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', "formatted_address",'locality', 'admin_district', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            
            #only print out every 100th number
            if cnt % 100 == 0:
                print(cnt)
                
            row_information = []
            
            input_name = unidecode(str(row['affiliationname']))
            row_information.append(input_name)
            
            freq = row['freq']
            row_information.append(freq)
            
            #google
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    params={"key": "AIzaSyCsi6Ifq8Y2kispVYnL5DfZX3lK2--DsTs", 
                            "address": input_name})
            
            try:
                response.json()
            except ValueError:
                tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                continue
            
            try:
                data = response.json()
            
                #get the formatted address
                try:
                    formatted_address = data['results'][0]['formatted_address']
                    row_information.append(formatted_address)
                except:
                    row_information.append("N/A")
                    
                #get locality
                try:
                    for component in data['results'][0]['address_components']:
                        if 'locality' in component['types'] or 'sublocality' in component['types']:
                            locality = component['long_name']
                    row_information.append(locality)
                except:
                    row_information.append("N/A")
                    
                #get the admin district
                try:
                    for component in data['results'][0]['address_components']:
                        if 'administrative_area_level_1' in component['types']:
                            admin_district = component['long_name']
                    row_information.append(admin_district)
                except:
                    row_information.append("N/A")
                            
                #get the country
                try:
                    for component in data['results'][0]['address_components']:
                        if 'country' in component['types']:
                            country = component['long_name']
                    row_information.append(country)
                except:        
                    row_information.append("N/A")
                    
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
                data = response.json()
                row_information = []
                row_information.append(input_name)
                row_information.append(freq)
            
                #get the formatted address
                try:
                    formatted_address = data['results'][0]['formatted_address']
                    row_information.append(unidecode(formatted_address))
                except:
                    row_information.append("N/A")
                    
                #get locality
                try:
                    for component in data['results'][0]['address_components']:
                        if 'locality' in component['types'] or 'sublocality' in component['types']:
                            locality = component['long_name']
                    row_information.append(unidecode(locality))
                except:
                    row_information.append("N/A")
                    
                #get the admin district
                try:
                    for component in data['results'][0]['address_components']:
                        if 'administrative_area_level_1' in component['types']:
                            admin_district = component['long_name']
                    row_information.append(unidecode(admin_district))
                except:
                    row_information.append("N/A")
                            
                #get the country
                try:
                    for component in data['results'][0]['address_components']:
                        if 'country' in component['types']:
                            country = component['long_name']
                    row_information.append(unidecode(country))
                except:        
                    row_information.append("N/A")
                    
                try:
                    lat = data['results'][0]['geometry']['location']['lat']
                    lng = data['results'][0]['geometry']['location']['lng']
                except:
                    lat = "N/A"
                    lng = "N/A"
                    
                row_information.append(lat)
                row_information.append(lng)
                
                tsv_writer.writerow(row_information)

import requests
import csv
from unidecode import unidecode

with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/bing_output.tsv', 'w', newline="\n", encoding='utf-8') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'formatted_address', 'locality', 'admin_district', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            
            if cnt > 10:
                break
            
            #only print out every 100th number
            if cnt % 100 == 0:
                print(cnt)
            
            input_name = unidecode(str(row['affiliationname']))
            freq = row['freq']
            
            #bing
            response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/?",
                        params={"query": input_name,
                                "include": "queryParse",
                                "key": "Ahrn_2njXN5bYX-QWFpvfQqJJFTuIOvCnacTFbTLO48RL8rjYVZbmC5Fw6YTM5tb "})
            
            try:
                response.json()
            except ValueError:
                tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                continue
           
            try:
                data = response.json()
                print(data)
                
                row_list = []
                row_list.append(input_name)
                row_list.append(freq)
                
                # formatted_address
                try:
                    #bing
                    address = data['resourceSets'][0]['resources'][0]['address']['formattedAddress']
                    row_list.append(address)
                except:
                    row_list.append("N/A")
                
                # locality
                try:
                    #bing
                    locality = data['resourceSets'][0]['resources'][0]['address']['locality']
                    row_list.append(locality)
                except:
                    row_list.append("N/A")
                
                #admin district or state
                try:
                    #bing
                    admin_district = data['resourceSets'][0]['resources'][0]['address']['adminDistrict']
                    row_list.append(admin_district)
                except:
                    row_list.append("N/A")
                    
                # country
                try:
                    #bing
                    country = data['resourceSets'][0]['resources'][0]['address']['countryRegion']
                    row_list.append(country)
                except:
                    row_list.append("N/A")
                
                
                # get lat and long
                try:
                    #bing
                    lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                    lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                    row_list.append(lat)
                    row_list.append(lng)
                except:
                    row_list.append("N/A")
                    row_list.append("N/A")
                    
                tsv_writer.writerow(row_list)
                
            except:
                data = response.json()
            
                row_list = []
                row_list.append(input_name)
                row_list.append(freq)
                
                # formatted_address
                address = data['resourceSets'][0]['resources'][0]['address']['formattedAddress']
                row_list.append(unidecode(address))
                
                
                
                # locality
                locality = data['resourceSets'][0]['resources'][0]['address']['locality']
                row_list.append(unidecode(locality))
                
                #admin district or state
                admin_district = data['resourceSets'][0]['resources'][0]['address']['adminDistrict']
                row_list.append(unidecode(admin_district))
                
                # country
                country = data['resourceSets'][0]['resources'][0]['address']['countryRegion']
                row_list.append(unidecode(country))
                
                
                # get lat and long
                try:
                    #bing
                    lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                    lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                    row_list.append(lat)
                    row_list.append(lng)
                except:
                    row_list.append("N/A")
                    row_list.append("N/A")
                    
                tsv_writer.writerow(row_list)

                
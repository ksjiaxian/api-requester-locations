import requests
import csv


with open('files/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('files/bing_output.tsv', 'w', newline="\n", encoding='latin-1') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'formatted_address', 'locality', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            print(cnt)
            input_name = str(row['affiliationname'])
            freq = row['freq']
            if (cnt < 20000 or cnt > 20150): 
                continue
            #bing
            response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + input_name,
                        params={"include":"queryParse",
                                'output': "json",
                                "key":"AjhzSUKjNFFV0ckKVCV64tSLhw_EWSlN6LP9UPiWdEJDRMZn3Vm17HtoSclZZfO_ "})

            try:
                data = response.json()
                
                row_list = []
                row_list.append(input_name)
                row_list.append(freq)
                
                
                
                # formatted_address
                try:
                    #bing
                    address = data['resourceSets'][0]['resources'][0]['address']['formattedAddress']
                    row_list.append(address)
                except:
                    row_list.append()
                
                
                
                # locality
                try:
                    #bing
                    locality = data['resourceSets'][0]['resources'][0]['address']['locality']
                    row_list.append(locality)
                except:
                    row_list.append()
                
                
                # country
                try:
                    #bing
                    country = data['resourceSets'][0]['resources'][0]['address']['countryRegion']
                    row_list.append(country)
                except:
                    row_list.append()
                
                
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
                tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            
            
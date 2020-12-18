def pull_citi_data(filename: str) -> None:
    """Connects to Citibike's S3 bucket, extracts, and stores the trip data into the temp_data_folder

    Parameters
    ----------
    filename : str
        The name of a file in the Citibike S3 bucket (stem only)

    Returns
    -------
    None:
        If executed properly there should be a CSV file in the TEMP_BIKE_FOLDER.
    """
    
    # The purpose of the following try block is to attempt to connect to the file in the Citibike S3 bucket 
    # and catch the different errors that may occur if the connection fails. A failed connection exists the function
    
    try:
        r = requests.get(CITIBIKE_DATA_FOLDER + filename, stream=True)   
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        # The firt block might fail due to the inconsistency of the naming convention
        # Starting in 2017 the bucket endings changed from .zip -> .csv.zip
        # We try to connect again with the new ending 
        try:
            r = requests.get(CITIBIKE_DATA_FOLDER + filename[:-4] + '.csv.' + filename[-3:])
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh: 
            print(errh)
            return None
        else:
            print(f"Request Success: {filename[:-4] + '.csv.' + filename[-3:]} requested from Citibike S3 Bucket")       
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        return None
    except requests.exceptions.Timeout as errt:
        print(errt)
        return None
    except requests.exceptions.RequestException as err:
        print(err)
        return None
    else:
        print(f"Request Success: {filename} requested from Citibike S3 Bucket")
    
    # ==============================================================================================================
    #The with block belows purpose is to unzip the file and extract it to the Temporary Bike Folder defined above.
    
    with zipfile.ZipFile(io.BytesIO(r.content), 'r') as zip: 
        
        # Regardless of the change in naming conventions, the actual data appears first in every bucket
        datafile = zip.namelist()[0] 
               
        if os.path.exists(TEMP_BIKE_FOLDER + datafile):
            print(f"Skipped: {datafile} already extracted from Citbike S3 Bucket \n")
            return None
        
        zip.extract(datafile, path = TEMP_BIKE_FOLDER)
    
    print(f"Extract Success: {datafile} unzipped and uploaded to {TEMP_BIKE_FOLDER} \n")
    return None


"==========================================================================================="

def pull_hood_data(code: str, name: str) -> None:
    """Uses the scraped neighborhood code to download the xlsx data from Furman Center
    
    Parameters
    ----------
    code: str
        The 4 character neighborhood string
    name: str
        The actual name of the neighborhood
    Returns
    -------
    None:
        If executed properly there should be an XLSX file in the TEMP_HOOD_FOLDER.
    """
    
    file = f"https://furmancenter.org/files/NDP/{code}_NeighborhoodDataProfile.xlsx"
    
    if os.path.exists(TEMP_HOOD_FOLDER + f"{code}_{name}.xlsx"):
        print(f"Skipped: {code}_{name} already downloaded from Furman Center")
        return None
    
    try:
        r3 = requests.get(file)
        r3.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(errh)
        return None
    else:
        print(f"Request Success: {file} from Furman Center")
    
    with open(TEMP_HOOD_FOLDER + f"{code}_{name}.xlsx", 'wb') as output:
        output.write(r3.content)
    
    return None
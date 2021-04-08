<div style='text-align:center;'>
    <img style="float:right;" src="./Data/Images/Report/0000.Coffee-Bike.png" width="160" />
    <span style="float:center;text-align:center">
        <span style="text-align:center">
        <p style="text-align:center;margin:0;font-size:12px;color:#c1121f"> <b> Data Science = Solving Problems = Happiness </b> </p>
        <p style="text-align:center;font-size:40px;margin:0"> <b> Bike Share USA</b> </p>
        <p style="text-align:center;margin:0"> Denzel S. Williams </p>
        <p style="text-align:center;margin:0"> <i> Springboard Data Science Track '20 </i> </p>
        </span>
        <a href="https://linkedin.com/in/williamdst">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="75" />
        </a>
    </span>
</div>


<h2> The Inspiration </h2>

From 2013 - 2020 I lived in Melbourne, FL without a car; and for those 7 years I pretty much walked to every spot in the 32901/32905 zip code. Grocery stores, check; The Mall, check; College, check; Downtown, check; The Gym, check; Restaurants, check; Barber Shop, check; Places that shouldn't be listed, check. 

<p style="text-align:center;" align='center'> <i><b> Shoutout to any friend that ever gave me a ride to any place ever.</b></i></p>

The height of my walking took place in the last two years when I was teaching at Palm Bay HS. The public bus to take me to the school came ONCE every hour at an inconveient time either getting me to work too early or too late. Even worse the routes were not symmetrical and the bus couldn't take me back home. So the solution was to walk in the Florida heat everyday for two years.
<ul>
    <li> Why didn't you buy a car? I was BARELY not a broke college student.
    <li> Ok, why didn't you just get a bike? My apartment couldn't accommodate a bike.
    <li> You could've taken Ubers. Have you lost your mind???
</ul>

Moving back home in 2020, I discovered New York City's bike sharing program, CitiBike, and wished I had this service during my time in Florida. Even better, I am "fortunate" enough to live in a zip code that <b>doesn't</b> have bikes. So out of wishful thinking and an accidental ingredient of pure jealously, the Bike Share USA project was born. 



<h2> Introduction </h2>



<h2> The Data Wrangling </h2>

The data used to complete the project can be broken into four major groups. The first two groups were fundamental to completing the project and the other half were required for the Exploratory Data Analytics (EDA):

<b> Bike Share Trip Datasets </b> <br>
The subset of zip codes that have bike stations are derived from the five largest bike sharing services in the US: Bay Wheels, Blue Bike, Capital Bikeshare, Citi Bike, and Divvy Bike. Each company hosts their trip data on S3 buckets for public use. These datasets hold key information about each trip that was taken by their customers. The rows of the datasets represent a single trip; the columns are the properties of the trip such as the starting station and the time when the trip ended. Since the trip data includes the start and end stations, the station data used to make the predictions was derived from these datasets.

<ul>
    <li> Dataset I - <a href="https://s3.amazonaws.com/baywheels-data/index.html"> BayWheels S3 Trip Data Bucket </a>
    <li> Dataset II - <a href="https://s3.amazonaws.com/hubway-data/index.html"> BlueBike S3 Trip Data Bucket </a>
    <li> Dataset III - <a href="https://s3.amazonaws.com/capitalbikeshare-data/index.html"> Capital S3 Trip Data Bucket </a>
    <li> Dataset IV - <a href="https://s3.amazonaws.com/tripdata/index.html"> CitiBike S3 Trip Data Bucket </a>
    <li> Dataset V - <a href="https://divvy-tripdata.s3.amazonaws.com/index.html"> DivvyBike S3 Trip Data Bucket </a>
</ul>

<b> Zip Code Datasets </b> <br>
All the zip codes of the US along with the properties of the zip code are included in this group. Properties such as the total population, core based statistical area classification, and water area are included. Two supplementary files were used to help fill missing values within the main zip code file. 

<ul>
    <li> Dataset XI - <a href="https://github.com/Williamdst/Bike-Share-USA/blob/main/Data/ZX01_Zipcodes-USA.csv"> Zipcode USA Data </a> (<i>Download the raw .txt file and then change the extension to .csv</i>)
    <li> Dataset XII -<a href="https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2020/delineation-files/list1_2020.xls" > Delineation File </a>
    <li> Dataset XIII -
<a href="https://www.huduser.gov/portal/datasets/usps_crosswalk.html"> USPS Zipcode Crosswalk Files</a>
</ul>


<b> Geospatial Datasets </b> <br>
New York City (NYC) and San Francisco has geospatial boundaries of their segmented neighborhoods. The datasets in this group contain those geospatial multi-polygons. Additionally, the geospatial locations of the MTA Subway Entrances was gathered for particular analytics section.

<ul>
    <li> Dataset VIII - <a href="https://data.cityofnewyork.us/api/geospatial/yfnk-k7r4?method=export&format=GeoJSON"> NYC Community District GeoJSON File </a>
    <li> Dataset IX - <a href="https://data.sfgov.org/api/geospatial/p5b7-5n3h?method=export&format=GeoJSON"> San Francisco Community District GeoJSON File </a>
    <li> Dataset X - <a href="https://data.cityofnewyork.us/api/geospatial/drex-xx56?method=export&format=GeoJSON"> Subway Entrance GeoJSON File </a>
</ul>

<b> Neighborhood Profile Datasets </b> <br>
The datasets in this group have the demographics of those segmented neighborhoods. These demographics, when combined with the geospatial data were used to do two custom analyses in the EDA portion of the project. The analysis used both the station location point geometries and the Voronoi polygons of the station locations. 

<ul>
    <li> Dataset VI - <a href = "https://furmancenter.org/neighborhoods"> New York City Neighborhood Profiles </a>
    <li> Dataset VII - <a href = "https://default.sfplanning.org/publications_reports/SF_NGBD_SocioEconomic_Profiles/2012-2016_ACS_Profile_Neighborhoods_Final.pdf"> San Francisco Neighborhood Profiles </a>
</ul>





<h2> The Database 
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" width="75" />
    <img src="https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" width="75" />
    <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" width="80" />
</h2>

All the datasets summed to over 68 GB of data across 350+ files. To work with this data, the best course of action was to build a database. Leveraging the Amazon Web Services (AWS) Cloud a RDS Database running PostgreSQL 12.5 was created on a db.t3.micro instance. With the blank database created, before doing anything, it was important to think about how the data was going to be used for analytics; to determine how it should be feed into the database. With that idea in mind an Entity Relationship Diagram (ERD) was created to structure the database and guide the transformation portion of the upcoming Extract Transform and Load (ETL) jobs. 

<figure style="text-align:center" align='center'>
    <img src="./Data/Images/Report/0003.ERD-Final.png" style="max-width:50%" />
    <figcaption style="text-align:center"> Figure 2. Entity Relationship Diagram of the Database </figcaption>
</figure>

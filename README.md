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

<p align='center'>
    <img src="./Data/Images/Report/0003.ERD-Final.png" align='center' width="550" />
    <p align='center'> Figure 2. Entity Relationship Diagram of the Database </p>
</p>




<h2> Exploratory Data Analytics </h2>
The full EDA can be found in the <a href=""> BSU-Report </a>. Some sample analyses are shown below. 

<h3> Inter Zip Code Travel </h3>

The significance of this project is to guide a bike share company's expansion into new areas. For an expansion into a new area, it is important to expand into multiple zip codes in a region, but the ultimate question is <b>how many</b>. To get an idea of how things should be done, the number of zip codes the stations were spread across when the five services made their inital launches was determined. Additionally, the number of zip codes the stations were in at the end of 2020 was determined. 

<p align='center'>
    <img src="./Data/Images/Report/0013.Zip-Expand.jpg" align='center' width="500" />
    <p align='center'> Table 1. The initial number of zip codes a bike sharing service launched in and the current number of zip codes it covers. </p>
</p>



<h3> How Many People Does Each Station Serve? </h3>

When people use public transportation they go to the spot that is most convient for them. Typically, conveient means the closet. I say typically because there are times when people have to go farther distances to catch a bus or train because the route of the bus/train is more conveient for where they are headed. However, in the case of bike share, there is no incentive to go to a bike station that is farther away from the one that is closet to you. Therefore a station only serves the people that are closer to it than to any other station. The number of people a station serves is defined by the equation:

<p align='center'>
    <img align='center' src="https://render.githubusercontent.com/render/math?math=S(s) = \sum_{i=1}^{N}\frac{A(G_i \cap V_s)}{A(G_i)} \cdot P_i"> 
</p>

where <img src="https://render.githubusercontent.com/render/math?math=S(s)"> is the number of people served by station <img src="https://render.githubusercontent.com/render/math?math=s">, <img src="https://render.githubusercontent.com/render/math?math=N"> is the number of neighborhoods in the region (NYC or San Francisco), <img src="https://render.githubusercontent.com/render/math?math=A"> is the area function, <img src="https://render.githubusercontent.com/render/math?math=G_i"> is the geometry polygon for neighborhood <img src="https://render.githubusercontent.com/render/math?math=i">, <img src="https://render.githubusercontent.com/render/math?math=V_s"> is the voronoi polygon for station <img src="https://render.githubusercontent.com/render/math?math=s">, <img src="https://render.githubusercontent.com/render/math?math=P_i"> is the population for neighborhood <img src="https://render.githubusercontent.com/render/math?math=i">. 

<p align='center'> <b><i>A Simple Interpretation of the Formula: It's multiplying the portion of a station's voronoi polygon that is in a neighborhood by the population density of that neighborhood.</i></b>
</p>

<p align='center'>
    <img src="./Data/Images/Report/0014.NYC-Serve-Box.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <img src="./Data/Images/Report/0014.NYC-Serve-Kernel.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <img src="./Data/Images/Report/0014.NYC-Serve-Strip.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <p style="clear:both;">
    <p align='center'> Figure 3. Different visulizations of the number of people served by bike stations in New York City. </p>
</p>

Each of the three graphs above show the number of riders served by stations in NYC. They reveal that majority of stations, about 75%, serve between 100K and 225K people. There is a smaller group that serve between 225K and 350K people. Although the people served statistic is interesting, it isn't very useful on in its own. It's impossible to tell if a station with a higher statistic has a bigger voronoi area or has a smaller voronoi area in a denser part of the city. A better statistic to look at would be the ratio between the riders served and the area of the voronoi. The graphs of the ratios for both cities are shown in the graphs below:

<p align='center'>
    <img src="./Data/Images/Report/0017.NYC-Serve-Ratio-Box.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <img src="./Data/Images/Report/0017.NYC-Serve-Ratio-Kernel.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <img src="./Data/Images/Report/0017.NYC-Serve-Ratio-Borough.jpg" style="float: left; width: 30%; margin-right: 3%; margin-bottom: 0.5em;" />
    <p style="clear:both;">
    <p align='center'> Figure 4. Different visualizations of the <b> ratio </b> between people served and the voronoi area of stations in New York City</p>
</p>

Looking at just riders served the data was really spread out, the data is much tighter when looking at the ratio between the riders served and the area of the voronoi. Regardless of the borough, regardless of the location, the number of people that a station serves in NYC is rarely over 3.5 people per square meter of it's voronoi polygon. Which makes practical sense because the denser the population of an area the more stations you need to accomodate the population. The more stations packed into one area, the smaller the voronoi area. Although the area is small, it is still serving tons of people. Population density may be an extremely important factor when a company chooses the number of; and the locations of stations in a potential expansion area. 

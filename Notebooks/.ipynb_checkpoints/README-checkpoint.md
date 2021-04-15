<p align="center">
    <b> Use the 
        <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/">
            <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
        </a> 
        Links to View the Notebooks on NBviewer 
    </b>
</p>

<h2> Data Wrangling 
    <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/01.Data-Wrangling.ipynb">
        <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
    </a>
</h2> 
The goal of this notebook is to get all the required data needed to complete the project. The vision for this project is that all files needed for any analysis be stored in the cloud (AWS S3), separate from the directory of the code. In the "Upload..." sections of the notebook the extracted data is uploaded from a temporary local folder to a personal S3 bucket. For the remainder of the project, all data will be pulled from that S3 bucket. 

<h2> Building the Database 
    <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/02.Building-Database.ipynb">
        <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
    </a>
</h2>
In the <i>Data Wrangling</i> notebook ten different sets,over 350 files, were gathered in the S3 bucket. To work with all this data, the best course of action will be to build a database that can be queried from. The database that is built in this notebook will have the majority of the data needed to complete the project. Four schemas are used to organize the database and the database diagram is shown below:
<ol>
    <li> The Staging Schema: Has all the raw trip data for each of the different bike share services
    <li> The Trips Schema: Has all the filtered and edited trip data for each of the different bike share services
    <li> The Stations Schema: Has all the stations for each of the different bike share services
    <li> The Neighborhoods Schema: Has all the information for different zipcodes within the United States as well as neighborhood data from New York City (NYC) and San Francisco
</ol>

<h2> Modifying the Database 
    <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/03.Modifying-Database.ipynb">
        <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
    </a>
</h2>
With the database created, in this section, modifications will be made to some tables through updates and deletes to get it ready for the Exploratory Data Analytics in the following section. The two schemas that will be of focus are the Trip and Stations schema. The modifying of these schemas has to be done on a massive scale and it requires us to clean it directly in the database itself. 

The other neighborhood schema has small datasets that can be cleaned locally. More so than that, it is important that these tables remain raw in the database to conserve the integrity of the data. This also conserves the <b>OPTION</b> of cleaning it how we see fit at any time in the future as compared to finalizing the clean. Directly related to that idea, another person querying from the database won't know how the data was chosen to be cleaned. 
    

<h2> EDA 
    <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/04.EDA.ipynb">
        <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
    </a>
</h2>
After three notebooks the data is in a position where it can be used to uncover insights. Since this project is focused on stations, the trip data was only needed to get the station data. However, it is possible that the trip data contains gems of insight. In this notebook the data in the Trips and Stations schema will be explored. First, some very basic exploratory analysis on the trip data will be done and then more in-depth analysis on the station data.
    

<h2> Prediction 
    <a href="https://nbviewer.jupyter.org/github/Williamdst/Bike-Share-USA/blob/main/Notebooks/05.Prediction.ipynb">
        <img align='center' src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" width='53' />
    </a>
</h2>
In the final notebook of the project we do what we set out to do in the first place: predict the number of stations that should be in a given zipcode. First the known number of stations in a handful of zip codes will be counted. This count will be the target value in the regression problem and the features will be the columns of the zipcode dataset that were gathered back in notebook 1. After the model is trained a pipeline will be constructed to take in the information for all the zipcodes that don't already have bike stations. 
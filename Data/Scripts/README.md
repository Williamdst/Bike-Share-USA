<h2> Introducing the Queries Package </h2>

The Queries Package is a custom package containing custom queries that execute against our database. The most used function in this package is the execute_query function which takes in a SQL statement and makes the execution. There are queries that return results and the execute_query function has the option of returning the results as a pandas dataframe or a 2 length tuple of the (column_names, data).

<h2> Future Updates </h2>

In future installments of the project, this folder will contain the scripts that can be used to download the data from the 5 different bike share company's S3 buckets. I am hoping that these scripts can be used to help stream the data directly from the companies' S3 bucket to my database. 

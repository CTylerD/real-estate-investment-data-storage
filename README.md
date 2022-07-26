# Real Estate Investment App Storage Microservice

This API service allows for storing data calculated by a real estate investment calculator/evaluator web app service.

## Storing Data

To store data, submit an HTTP POST or PUT request to the */add* endpoint, with a body that contains a JSON object with all of the calculated data. The keys in this JSON object should be to the following strings, and the values should contain the corresponding data points:

"address"  
"market value"  
"expenses"  
"fees"  
"anticipated ROI"  

The values of each calculation will be stored in a CSV format with a unique ID, so it will be possible for multiple requests to be stored with the same data, since they will be stored with unique IDs corresponding to each calculation request.

Each successful data storage request will receive a response containing the submitted JSON of calculated values, with an additional "id" key added, with that requests data id set as the value.

## Retrieving Data

To retrieve data, submit an HTTP GET request to the */retrieve/\<id>* endpoint, where \<id> contains the id value of the stored data calculation that you wish to receive. The data will then be pulled from the CSV and sent back to the client in an identical manner to the data storage response, with all of the calculated values stored under their corresponding keys plus the "id" value as well.

## UML sequence diagram
![](uml.png)
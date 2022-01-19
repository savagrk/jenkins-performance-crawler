# Jenkins Performance Plugin Results Crawler

Crawler for parsing and comparison of Performance Results obtain by Jenkins Performance Plugin.

## Usage

In DataProcessor.py set **URLs**, **crawler_option**, **data_type** and **threshold** values and run the script. 

**URLs** - Jenkins Performance Plugin URLs that will be used for getting results,

**crawler_option** - which mode of commparison will be used,

**data_type** - which type of data provided by Jenkins Performance Plugin will be used,

**threshold** - defines value below which results will not be collected from Jenkins Performance Plugin.

## Currently supported Crawler Options are:
        
 **1** - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than Previous Job and Error Request Results per single URL in single Excel File
                
 **2** - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than and Error Request Results per single URL in separate Excel Files
                
 **3** - Responses over entered Threshold Results per single URL 
            in single Excel File
            
 **4** - Request Responses Better than Previous and Request Responses Worse than Previous Results
            per single URL in single Excel File
            
 **5** - Error Requests Results per single URL in single Excel File
            
 **6** - Trend Compared Response and Errors per URL implemented as Jenkins Staging Test Run 
            
 **7** - Compared Response and Errors to Previous Job Results per Request 
            for up to 5 provided Jenkins Test Run URLs
        
 **8** - Compared Response and Errors to Previous Job Results per Test 
            for up to 5 provided Jenkins Test Run URLs
        
 **9** - Trend Compared Response for limitless number of provided Jenkins Test Run URLs 
            and Errors to Previous Job Results per Request
        
 **10** - Trend Compared Response for limitless number of provided Jenkins Test Run URLs 
            and Errors to Previous Job Results per Test
        
 **11** - Trend Compared Responses and Deviations for exactly 2 provided URLs per Request
        
 **12** - Trend Compared Responses and Deviations for exactly 2 provided URLs per Test
        
        
## Data Type options:
        
 **1** - Use Average Response Time Data,
        
 **2** - Use Median Response Time Data,
        
 **3** - Use Min Response Time Data,
        
 **4** - Use Max Response Time Data,
        
 **5** - Use 90 Percentiles Response Time Data,
        
 **6** - Use 95 Percentiles Response Time Data,
        
 **7** - For Getting 99 Percentiles Response Time Data.
        
## Limitations:
   
*  If there isn't Previous Jenkins Test Run Previous Response Time will be invalid because it will be the same as Current Response Time,
*  Sheet Names, Request and Suite Title Graph Names are limited to 31 chars due to Excel limitations,
*  Request and Test Names shouldn't contain next chars: '[]:*?/\\'
*  In options 7 and 8 URL Number is limited to 5 due to excel graph limitations
*  In options 11 and 12 deviation is calculated between two provided Runs thus option is limited to 2 URLs
        
## Required Python and Libraries:
   
* Python 3.7, 3.8,
* pandas,
* requests,
* beautifulsoup4,
* lxml,
* XlxsWriter,
* vincent.
        
## Author

Sava Grkovic - [github](https://github.com/savagrk).

## License

This project is licensed under the [MIT license](/LICENSE).

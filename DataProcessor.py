'''
========================================================================================================================
 Interpreter: !/usr/local/bin/python
 Coding: utf-8
 Python Version: 3.7
 =======================================================================================================================
 File name: DataProcessor.py
 Author: Sava Grkovic
 Create Date: 17/9/2018
 Purpose: Runner for Jenkins Crawler with appropriate set of data
 =======================================================================================================================
 Last Modified: 11/4/2019
 Modified by: Sava Grkovic
========================================================================================================================
'''

# Import Section
from Core import JenkinsCrawler as Crawler
# Init Section
crawler = Crawler.JenkinsCrawler()


# Setup of Links for Crawling
crawler_urls = [
                #   APP1
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   APP 2
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                #   "http://jenkins.adress/view/project.name/job/job.name/lastBuild/performance/",
                ]

# Setup of Crawler Option
crawler_option = 1

# Setup of Threshold Value
threshold = 1

# Setup of Data Type
data_type = 1

"""
    Currently supported Crawler Options are:
        
        1 - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than Previous Job and Error Request Results in single Excel File
                
        2 - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than and Error Request Results in separate Excel Files
                
        3 - Responses over entered Threshold Results in single Excel File
            
        4 - Request Responses Better than Previous and Request Responses Worse than Previous Results in single Excel File
            
        5 - Error Requests Results in single Excel File
            
        6 - Compared Response and Deviation to Previous Job Results per Test Suite implemented as Jenkins Staging Test Run URLs
            
        7 - Compared Response and Deviation to Previous Job Results per Request for provided Jenkins Test Run URLs
        
        8 - Compared Response and Deviation to Previous Job Results per Test for provided Jenkins Test Run URLs
        
        9 - Trend Compared Response and Deviation to Previous Job Results per Request for provided Jenkins Test Run URLs
        
        10 - Trend Compared Response and Deviation to Previous Job Results per Test for provided Jenkins Test Run URLs
        
        11 - Trend Compared Responses and Deviations for Two provided URLs per Request
        
        12 - Trend Compared Responses and Deviations for Two provided URLs per Test
        
        
    Data Type options:
        
        1 - Use Average Response Time Data
        
        2 - Use Median Response Time Data
        
        3 - Use Min Response Time Data
        
        4 - Use Max Response Time Data
        
        5 - Use 90 Percentiles Response Time Data
        
        6 - Use 95 Percentiles Response Time Data
        
        7 - For Getting 99 Percentiles Response Time Data
        
    Limitations:
        - If there isn't Previous Jenkins Test Run Previous Response Time will be invalid because it will be the same as Current Response Time
        - Sheet Names, Request and Suite Title Graph Names are limited to 31 chars due to Excel limitations
        - Request and Test Names shouldn't contain next chars: '[]:*?/\\'
"""

# Crawler Command Line
crawler.jenkins_crawler(crawler_option, data_type, crawler_urls, threshold)


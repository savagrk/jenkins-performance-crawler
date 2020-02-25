'''
========================================================================================================================
 Interpreter: !/usr/local/bin/python
 Coding: utf-8
 Python Version: 3.7
 =======================================================================================================================
 File name: DataProcessor.py
 Author: Sava Grkovic
 Team: Integration QA
 Create Date: 17/9/2018
 Purpose: Runner for Jenkins Crawler with appropriate set of data
 =======================================================================================================================
 Last Modified: 30/1/2020
 Modified by: Sava Grkovic
========================================================================================================================
'''

# Import Section
from Core import JenkinsCrawler as Crawler
# Init Section
crawler = Crawler.JenkinsCrawler()

"""
    Currently supported Crawler Options are:

        1 - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than Previous Job and Error Request Results per single URL in single Excel File

        2 - Responses over entered Threshold, Request Responses Better than Previous Job, 
            Request Responses Worse than and Error Request Results per single URL in separate Excel Files

        3 - Responses over entered Threshold Results per single URL 
            in single Excel File

        4 - Request Responses Better than Previous and Request Responses Worse than Previous Results
            per single URL in single Excel File

        5 - Error Requests Results per single URL in single Excel File

        6 - Trend Compared Response and Errors to Previous Results per URL implemented as Jenkins Staging Test Run 

        7 - Compared Response and Errors to Previous Job Results per Request 
            for up to 5 provided Jenkins Test Run URLs

        8 - Compared Response and Errors to Previous Job Results per Test 
            for up to 5 provided Jenkins Test Run URLs

        9 - Trend Compared Response for limitless number of provided Jenkins Test Run URLs 
            and Errors to Previous Job Results per Request

        10 - Trend Compared Response for limitless number of provided Jenkins Test Run URLs 
            and Errors to Previous Job Results per Test

        11 - Trend Compared Responses and Deviations for exactly 2 provided URLs per Request

        12 - Trend Compared Responses and Deviations for exactly 2 provided URLs per Test


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
        - In options 7 and 8 URL Number is limited to 5 due to excel graph limitations
        - In options 11 and 12 deviation is calculated between two provided Runs thus option is limited to 2 URLs
"""


# Setup of Crawler Option
crawler_option = 10

# Setup of Threshold Value
threshold = 100

# Setup of Data Type
data_type = 1

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


# Crawler Command Line
crawler.jenkins_crawler(crawler_option, data_type, crawler_urls, threshold)


'''
========================================================================================================================
 Interpreter: !/usr/local/bin/python
 Coding: utf-8
 Python Version: 3.7
 =======================================================================================================================
 File name: JenkinsCrawler.py
 Author: Sava Grkovic
 Create Date: 17/9/2018
 Purpose: Definition of Jenkins Data Crawler options and functions
 =======================================================================================================================
 Last Modified: 11/4/2019
 Modified by: Sava Grkovic
========================================================================================================================
'''

from Core import DataParser as Parser
import xlsxwriter
import requests

parser = Parser.DataParser()


class JenkinsCrawler:

    def responses_over_entered_threshold(self, urls, threshold, data_type):

        i = 1
        for url in urls:
            suite_title, titles, tables = parser.url_parser(url)
            suite_title = "Suite#" + str(i) + " " + suite_title
            response_title, request, response, previous, deviation, rows = parser.response_above_threshold_parser(titles, tables, threshold, data_type)
            response_table, sheet_name = parser.response_results(response_title, request, response, previous, deviation, rows, threshold)
            parser.excel_table(response_table, sheet_name, suite_title + " - Response Time.xlsx", 1)
            i += 1

    def deviations_to_previous_build(self, urls, data_type):

        i = 1
        for url in urls:
            suite_title, titles, tables = parser.url_parser(url)
            suite_title = "Suite#" + str(i) + " " + suite_title
            deviation_title, worse_request, worse, worse_rows, better_request, better, better_rows = parser.deviation_parser(titles, tables, data_type)
            better_table, worse_table, sheet_name = parser.deviation_results(deviation_title, worse_request, worse, worse_rows, better_request, better, better_rows)
            parser.excel_two_tables(better_table, worse_table, sheet_name, suite_title + " - Deviations.xlsx", 1)
            i += 1

    def request_errors(self, urls):

        i = 1
        for url in urls:
            suite_title, titles, tables = parser.url_parser(url)
            suite_title = "Suite#" + str(i) + " " + suite_title
            errors_title, request, errors_percentage, errors_deviation, codes, old_codes, rows, flag = parser.errors_parser(titles, tables)
            errors_table, sheet_name = parser.errors_result(errors_title, request, errors_percentage, errors_deviation, codes, old_codes, rows, flag)
            parser.excel_table(errors_table, sheet_name, suite_title + " - Errors.xlsx")
            i += 1

    def responses_deviations_errors(self, urls, threshold, data_type):

        i = 1
        for url in urls:
            suite_title, titles, tables = parser.url_parser(url)
            suite_title = "Suite#" + str(i) + " " + suite_title
            response_title, request, response, previous, deviation, response_rows = parser.response_above_threshold_parser(titles, tables, threshold, data_type)
            response_table, response_sheet_name = parser.response_results(response_title, request, response, previous, deviation, response_rows, threshold)
            deviation_title, worse_request, worse, worse_rows, better_request, better, better_rows = parser.deviation_parser(titles, tables, data_type)
            better_table, worse_table, deviation_sheet_name = parser.deviation_results(deviation_title, worse_request, worse, worse_rows, better_request, better, better_rows)
            errors_title, request, errors_percentage, errors_deviation, codes, old_codes, errors_rows, flag = parser.errors_parser(titles, tables)
            errors_table, errors_sheet_name = parser.errors_result(errors_title, request, errors_percentage, errors_deviation, codes, old_codes, errors_rows, flag)
            if len(errors_sheet_name) is 1:
                errors_table = errors_table * len(response_sheet_name)
            parser.excel_four_tables(response_table, errors_table, better_table, worse_table, response_sheet_name, suite_title + ".xlsx", 1)
            i += 1

    def request_responses_stage_view(self, urls, threshold, data_type):

        i = 1
        for url in urls:
            sheet_name = []
            suite_title, titles, tables = parser.url_parser(url)
            suite_title = "Suite#" + str(i) + " " + suite_title
            sheet_name.append(suite_title[:31])
            request, response, previous, deviation, response_rows = parser.response_parser(tables, data_type)
            response_table, deviation_table = parser.response_by_request_stage_results(suite_title, titles, request, response, previous, deviation, response_rows, threshold)
            parser.excel_two_tables(response_table, deviation_table, sheet_name, suite_title + " - StageCompared.xlsx", 2)
            i += 1

    def request_responses_across_urls(self, urls, threshold, data_type):

        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.response_by_request_accross_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Builds - RequestsCompared.xlsx", 2)

    def test_responses_accross_urls(self, urls, threshold, data_type):

        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.response_by_test_accross_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Builds - TestCompared.xlsx", 2)

    def request_trend_responses_across_urls(self, urls, threshold, data_type):

        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.trend_response_by_request_accross_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Builds - TrendRequestsCompared.xlsx", 3)

    def test_trend_responses_accross_urls(self, urls, threshold, data_type):

        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.trend_response_by_test_accross_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Builds - TrendTestCompared.xlsx", 3)

    def request_trend_responses_two_urls(self, urls, threshold, data_type):

        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.trend_response_by_request_two_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Two Builds - TrendRequestsCompared.xlsx", 3)

    def test_trend_responses_two_urls(self, urls, threshold, data_type):
        suite_list, test_list, request_list, data = parser.urls_response_parser(urls, data_type)
        response_table, deviation_table, sheet_names = parser.trend_response_by_test_two_urls_results(suite_list, test_list, request_list, data, threshold)
        parser.excel_two_tables(response_table, deviation_table, sheet_names, "Jenkins Performance Two Builds - TrendTestCompared.xlsx", 3)

    def jenkins_crawler(self, option, data_type, urls, threshold):

        if not urls:
            print("\n\nURL list is empty! Please provide valid URLs!\n")
        else:
            try:
                if option is 1:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.responses_deviations_errors(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 2:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.responses_over_entered_threshold(urls, threshold, data_type)
                    self.deviations_to_previous_build(urls, data_type)
                    self.request_errors(urls)
                    print("\nData Parsing is finished!\n")

                elif option is 3:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.responses_over_entered_threshold(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 4:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.deviations_to_previous_build(urls, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 5:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.request_errors(urls)
                    print("\nData Parsing is finished!\n")

                elif option is 6:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.request_responses_stage_view(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 7:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.request_responses_across_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 8:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.test_responses_accross_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 9:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.request_trend_responses_across_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 10:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.test_trend_responses_accross_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 11:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.request_trend_responses_two_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                elif option is 12:
                    print("\nPlease wait, Crawler is Loading Data . . .\n")
                    self.test_trend_responses_two_urls(urls, threshold, data_type)
                    print("\nData Parsing is finished!\n")

                else:
                    print("\nPlease enter Valid Crawler option!!!\n")
                    print("Currently supported Crawler Options are:\n")
                    print("1 - Responses over entered Threshold, Request Responses Better then Previous Job, "
                          "Request Responses Worse then Previous Job and Error Request Results in single Excel File\n")
                    print("2 - Responses over entered Threshold, Request Responses Better then Previous Job, "
                          "Request Responses Worse then Previous Job and Error Request Results in separate Excel Files\n")
                    print("3 - Responses over entered Threshold Results in single Excel File\n")
                    print("4 - Request Responses Better then in Previous Job and "
                          "Request Responses Worse then in Previous Job Results in single Excel File\n")
                    print("5 - Error Requests Results in single Excel File\n")
                    print("6 - Compared Response and Deviation Results per Test Suite "
                          "implemented as Jenkins Staging Test Run URLs\n")
                    print("7 - Compared Response and Deviation to Previous Job Results per Request for provided Jenkins Test Run URLs\n")
                    print("8 - Compared Response and Deviation to Previous Job Results per Test for provided Jenkins Test Run URLs\n")
                    print("9 - Trend Compared Response and Deviation to Previous Job Results per Request for provided Jenkins Test Run URLs\n")
                    print("10 - Trend Compared Response and Deviation to Previous Job Results per Test for provided Jenkins Test Run URLs\n")
                    print("11 - Trend Compared Responses and Deviations for Two provided URLs per Request\n")
                    print("12 - Trend Compared Responses and Deviations for Two provided URLs per Test\n")
                    print("\n Limitations:\n")
                    print("    - If there isn't Previous Jenkins Test Run Previous Response Time will be invalid because it will be the same as Current Response Time")
                    print("    - Sheet Names, Request and Suite Title Graph Names are limited to 31 chars due to Excel limitations\n")
                    print("    - Request and Test Names shouldn't contain next chars: '[]:*?/\\'\n")

            except PermissionError:
                print("\nWARNING: PLEASE CLOSE ALL OPENED EXCEL FILES AND RERUN CRAWLER IN ORDER TO GET RESULTS IN EXCEL!!!\n")

            except AttributeError:
                print("\nWARNING: INVALID URL DICTIONARY!!! PLEASE CHECK PROVIDED URLS AND LIST FORMATTING!!!\n")

            except ValueError:
                print("\nWARNING: INVALID URLS PROVIDED!!! PLEASE ENTER JENKINS STAGING JOB URLS IF OPTION 6 IS USED!!!\n")

            except TypeError:
                print("\nWARNING: PLEASE USE PANDAS VERSION 23.4 OR LOWER DUE TO COMPATIBILITY OF FILE TYPES!!!\n")

            except xlsxwriter.exceptions.InvalidWorksheetName:
                print("\nWARNING: INVALID SHEET NAME PROVIDED!!! PLEASE DON'T USE '[]:*?/\\' CHARS FOR REQUEST AND TEST NAMES!!!")
                print("         REMOVE INVALID CHARS AND RERUN CRAWLER IN ORDER TO GET RESULTS IN EXCEL!!!\n")

            except requests.exceptions.ConnectionError:
                print("\nWARNING: URLS ARE UNAVAILABLE!!! PLEASE CHECK INTERNET CONNECTION!!!\n")

            except UnboundLocalError:
                print("\nPlease enter Valid Data Type option:\n")
                print("1 - For Getting Average Response Time Data\n")
                print("2 - For Getting Median Response Time Data\n")
                print("3 - For Getting Min Response Time Data\n")
                print("4 - For Getting Max Response Time Data\n")
                print("5 - For Getting 90 Percentiles Response Time Data\n")
                print("6 - For Getting 95 Percentiles Response Time Data\n")
                print("7 - For Getting 99 Percentiles Response Time Data\n")

            except KeyError:
                print("\nWARNING: REQUESTED DATA TYPE DOESN'T EXIST ON PROVIDED URLs!!!\n")

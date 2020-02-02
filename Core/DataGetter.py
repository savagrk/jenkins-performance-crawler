'''
========================================================================================================================
 Interpreter: !/usr/local/bin/python
 Coding: utf-8
 Python Version: 3.7
 =======================================================================================================================
 File name: DataGetter.py
 Author: Sava Grkovic
 Team: Integration QA
 Create Date: 17/9/2018
 Purpose: Getting specific Jenkins Performance Plugin data obtained by pandas lib
 =======================================================================================================================
 Last Modified: 30/1/2020
 Modified by: Sava Grkovic
========================================================================================================================
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup


class DataGetter:

    def url_getter(self, url):

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        titles = soup.find_all("h2")
        suite_title = self.suite_title(soup)
        test_titles = self.test_titles(titles)
        tables = pd.read_html(url, header=0, parse_dates=["URI"])

        return suite_title, test_titles, tables

    @staticmethod
    def suite_title(page):

        elements = page.find("ul", {"id": "breadcrumbs"})
        title = elements.find_all("li")[2].text

        return title

    @staticmethod
    def test_titles(titles):

        start = "Performance Breakdown by URI: "
        end = ".jtl"
        parsed_titles = []
        for title in titles:
            parsed_titles.append(str(title.contents)[str(title.contents).find(start) + len(start):str(title.contents).find(end)])

        return parsed_titles

    @staticmethod
    def request_name(table):

        request_name = table["URI"].tolist()

        return request_name

    @staticmethod
    def response_time_type(table, data_type):

        if data_type == 1:
            response = table["Average (ms)"].tolist()

        elif data_type == 2:
            response = table["Median(ms)"].tolist()

        elif data_type == 3:
            response = table["Min(ms)"].tolist()

        elif data_type == 4:
            response = table["Max(ms)"].tolist()

        elif data_type == 5:
            response = table["Line 90.0(ms)"].tolist()

        elif data_type == 6:
            response = table["Line 95.0(ms)"].tolist()

        elif data_type == 7:
            response = table["Line 99.0(ms)"].tolist()

        else:
            print("\nWARNING: INVALID DATA TYPE OPTION IS PROVIDED!!!\n")

        return response

    def response_time(self, table, data_type):

        response = self.response_time_type(table, data_type)
        response_time = []
        deviation = []
        for value in response:
            response_time.append(value.split('  ')[0])
            deviation.append(value.split('  ')[1])

        return response_time, deviation

    @staticmethod
    def http_codes(table):

        current = []
        compared = []
        http_codes = table["Http Code"].tolist()
        for codes in http_codes:
            code = str(codes).split("  ", 1)
            if len(code) == 2:
                current.append(code[0])
                compared.append(code[1])
            else:
                current.append(code[0])
                compared.append("No Past Errors")

        return current, compared

    @staticmethod
    def errors(table):

        current = []
        compared = []
        errors = table["Errors (%)"].tolist()
        for error in errors:
            string = str(error)
            current.append(string.split(' %  ')[0])
            compared.append(string.split('  ')[1])

        return current, compared

    @staticmethod
    def response_above_threshold(request_name, response_time, deviation_time, threshold):

        i = 0
        rows = 0
        request = []
        response = []
        previous = []
        deviation = []
        response_time = list(map(int, response_time))
        deviation_time = list(map(int, deviation_time))
        for time in response_time:
            if time > threshold:
                request.append(request_name[i])
                response.append(response_time[i])
                previous.append(response_time[i] - deviation_time[i])
                deviation.append(deviation_time[i])
                rows += 1
            i += 1

        return request, response, previous, deviation, rows

    @staticmethod
    def response_classification(request_name, response_time, deviation_time):

        i = 0
        rows = 0
        request = []
        response = []
        previous = []
        deviation = []
        response_time = list(map(int, response_time))
        deviation_time = list(map(int, deviation_time))
        for time in response_time:
            request.append(request_name[i])
            response.append(time)
            previous.append(response_time[i] - deviation_time[i])
            deviation.append(deviation_time[i])
            rows += 1
            i += 1

        return request, response, previous, deviation, rows

    @staticmethod
    def deviation_classification(request_name, deviation):

        i = 0
        worse_rows = 0
        better_rows = 0
        worse = []
        better = []
        worse_request = []
        better_request = []
        deviation = list(map(int, deviation))
        for dev in deviation:
            if dev > 0:
                worse_request.append(request_name[i])
                worse.append(deviation[i])
                worse_rows += 1
            else:
                better_request.append(request_name[i])
                better.append(deviation[i])
                better_rows += 1
            i += 1

        return worse_request, worse, worse_rows, better_request, better, better_rows

    @staticmethod
    def error_requests(request_name, current, compared, http_codes, old_codes):

        i = 0
        rows = 0
        request = []
        errors_percentage = []
        errors_deviation = []
        codes = []
        codes_old = []
        for percentage in current:
            if float(percentage) != 0.0:
                request.append(request_name[i])
                errors_percentage.append(percentage + " %")
                errors_deviation.append(compared[i])
                codes.append(http_codes[i])
                codes_old.append(old_codes[i])
                rows += 1
            i += 1

        return request, errors_percentage, errors_deviation, codes, codes_old, rows

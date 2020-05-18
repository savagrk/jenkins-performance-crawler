"""
========================================================================================================================
 Interpreter: !/usr/local/bin/python
 Coding: utf-8
 Python Version: 3.7
 =======================================================================================================================
 File name: DataParser.py
 Author: Sava Grkovic
 Create Date: 17/9/2018
 Purpose: Parsing of Jenkins Performance Plugin data obtained by pandas lib
 =======================================================================================================================
 Last Modified: 4/2/2020
 Modified by: Sava Grkovic
========================================================================================================================
"""

import pandas as pd
from Core import DataGetter as Core
from vincent.colors import brews

core = Core.DataGetter()


class DataParser:

    @staticmethod
    def url_parser(url):

        suite_title, test_titles, tables = core.url_getter(url)

        return suite_title, test_titles, tables

    def excel_table(self, df_list, sheet_list, file_name, plotting=0):

        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        for dataframe, sheet in zip(df_list, sheet_list):
            dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
            dfs = [dataframe]
            self.auto_align_excel_columns(writer, sheet, dfs)
            if plotting is 1:
                self.response_and_deviation_coloring(writer, sheet, dfs)
                self.response_with_deviation_plotting(writer, sheet, dfs)
                self.response_with_deviation_trend_plotting(writer, sheet, dfs)
        writer.save()

    def excel_two_tables(self, df_list1, df_list2, sheet_list, file_name, plotting=0):

        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        for dataframe1, dataframe2, sheet in zip(df_list1, df_list2, sheet_list):
            dataframe1.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
            dataframe2.to_excel(writer, sheet_name=sheet, startrow=len(dataframe1.index) + 3, startcol=0)
            dfs = [dataframe1, dataframe2]
            self.auto_align_excel_columns(writer, sheet, dfs)
            if plotting is 1:
                self.deviation_coloring(writer, sheet, dfs)
            elif plotting is 2:
                self.response_deviation_coloring(writer, sheet, dfs)
                self.response_plotting(writer, sheet, dfs)
            elif plotting is 3:
                self.response_deviation_coloring(writer, sheet, dfs)
                self.response_trend_plotting(writer, sheet, dfs)
        writer.save()

    def excel_four_tables(self, df_list1, df_list2, df_list3, df_list4, sheet_list, file_name, plotting=0):

        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        for dataframe1, dataframe2, dataframe3, dataframe4, sheet in zip(df_list1, df_list2, df_list3, df_list4, sheet_list):
            dataframe1.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
            dataframe2.to_excel(writer, sheet_name=sheet, startrow=len(dataframe1.index) + 3, startcol=0)
            dataframe3.to_excel(writer, sheet_name=sheet, startrow=len(dataframe1.index) + 3 + len(dataframe2.index) + 3, startcol=0)
            dataframe4.to_excel(writer, sheet_name=sheet, startrow=len(dataframe1.index) + 3 + len(dataframe2.index) + 3 + len(dataframe3.index) + 3, startcol=0)
            dfs = [dataframe1, dataframe2, dataframe3, dataframe4]
            self.auto_align_excel_columns(writer, sheet, dfs)
            if plotting is 1:
                self.all_response_deviation_coloring(writer, sheet, dfs)
                self.response_with_deviation_plotting(writer, sheet, dfs)
                self.response_with_deviation_trend_plotting(writer, sheet, dfs)
        writer.save()

    @staticmethod
    def auto_align_excel_columns(writer, sheet, dfs):

        width = []
        index = []
        workbook = writer.book
        centre_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        worksheet = writer.sheets[sheet]
        for df in dfs:
            for idx, col in enumerate(df):
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),
                    len(str(series.name)) + 2))
                width.append(max_len)
                index.append(idx)
        worksheet.set_column('A:XFD', max(width) + 2, centre_format)

    @staticmethod
    def response_and_deviation_coloring(writer, sheet, dfs):

        response_format = {'type': '3_color_scale',
                           'min_color': "#FBEA60",
                           'mid_color': "#FBB760",
                           'max_color': "#FB6060"}

        deviation_format = {'type': 'data_bar',
                            'bar_color': 'red',
                            'bar_border_color': 'white',
                            'bar_negative_color': 'green',
                            'bar_negative_border_color': 'white',
                            'bar_axis_position': 'middle',
                            'bar_axis_color': 'white'}

        worksheet = writer.sheets[sheet]
        dimension = dfs[0].shape
        last_row = 0
        if dimension[1] != 1:
            first_row = 1
            last_row = dimension[0] + 3
            response_col = 2
            previous_col = 3
            deviation_col = dimension[1]
            worksheet.conditional_format(first_row, response_col, last_row, response_col, response_format)
            worksheet.conditional_format(first_row, previous_col, last_row, response_col, response_format)
            worksheet.conditional_format(first_row, deviation_col, last_row, deviation_col, deviation_format)

        return last_row

    @staticmethod
    def deviation_coloring(writer, sheet, dfs, row_counter=0):

        deviation_format = {'type': 'data_bar',
                            'bar_color': 'red',
                            'bar_border_color': 'white',
                            'bar_negative_color': 'green',
                            'bar_negative_border_color': 'white',
                            'bar_axis_position': 'middle',
                            'bar_axis_color': 'white'}

        worksheet = writer.sheets[sheet]
        for df in dfs:
            dimension = df.shape
            if dimension[1] != 1:
                first_row = 1 + row_counter
                last_row = dimension[0] + row_counter
                deviation_col = dimension[1]
                worksheet.conditional_format(first_row, deviation_col, last_row, deviation_col, deviation_format)
                row_counter = last_row + 3
            else:
                last_row = dimension[0] + row_counter

    @staticmethod
    def response_deviation_coloring(writer, sheet, dfs):

        response_format = {'type': '3_color_scale',
                           'min_color': "#FBEA60",
                           'mid_color': "#FBB760",
                           'max_color': "#FB6060"}

        deviation_format = {'type': 'data_bar',
                            'bar_color': 'red',
                            'bar_border_color': 'white',
                            'bar_negative_color': 'green',
                            'bar_negative_border_color': 'white',
                            'bar_axis_position': 'middle',
                            'bar_axis_color': 'white'}

        worksheet = writer.sheets[sheet]
        dimension = dfs[0].shape
        if dimension[1] != 1:
            first_row = 1
            last_row = dimension[0]
            last_col = dimension[1]
            for result_col in range(2, last_col + 1):
                worksheet.conditional_format(first_row, result_col, last_row, result_col, response_format)
        else:
            last_row = 1

        dimension = dfs[1].shape
        if dimension[1] != 1:
            first_row = last_row + 3
            last_row = first_row + dimension[0]
            last_col = dimension[1]
            for result_col in range(2, last_col + 1):
                worksheet.conditional_format(first_row, result_col, last_row, result_col, deviation_format)

    def all_response_deviation_coloring(self, writer, sheet, dfs):

        dimension = dfs[1].shape
        last_row = self.response_and_deviation_coloring(writer, sheet, dfs) + dimension[0] + 3
        df = [dfs[2], dfs[3]]
        self.deviation_coloring(writer, sheet, df, last_row)

    @staticmethod
    def response_plotting(writer, sheet, dfs):

        workbook = writer.book
        worksheet = writer.sheets[sheet]

        dimension = dfs[0].shape
        if dimension[1] != 1:
            first_row = 1
            first_col = 2
            last_row = dimension[0]
            last_col = dimension[1]
            column_chart = workbook.add_chart({'type': 'column'})
            result_col = first_col
            while result_col <= last_col:
                column_chart.add_series({
                    'name': [sheet, 0, result_col],
                    'categories': [sheet, first_row, 1, last_row, 1],
                    'values': [sheet, first_row, result_col, last_row, result_col],
                    'fill': {'color': brews['Spectral'][result_col - 1]},
                    'border': {'color': 'black'},
                    'gap': 300,
                })
                result_col += 1

            column_chart.set_y_axis({
                'major_gridlines': {
                    'visible': True,
                    'line': {'width': 0.5, 'dash_type': 'dash'}
                },
            })

            column_chart.set_title({'name': sheet})
            column_chart.set_size({'x_scale': 3, 'y_scale': 2.5})
            column_chart.set_legend({'position': 'bottom'})
            column_chart.set_x_axis({'name': list(dfs[0])[0]})
            column_chart.set_y_axis({'name': 'Average Response Time (ms)'})
            worksheet.insert_chart(last_row + dfs[1].shape[0] + 6, 0, column_chart, {'x_offset': 75, 'y_offset': 10})

    @staticmethod
    def response_trend_plotting(writer, sheet, dfs):

        workbook = writer.book
        worksheet = writer.sheets[sheet]

        dimension = dfs[0].shape
        if dimension[1] != 1:
            first_col = 2
            last_row = dimension[0]
            last_col = dimension[1]
            line_chart = workbook.add_chart({'type': 'line'})
            result_row = 1
            while result_row <= last_row:
                line_chart.add_series({
                    'name': [sheet, result_row, 1],
                    'categories': [sheet, 0, first_col, 0, last_col],
                    'values': [sheet, result_row, first_col, result_row, last_col],
                    'marker': {'type': 'circle', 'size': 8},
                })
                result_row += 1

            line_chart.set_title({'name': 'Performance Trends per Test Run'})
            line_chart.set_size({'x_scale': 3, 'y_scale': 2.5})
            line_chart.set_legend({'position': 'bottom'})
            line_chart.set_x_axis({'name': 'Test Run'})
            line_chart.set_y_axis({'name': 'Average Response Time (ms)'})
            worksheet.insert_chart(last_row + dfs[1].shape[0] + 6, 0, line_chart, {'x_offset': 75, 'y_offset': 10})

    @staticmethod
    def response_with_deviation_plotting(writer, sheet, dfs):

        workbook = writer.book
        worksheet = writer.sheets[sheet]

        dimension = dfs[0].shape
        try:
            second = dfs[1].shape
            try:
                third = dfs[2].shape
            except:
                third = (0, -1)
        except:
            second = (0, -1)
            third = (0, -1)

        if dimension[1] != 1:
            first_row = 1
            first_col = 2
            last_row = dimension[0]
            last_col = dimension[1] - 1
            column_chart = workbook.add_chart({'type': 'column'})
            result_col = first_col
            while result_col <= last_col:
                column_chart.add_series({
                    'name': [sheet, 0, result_col],
                    'categories': [sheet, first_row, 1, last_row, 1],
                    'values': [sheet, first_row, result_col, last_row, result_col],
                    'border': {'color': 'black'},
                    'gap': 300,
                })
                result_col += 1

            column_chart.set_y_axis({
                'major_gridlines': {
                    'visible': True,
                    'line': {'width': 0.5, 'dash_type': 'dash'}
                },
            })

            last_second_col = third[1] + 1
            column_chart.set_title({'name': sheet})
            column_chart.set_size({'x_scale': 3, 'y_scale': 2.5})
            column_chart.set_legend({'position': 'bottom'})
            column_chart.set_x_axis({'name': list(dfs[0])[0]})
            column_chart.set_y_axis({'name': 'Average Response Time (ms)'})
            worksheet.insert_chart(last_row + second[0] + 5, last_second_col, column_chart, {'x_offset': 75, 'y_offset': 10})

    @staticmethod
    def response_with_deviation_trend_plotting(writer, sheet, dfs):

        workbook = writer.book
        worksheet = writer.sheets[sheet]

        dimension = dfs[0].shape
        try:
            second = dfs[1].shape
            try:
                third = dfs[2].shape
            except:
                third = (0, -1)
        except:
            second = (0, -1)
            third = (0, -1)

        if dimension[1] != 1:
            first_col = 2
            last_row = dimension[0]
            last_col = dimension[1] - 1
            line_chart = workbook.add_chart({'type': 'line'})
            result_row = 1
            while result_row <= last_row:
                line_chart.add_series({
                    'name': [sheet, result_row, 1],
                    'categories': [sheet, 0, first_col, 0, last_col],
                    'values': [sheet, result_row, first_col, result_row, last_col],
                    'marker': {'type': 'circle', 'size': 8},
                })
                result_row += 1


            last_second_col = third[1] + 1
            line_chart.set_title({'name': 'Performance Trends per Test Run'})
            line_chart.set_size({'x_scale': 3, 'y_scale': 2.5})
            line_chart.set_legend({'position': 'bottom'})
            line_chart.set_x_axis({'name': 'Test Run'})
            line_chart.set_y_axis({'name': 'Average Response Time (ms)'})
            worksheet.insert_chart(last_row + second[0] + 44, last_second_col, line_chart, {'x_offset': 75, 'y_offset': 10})

    @staticmethod
    def response_above_threshold_parser(titles, tables, threshold, data_type):

        i = 0
        title = []
        request = []
        response = []
        previous = []
        deviation = []
        rows = []
        for table in tables:
            request_name = core.request_name(table)
            response_time, deviation_int = core.response_time(table, data_type)
            request_part, response_part, previous_part, deviation_part, rows_part = core.response_above_threshold(request_name,
                                                                                                                  response_time,
                                                                                                                  deviation_int,
                                                                                                                  threshold)
            title.append(titles[i])
            request.append(request_part)
            response.append(response_part)
            previous.append(previous_part)
            deviation.append(deviation_part)
            rows.append(rows_part)
            i += 1

        return title, request, response, previous, deviation, rows

    @staticmethod
    def response_results(titles, request, responses, previous, deviation, rows, threshold):

        i = 0
        table = []
        sheet_name = []
        for title in titles:
            print("\n")
            print("Test Name: " + title)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")
            if not request[i]:
                print("!!! All Requests are within the Expected Response Time !!!\n")
                df = pd.DataFrame({"Results": "☺ All Requests are within the Expected Response Time ☺"},
                                  index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
                table.append(df)
                sheet_name.append(title[:31])
            else:
                df = pd.DataFrame({"Request Name": request[i],
                                   "Previous ResponseTime(ms)": previous[i],
                                   "Current ResponseTime(ms)": responses[i],
                                   "Deviation(ms)": deviation[i]},
                                  index=pd.Index(range(1, rows[i] + 1, 1), name="Responses over " + str(threshold) + " ms"))

                print(df.to_string() + "\n")
                table.append(df)
                sheet_name.append(title[:31])
            i += 1

        return table, sheet_name

    @staticmethod
    def deviation_parser(titles, tables, data_type):

        i = 0
        worse_rows = []
        better_rows = []
        worse = []
        better = []
        title = []
        worse_request = []
        better_request = []
        for table in tables:
            request_name = core.request_name(table)
            response_time, deviation = core.response_time(table, data_type)
            worse_request_part, worse_part, worse_rows_part, better_request_part, better_part, better_rows_part = core.deviation_classification(request_name, deviation)

            worse_request.append(worse_request_part)
            worse.append(worse_part)
            worse_rows.append(worse_rows_part)
            better_request.append(better_request_part)
            better.append(better_part)
            better_rows.append(better_rows_part)
            title.append(titles[i])
            i += 1

        return title, worse_request, worse, worse_rows, better_request, better, better_rows

    @staticmethod
    def deviation_results(titles, worse_requests, worse, worse_rows, better_requests, better, better_rows):

        i = 0
        table1 = []
        table2 = []
        sheet_name = []
        for title in titles:
            print("\n")
            print("Test Name: " + title)
            print("---------------------------------------------------------------------------------------------------")
            if not better[i]:
                print("Response Times Worse than in the Previous Build:\n")
                print("☹ No Requests with Better Response Times ☹\n")
                df1 = pd.DataFrame({"Results": "☹ No Requests with Better Response Times ☹"},
                                   index=pd.Index(range(1, 2, 1), name="Better Requests"))
                table1.append(df1)
            else:
                print("Response Times the Same or Better than in the Previous Build:\n")
                df1 = pd.DataFrame({"Request Name": better_requests[i],
                                    "Deviation(ms)": better[i]},
                                   index=pd.Index(range(1, better_rows[i] + 1, 1), name="Same or Better Response Times"))
                print(df1.to_string() + "\n")
                table1.append(df1)

            if not worse[i]:
                print("Response Times Worse than in the Previous Build:\n")
                print("☺ No Requests with Worse Response Times ☺\n")
                df2 = pd.DataFrame({"Results": "☺ No Requests with Worse Response Times ☺"},
                                   index=pd.Index(range(1, 2, 1), name="Worse Requests"))
                table2.append(df2)

            else:
                print("Response Times Worse than in the Previous Build:\n")
                df2 = pd.DataFrame({"Request Name": worse_requests[i],
                                    "Deviation(ms)": worse[i]},
                                   index=pd.Index(range(1, worse_rows[i] + 1, 1), name="Worse Response Times"))
                print(df2.to_string() + "\n")
                table2.append(df2)
            sheet_name.append(title[:31])
            i += 1

        return table1, table2, sheet_name

    @staticmethod
    def errors_parser(titles, tables):

        i = 0
        rows = []
        request = []
        errors_percentage = []
        errors_deviation = []
        codes = []
        codes_old = []
        title = []
        flag = []
        for table in tables:
            request_name = core.request_name(table)
            http_codes, old_codes = core.http_codes(table)
            current, compared = core.errors(table)
            request_part, errors_percentage_part, errors_deviation_part, codes_part, old_codes_part, rows_part = core.error_requests(request_name, current, compared, http_codes, old_codes)

            if request_part:
                request.append(request_part)
                errors_percentage.append(errors_percentage_part)
                errors_deviation.append(errors_deviation_part)
                codes.append(codes_part)
                codes_old.append(old_codes_part)
                rows.append(rows_part)
                title.append(titles[i])
                flag.append(1)
            else:
                request.append("No Problematical Requests")
                errors_percentage.append("No Errors")
                errors_deviation.append("No Error Deviation")
                codes.append("No HTTP Codes")
                codes_old.append("No Old HTTP Codes")
                rows.append(1)
                title.append(titles[i])
            i += 1

        return title, request, errors_percentage, errors_deviation, codes, codes_old, rows, flag

    @staticmethod
    def errors_result(titles, error_requests, errors_percentage, errors_deviation, codes, old_codes, rows, flag):

        table = []
        sheet_name = []
        if not flag:
            print("\n")
            print("☺ No Test with Request Errors in Entire Suite ☺\n")
            df = pd.DataFrame({"Error Requests": "☺ No Test with Request Errors in Entire Suite ☺",
                               "Number Suite Tests": len(titles)},
                              index=pd.Index(range(1, 2, 1), name="Errors"))
            table.append(df)
            sheet_name.append("Suite Has No Errors")
        else:
            i = 0
            for title in titles:
                print("\n")
                print("Test Name: " + title)
                print("-----------------------------------------------------------------------------------------------")
                print("Requests with Errors:\n")
                df = pd.DataFrame({"ErrorRequests": error_requests[i],
                                   "ErrorPercentage": errors_percentage[i],
                                   "CurrentCodes": codes[i],
                                   "ErrorDeviation": errors_deviation[i],
                                   "PreviousCodes": old_codes[i]},
                                  index=pd.Index(range(1, rows[i] + 1, 1), name="Errors"))
                print(df.to_string() + "\n")
                i += 1
                table.append(df)
                sheet_name.append(title[:31])

        return table, sheet_name

    @staticmethod
    def response_parser(tables, data_type):

        i = 0
        request = []
        response = []
        previous = []
        deviation = []
        error_percentage = []
        rows = []
        for table in tables:
            request_name = core.request_name(table)
            response_time, deviation_int = core.response_time(table, data_type)
            current, compared = core.errors(table)
            request_part, response_part, previous_part, deviation_part, percentage, rows_part = core.response_classification(request_name, response_time, deviation_int, current)

            request.append(request_part)
            response.append(response_part)
            previous.append(previous_part)
            deviation.append(deviation_part)
            error_percentage.append(percentage)
            rows.append(rows_part)
            i += 1

        return request, response, previous, deviation, error_percentage, rows

    @staticmethod
    def response_by_request_stage_results(suite_title, titles, request, responses, error_percentage, rows, threshold):

        response_table = []
        errors_table = []
        dict_response = {}
        dict_errors = {}
        print("\n")
        print("SuiteName: " + suite_title)
        print("---------------------------------------------------------------------------------------------------")
        print("Response Times over " + str(threshold) + " ms:\n")

        i = 0
        for title in titles:
            dict_response['Request Name'] = request[i]
            dict_response[title] = responses[i]
            dict_errors['Request Name'] = request[i]
            dict_errors[title] = error_percentage[i]
            i += 1

        df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, max(rows) + 1, 1), name="Responses over " + str(threshold) + " ms"))

        df1 = df1[df1[df1 > threshold].count(axis=1) > 1]
        if df1.empty:
            print("☺ All Requests are within the Expected Response Time in " + suite_title + "!!! ☺\n\n")
            df1 = pd.DataFrame({"Results": "☺ All Requests are within the Expected Response Time in " + suite_title + "!!! ☺"},
                               index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))

        df2 = pd.DataFrame(dict_errors, index=pd.Index(range(1, max(rows) + 1, 1), name="Errors Percentage [%]"))

        print(df1.to_string() + "\n\n")
        print("Errors in %:\n")
        print(df2.to_string() + "\n")
        response_table.append(df1)
        errors_table.append(df2)

        return response_table, errors_table

    def urls_response_parser(self, urls, data_type):

        i = 1
        data = []
        suite_list = []
        test_list = []
        request_list = []
        for url in urls:
            suite_title, titles, tables = self.url_parser(url)
            suite_title = "Suite#" + str(i) + ": " + suite_title
            suite_requests, suite_responses, suite_previous, suite_deviations, suite_error_percentages, old_row = self.response_parser(tables, data_type)
            for title, requests, responses, previous, deviations, errors in zip(titles, suite_requests, suite_responses, suite_previous, suite_deviations, suite_error_percentages):
                for request, response, prev, deviation, error in zip(requests, responses, previous, deviations, errors):
                    dictionary = {}
                    if request != 'All URIs':
                        dictionary['SuiteName'] = suite_title
                        dictionary['Test Name'] = title
                        dictionary['Request Name'] = request
                        dictionary['PreviousTime'] = prev
                        dictionary['ResponseTime'] = response
                        dictionary['Deviation'] = deviation
                        dictionary['Errors'] = error
                        data.append(dictionary)
                        request_list.append(request)
                test_list.append(title)
            suite_list.append(suite_title)
            i += 1

        data = sorted(data, key=lambda k: k['Request Name'])
        request_list = list(set(request_list))
        request_list.sort()
        test_list = list(set(test_list))
        test_list.sort()

        return suite_list, test_list, request_list, data

    @staticmethod
    def response_by_request_across_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        errors_table = []
        for request in request_list:
            response_dfs = []
            previous_dfs = []
            errors_dfs = []
            for suite in suite_list:
                rows = 0
                tests = []
                dict_response = {}
                dict_previous = {}
                dict_errors = {}
                response_list = []
                previous_list = []
                errors_list = []
                for test in test_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            tests.append(dictionary['Test Name'])
                            previous_list.append(dictionary['PreviousTime'])
                            response_list.append(dictionary['ResponseTime'])
                            errors_list.append(dictionary['Errors'])
                            rows += 1

                dict_previous['Test Name'] = tests
                dict_previous[suite + " - Previous Build"] = previous_list
                dict_response['Test Name'] = tests
                dict_response[suite + " - Current Build"] = response_list
                dict_errors['Test Name'] = tests
                dict_errors[suite] = errors_list

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df2 = pd.DataFrame(dict_previous, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                previous_dfs.append(df2)
                df3 = pd.DataFrame(dict_errors, index=pd.Index(range(1, rows + 1, 1), name="Errors Percentage [%]"))
                errors_dfs.append(df3)

            i = 0
            for response, previous, error in zip(response_dfs, previous_dfs, errors_dfs):
                if i == 0:
                    response_df = pd.merge(previous, response, how='outer', on='Test Name')
                    errors_df = error
                else:
                    response_df = pd.merge(response_df, previous, how='outer', on='Test Name')
                    response_df = pd.merge(response_df, response, how='outer', on='Test Name')
                    errors_df = pd.merge(errors_df, error, how='outer', on='Test Name')
                i += 1

            print("\n")
            print("Request Name: " + request)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Errors in %:\n")
            errors_df.index.names = ["Errors Percentage [%]"]
            print(errors_df.to_string() + "\n")

            response_table.append(response_df)
            errors_table.append(errors_df)
            sheet_names.append(request[:31])

        return response_table, errors_table, sheet_names

    @staticmethod
    def response_by_test_across_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        errors_table = []
        for test in test_list:
            response_dfs = []
            previous_dfs = []
            errors_dfs = []
            for suite in suite_list:
                rows = 0
                requests = []
                dict_response = {}
                dict_previous = {}
                dict_errors = {}
                response_list = []
                previous_list = []
                errors_list = []
                for request in request_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            requests.append(dictionary['Request Name'])
                            previous_list.append(dictionary['PreviousTime'])
                            response_list.append(dictionary['ResponseTime'])
                            errors_list.append(dictionary['Errors'])
                            rows += 1

                dict_previous['Request Name'] = requests
                dict_previous[suite + " - Previous Build"] = previous_list
                dict_response['Request Name'] = requests
                dict_response[suite + " - Current Build"] = response_list
                dict_errors['Request Name'] = requests
                dict_errors[suite] = errors_list

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df2 = pd.DataFrame(dict_previous, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                previous_dfs.append(df2)
                df3 = pd.DataFrame(dict_errors, index=pd.Index(range(1, rows + 1, 1), name="Errors Percentage [%]"))
                errors_dfs.append(df3)

            i = 0
            for response, previous, error in zip(response_dfs, previous_dfs, errors_dfs):
                if i == 0:
                    response_df = pd.merge(previous, response, how='outer', on='Request Name')
                    errors_df = error
                else:
                    response_df = pd.merge(response_df, previous, how='outer', on='Request Name')
                    response_df = pd.merge(response_df, response, how='outer', on='Request Name')
                    errors_df = pd.merge(errors_df, error, how='outer', on='Request Name')
                i += 1

            print("\n")
            print("Test Name: " + test)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Errors in %:\n")
            errors_df.index.names = ["Errors Percentage [%]"]
            print(errors_df.to_string() + "\n")

            response_table.append(response_df)
            errors_table.append(errors_df)
            sheet_names.append(test[:31])

        return response_table, errors_table, sheet_names

    @staticmethod
    def trend_response_by_request_across_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        errors_table = []
        for request in request_list:
            response_dfs = []
            errors_dfs = []
            for suite in suite_list:
                rows = 0
                tests = []
                dict_response = {}
                dict_errors = {}
                response_list = []
                errors_list = []
                for test in test_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            tests.append(dictionary['Test Name'])
                            response_list.append(dictionary['ResponseTime'])
                            errors_list.append(dictionary['Errors'])
                            rows += 1

                dict_response['Test Name'] = tests
                dict_response[suite] = response_list
                dict_errors['Test Name'] = tests
                dict_errors[suite] = errors_list

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df3 = pd.DataFrame(dict_errors, index=pd.Index(range(1, rows + 1, 1), name="Errors Percentage [%]"))
                errors_dfs.append(df3)

            i = 0
            for response, error in zip(response_dfs, errors_dfs):
                if i == 0:
                    response_df = response
                    errors_df = error
                else:
                    response_df = pd.merge(response_df, response, how='outer', on='Test Name')
                    errors_df = pd.merge(errors_df, error, how='outer', on='Test Name')
                i += 1

            print("\n")
            print("Request Name: " + request)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Errors in %:\n")
            errors_df.index.names = ["Errors Percentage [%]"]
            print(errors_df.to_string() + "\n")

            response_table.append(response_df)
            errors_table.append(errors_df)
            sheet_names.append(request[:31])

        return response_table, errors_table, sheet_names

    @staticmethod
    def trend_response_by_test_across_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        errors_table = []
        for test in test_list:
            response_dfs = []
            errors_dfs = []
            for suite in suite_list:
                rows = 0
                requests = []
                dict_response = {}
                dict_errors = {}
                response_list = []
                errors_list = []
                for request in request_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            requests.append(dictionary['Request Name'])
                            response_list.append(dictionary['ResponseTime'])
                            errors_list.append(dictionary['Errors'])
                            rows += 1

                dict_response['Request Name'] = requests
                dict_response[suite] = response_list
                dict_errors['Request Name'] = requests
                dict_errors[suite] = errors_list

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df3 = pd.DataFrame(dict_errors, index=pd.Index(range(1, rows + 1, 1), name="Errors Percentage [%]"))
                errors_dfs.append(df3)

            i = 0
            for response, error in zip(response_dfs, errors_dfs):
                if i == 0:
                    response_df = response
                    errors_df = error
                else:
                    response_df = pd.merge(response_df, response, how='outer', on='Request Name')
                    errors_df = pd.merge(errors_df, error, how='outer', on='Request Name')
                i += 1

            print("\n")
            print("Test Name: " + test)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Errors in %:\n")
            errors_df.index.names = ["Errors Percentage [%]"]
            print(errors_df.to_string() + "\n")

            response_table.append(response_df)
            errors_table.append(errors_df)
            sheet_names.append(test[:31])

        return response_table, errors_table, sheet_names

    @staticmethod
    def trend_response_by_test_two_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        deviation_table = []
        for test in test_list:
            response_dfs = []
            deviation_dfs = []
            for suite in suite_list:
                rows = 0
                requests = []
                dict_response = {}
                dict_deviation = {}
                response_list = []
                for request in request_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            requests.append(dictionary['Request Name'])
                            response_list.append(dictionary['ResponseTime'])
                            rows += 1

                dict_response['Request Name'] = requests
                dict_response[suite] = response_list
                dict_deviation['Request Name'] = requests

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df3 = pd.DataFrame(dict_deviation, index=pd.Index(range(1, rows + 1, 1), name="Deviations [ms]"))
                deviation_dfs.append(df3)

            i = 0
            for response, deviation in zip(response_dfs, deviation_dfs):
                if i == 0:
                    response_df = response
                    deviation_df = deviation
                elif i == 1:
                    response_df = pd.merge(response_df, response, how='outer', on='Request Name')
                    deviation_df = pd.merge(deviation_df, deviation, how='outer', on='Request Name')
                else:
                    print("Option could work only with TWO URLS")
                    break
                i += 1

            deviation_df['Deviations of Suite#1 to Suite#2'] = response_df[str(suite_list[0])] - response_df[str(suite_list[1])]

            print("\n")
            print("Test Name: " + test)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Requests are within the Expected Response Time for Test: " + test + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Deviations in ms:\n")
            deviation_df.index.names = ["Deviations [ms]"]
            print(deviation_df.to_string() + "\n")

            response_table.append(response_df)
            deviation_table.append(deviation_df)
            sheet_names.append(test[:31])

        return response_table, deviation_table, sheet_names

    @staticmethod
    def trend_response_by_request_two_urls_results(suite_list, test_list, request_list, data, threshold):

        sheet_names = []
        response_table = []
        deviation_table = []
        for request in request_list:
            response_dfs = []
            deviation_dfs = []
            for suite in suite_list:
                rows = 0
                tests = []
                dict_response = {}
                dict_deviation = {}
                response_list = []
                deviation_list = []
                for test in test_list:
                    for dictionary in data:
                        if dictionary['Request Name'] == request and dictionary['Test Name'] == test and dictionary['SuiteName'] == suite:
                            tests.append(dictionary['Test Name'])
                            response_list.append(dictionary['ResponseTime'])
                            deviation_list.append(dictionary['Deviation'])
                            rows += 1

                dict_response['Test Name'] = tests
                dict_response[suite] = response_list
                dict_deviation['Test Name'] = tests

                df1 = pd.DataFrame(dict_response, index=pd.Index(range(1, rows + 1, 1), name="Responses over " + str(threshold) + " ms"))
                response_dfs.append(df1)
                df3 = pd.DataFrame(dict_deviation, index=pd.Index(range(1, rows + 1, 1), name="Deviations [ms]"))
                deviation_dfs.append(df3)

            i = 0
            for response, deviation in zip(response_dfs, deviation_dfs):
                if i == 0:
                    response_df = response
                    deviation_df = deviation
                elif i == 1:
                    response_df = pd.merge(response_df, response, how='outer', on='Test Name')
                    deviation_df = pd.merge(deviation_df, deviation, how='outer', on='Test Name')
                else:
                    print("Option could work only with TWO URLS")
                    break
                i += 1

            deviation_df['Deviations of Suite#1 to Suite#2'] = response_df[str(suite_list[0])] - response_df[str(suite_list[1])]

            print("\n")
            print("Request Name: " + request)
            print("---------------------------------------------------------------------------------------------------")
            print("Response Times over " + str(threshold) + " ms:\n")

            response_df.index.names = ["Responses over " + str(threshold) + " ms"]
            response_df = response_df[response_df[response_df > threshold].count(axis=1) > 1]
            if response_df.empty:
                print("☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺\n\n")
                response_df = pd.DataFrame({"Results": "☺ All Tests are within the Expected Response Time for Request: " + request + "!!! ☺"},
                                           index=pd.Index(range(1, 2, 1), name="Responses over " + str(threshold) + " ms"))
            print(response_df.to_string() + "\n\n")

            print("Deviations in ms:\n")
            deviation_df.index.names = ["Deviations [ms]"]
            print(deviation_df.to_string() + "\n")

            response_table.append(response_df)
            deviation_table.append(deviation_df)
            sheet_names.append(request[:31])

        return response_table, deviation_table, sheet_names

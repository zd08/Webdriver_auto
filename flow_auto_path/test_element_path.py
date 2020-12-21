from assert_data.assert_result import Assert
from error_screenshot.error_web_screenshot import Screenshoot_web
from flow_auto_path.local_element_path import Flow_element
from read_writer_excel.option_excel import *
import time
from log.Log import info
from openpyxl import load_workbook

from test_case_result.test_result_build import Test_result


class test_path:
    def __init__(self, driver):
        self.driver = driver
        self.FLow_element = Flow_element(self.driver)
        self.Readexcel_element_path = Readexcel_element_path()
        self.Readexcel_data = Readexcel_data()
        self.document_path = Document_path()
        self.element_path = self.document_path.read_element_path()  # 读取文档row值
        self.case_path = self.document_path.read_data_path()
        self.element_wb = load_workbook(self.element_path)
        self.case_wb = load_workbook(self.case_path)
        self.element_max = self.element_wb['Sheet1'].max_row
        self.case_max = self.case_wb['Sheet1'].max_row
        # print(self.element_max,self.case_max)
        self.element_option_run()
        # return self.driver

    def element_option_run(self):
        '''拿取数据执行'''
        success = 0
        fail_count = 0
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        time_s = time.time()
        table = []
        for element_row in range(2, self.element_max + 1):
            test_path_item = self.Readexcel_element_path.test_items(element_row)  # 执行功能项
            execute = self.Readexcel_element_path.elemen_execute(element_row)  # 是否执行
            if execute == 'N':
                continue
            elif execute == 'Y':
                for case_row in range(2, self.case_max + 1):
                    test_case_item = self.Readexcel_data.test_items(case_row)  # case功能项
                    if test_path_item == test_case_item:
                        table_1 = []
                        path = self.Readexcel_element_path.element_path(element_row)  # 拿取定位方法元素操作
                        data = self.Readexcel_data.test_data(case_row)  # 测试数据
                        test_order_number = self.Readexcel_data.test_order_number(case_row)
                        test_son_data = self.Readexcel_data.test_son_items(case_row)  # 测试子项
                        clear_data = self.Readexcel_data.clear_data(case_row)  # 是否清空输入框
                        assert_local_method = self.Readexcel_data.test_assert(case_row)  # 断言定位
                        assert_method = self.Readexcel_data.assert_method(case_row)  # 断言方法
                        assert_data = self.Readexcel_data.test_assert_data(case_row)  # 断言数据
                        except_result = self.Readexcel_data.test_except_result(case_row)  # 预期结果
                        a = 0
                        table_1.append(test_son_data)
                        table_1.append(test_order_number)
                        # print(data)
                        for i in path:
                            ele_path = i.split('%')
                            # print(ele_path)
                            if ele_path[0] in ['xpath', 'css', 'class', 'id', 'name']:
                                self.FLow_element.location(ele_path[0], ele_path[1])
                                if ele_path[2] == 'send_keys' and data != None:  # send_keys执行if，其它执行else
                                    if a == len(data):
                                        a = 0
                                    else:
                                        self.FLow_element.page_operation(send_operation=ele_path[2], data=data[a],
                                                                         clear_data=clear_data)
                                        a += 1
                                else:
                                    self.FLow_element.page_operation(send_operation=ele_path[2])
                            elif ele_path[0] == 'js':
                                pass
                            elif ele_path[0] == 'wb':
                                pass
                        time.sleep(1)
                        if assert_local_method[0] in ['xpath', 'css', 'class', 'id', 'name']:
                            self.FLow_element.location(assert_local_method[0], assert_local_method[1])

                        elif assert_local_method[0] == '图片':
                            pass
                        self.assert_data_ = self.FLow_element.page_operation(send_operation=assert_local_method[2])

                        try:
                            b = 0
                            for assert_methodi in assert_method:
                                Assert(self.assert_data_, assert_data[b], assert_methodi)
                                b += 1
                            success += 1
                            table_1.append("pass")
                            info("%s执行成功" % test_son_data)
                        except Exception as e:
                            assert_driver = self.FLow_element.return_driver()
                            screen = Screenshoot_web(assert_driver)
                            screen_path = screen.screenshoot()
                            fail_count += 1
                            table_1.append("fail")
                            table_1.append(screen_path.replace("\\", "/"))
                            info("%s执行失败" % test_son_data)
                        table.append(table_1)
        time_t = time.time()
        time_time = time_t - time_s
        count_time = time.strftime('%M:%S', time.localtime(time_time))
        # Test_result(count_time=count_time,success=success,fail_count=fail_count,start_time=start_time,table=table)
        self.FLow_element.return_driver().quit()
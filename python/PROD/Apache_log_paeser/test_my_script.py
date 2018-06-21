#!/usr/bin/env python
"""
тестирование скрипта apache_log_parser_split.py
с помощью unittest
внутри класса описаны функции
по результатам выполненя можно определить будет ли корректно обрабатывать
функция def dictify_logline(line) в скрипте apache_log_parser_split.py
при различных примерах представленных в функциях
"""
import unittest
import apache_log_parser_split


class TestApacheLogParser(unittest.TestCase):

    def setUp(self):
        pass

    def testCombinedExample(self):
        combined_log_entry = '127.0.0.1 - - [09/Mar/2004:13:14:53 -0800] "GET / HTTP/1.1" 200 2326'
        self.assertEquals(
            apache_log_parser_split.dictify_logline(combined_log_entry),
            {'remote_host': '127.0.0.1', 'status': '200', 'bytes_sent': '2326'})

    def testCommonExample(self):
        pass

    def testExtraWhitespace(self):
        pass

    def testMalformed(self):
        common_log_entry = 'jacksonproject.cnc.bc.ca - - [09/Mar/2004:14:50:23 -0800] "GET /mailman/listinfo HTTP/1.1" 200 6893'
        self.assertEqual(
            apache_log_parser_split.dictify_logline(common_log_entry),
            {'remote_host': 'jacksonproject.cnc.bc.ca', 'status': '200', 'bytes_sent': '6893'})

if __name__ == '__main__':
 unittest.main()


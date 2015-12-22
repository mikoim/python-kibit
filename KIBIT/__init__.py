# Kibit wrapper for Python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Eshin Kunishima <ek@retty.me>
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import csv
import json
import sys
import urllib.error
import urllib.request


__author__ = 'Eshin Kunishima'
__copyright__ = 'Copyright (c) 2015, Eshin Kunishima <ek@retty.me>'


class KIBIT:
    """
    KIBIT API Wrapper for Python 3.x

    >>> u = KIBIT('http://localhost/')
    """

    class _Stub:

        def post(self, base_url, path, body):
            """
            Send POST request with the specified body.
            :param base_url: the base url of API
            :param path: path part of the endpoint.
            :param body: message body
            :return: json returned by the server.
            """

            body_json = json.dumps(body)

            request = urllib.request.Request(
                    url='{:s}{:s}'.format(base_url, path),
                    data=body_json.encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
            )

            try:
                response = urllib.request.urlopen(request).read()
                return json.loads(response.decode('utf-8'))

            except urllib.error.HTTPError as e:
                self.__eprint(body_json)
                self.__eprint(e.read())

                raise e

        @staticmethod
        def __eprint(objects):
            """
            Print message to stderr
            :param objects: Something
            """

            print(objects, file=sys.stderr)

    _stub = _Stub()

    def __init__(self, base_url):
        csv.field_size_limit(sys.maxsize)  # field larger than field limit
        self.stub = KIBIT._stub
        self.base_url = base_url

    @staticmethod
    def __status(response):
        """
        Check if request is successful
        :param response: Response message
        :return: Return True if the request is successful
        """

        return response['result'] == 'success'

    def document(self, text, document_id, category_id):
        """
        Adds document to KIBIT.

        :param text: Text
        :param document_id: Document ID
        :param category_id: Category ID
        :return: Return True if this operation is successful

        >>> u = KIBIT('http://localhost/')
        >>> u.document('hoge', 1, 690)
        True
        >>> u.document('fuga', 2, 690)
        True
        """

        body = {
            'documentId': document_id,
            'categoryId': category_id,
            'text': text
        }

        return self.__status(
                self.stub.post(self.base_url,
                               'document_analyzer/api/document', body)
        )

    def teacher(
            self,
            teacher_id,
            relevant_ids,
            not_relevant_ids=None,
            category_id=1):
        """
        Define relationship between documents
        :param teacher_id: Teacher ID
        :param relevant_ids: Relevant document ID (list)
        :param not_relevant_ids: Non relevant document ID (list)
        :param category_id: Category ID
        :return: Return True if this operation is successful
        """

        if not_relevant_ids is None:
            not_relevant_ids = []

        body = {
            'teacherId': teacher_id,
            'documents': {
                'relevant': relevant_ids,
                'notRelevant': not_relevant_ids
            },
            'categoryId': category_id
        }

        return self.__status(
                self.stub.post(self.base_url,
                               'relevance_evaluator/api/teacher', body)
        )

    def result(
            self,
            teacher_id,
            category_id,
            offset=0,
            limit=100, target_document_ids=None):
        """
        Retrieve estimated result from KIBIT
        :param teacher_id: Teacher ID
        :param category_id: Category ID
        :param offset: Offset >= 0
        :param limit: Limit (Default 100)
        :param target_document_ids: Target documents ID (list)
        :return: Return True if this operation is successful
        """

        if target_document_ids is None:
            target_document_ids = []

        body = {
            'teacherId': teacher_id,
            'offset': offset,
            'limit': limit,
            'targetDocuments': target_document_ids,
            'categoryId': category_id
        }

        return self.stub.post(self.base_url,
                              'relevance_evaluator/api/leaningResult', body)

    def bulk(self, file, category_id):
        """
        Load data from CSV and add document to KIBIT
        :param file: File object
        :param category_id: Category ID

        :return list of return values of KIBIT#document

        >>> import io
        >>> u = KIBIT('http://localhost/')
        >>> u.bulk(io.StringIO('id,name,report_comment\\n1,test,hoge'), 1)
        [True]
        """

        csv_reader = csv.reader(file)
        next(csv_reader, None)

        vals = []
        for row in csv_reader:
            restaurant_id = int(row[0])
            report_comment = row[2]

            vals.append(
                    self.document(report_comment, restaurant_id, category_id)
            )
        return vals

if __name__ == '__main__':

    class FakeStub:
        def post(self, base_url, path, body):
            return json.loads('{"result": "success"}')
    KIBIT._stub = FakeStub()

    import doctest
    doctest.testmod()

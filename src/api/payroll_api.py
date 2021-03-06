import csv
import re
from io import StringIO
from typing import List

import inject
from flask import jsonify, request, make_response
from flask_restful import Resource

from src.service.payroll_service import PayrollService
from src.service.service_exceptions import TimeReportAlreadyExistsException


class PayrollApi(Resource):
    payroll_service = inject.instance(PayrollService)
    valid_time_report_regex = r"time-report-(\d+).csv"
    valid_time_report_regex_pattern = re.compile(valid_time_report_regex)
    invalid_file_format_message = "One or more file names are not following the predefined format"
    no_uploaded_files_message = "Upload at least one file"
    duplicated_report_message = "The uploaded time report already exists on the system"

    def get(self):
        full_report = {"employeeReports": self.payroll_service.get_employee_report()}
        return jsonify(payrollReport=full_report)

    def post(self):
        uploaded_files = request.files
        if len(uploaded_files) == 0:
            return make_response(f"{self.no_uploaded_files_message}", 400)

        valid, invalid_names = self._validate_uploaded_file_format([v.filename for k, v in uploaded_files.items()])
        if not valid:
            return make_response(f"{self.invalid_file_format_message}: {invalid_names}", 400)

        try:
            for k, v in uploaded_files.items():
                reader = csv.reader(StringIO(v.read().decode("utf-8")))
                rows = [row for row in reader]
                self.payroll_service.add_time_report(v.filename, rows[1:])
        except TimeReportAlreadyExistsException as e:
            return make_response(f"{self.duplicated_report_message}: {e.report_name}", 400)

    def _validate_uploaded_file_format(self, file_names: List[str]):
        invalid_file_names = []
        for name in file_names:
            if not self.valid_time_report_regex_pattern.match(name):
                invalid_file_names.append(name)

        return len(invalid_file_names) == 0, invalid_file_names

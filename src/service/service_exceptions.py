class TimeReportAlreadyExistsException(Exception):
    def __init__(self, report_name):
        self.report_name = report_name

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import inject

from src.repository.payroll_repository import PayrollRepository
from src.service.service_exceptions import TimeReportAlreadyExistsException


class PayrollService:
    payroll_repository = inject.instance(PayrollRepository)
    job_group_to_hourly_rate = {
        "A": 20,
        "B": 30
    }

    def get_employee_report(self):
        employee_payroll_entries = self.payroll_repository.get_employee_payroll_entries()
        employee_sum = {}
        for entry in employee_payroll_entries:
            if entry[3] not in employee_sum:
                employee_sum[entry[3]] = {}

            pay_period = self._date_to_pay_period(entry[1])
            if pay_period not in employee_sum[entry[3]]:
                employee_sum[entry[3]][pay_period] = 0

            employee_sum[entry[3]][pay_period] += entry[2] * self.job_group_to_hourly_rate[entry[4]]

        result = []
        for employee_id, entry in employee_sum.items():
            for pay_period, amount in entry.items():
                result.append(
                    {
                        "employeeId": employee_id,
                        "payPeriod": {
                            "startDate": pay_period[0],
                            "endDate": pay_period[1]
                        },
                        "amountPaid": f"${amount:.2f}"
                    }
                )

        # sorting ascending by employee_id and period_start
        result.sort(key=lambda row: (row["employeeId"], row["payPeriod"]["startDate"]))

        return result

    def add_time_report(self, time_report_name, time_report_header, time_report_content):
        if self.payroll_repository.get_time_report_by_name(time_report_name):
            raise TimeReportAlreadyExistsException(time_report_name)

        time_report_id = self.payroll_repository.add_time_report(time_report_name)

        self.payroll_repository.add_time_report_info(time_report_id, time_report_content)

    def _date_to_pay_period(self, date):
        curr = datetime.strptime(date, "%d/%m/%Y")
        if (curr.day // 16) == 0:
            period_start = curr.replace(day=((curr.day // 16) * 15) + 1)
            period_end = curr.replace(day=15)
        else:
            period_start = curr.replace(day=((curr.day // 16) * 16))
            period_end = (curr + relativedelta(months=1)).replace(day=1) + timedelta(days=-1)

        return period_start.strftime("%Y-%m-%d"), period_end.strftime("%Y-%m-%d")

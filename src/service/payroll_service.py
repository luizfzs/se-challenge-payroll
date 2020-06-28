from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import inject

from src.repository.payroll_repository import PayrollRepository


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
                        "amountPaid": f"${amount}"
                    }
                )

        print(result)
        return result

    def add_time_report(self, time_report_name, time_report_header, time_report_content):
        # ensure time_report_name is not duplicated
        # insert new time_report_name
        # insert report content
        pass

    def _date_to_pay_period(self, date):
        curr = datetime.strptime(date, "%Y-%m-%d")
        if (curr.day // 16) == 0:
            rounded_begin = curr.replace(day=((curr.day // 16) * 15) + 1)
            rounded_end = curr.replace(day=15)
        else:
            rounded_begin = curr.replace(day=((curr.day // 16) * 16))
            rounded_end = (curr + relativedelta(months=1)).replace(day=1) + timedelta(days=-1)

        return rounded_begin.strftime("%Y-%m-%d"), rounded_end.strftime("%Y-%m-%d")

from unittest.mock import patch

import inject
import pytest

from src.repository.payroll_repository import PayrollRepository
from src.service.payroll_service import PayrollService


@pytest.fixture(scope="function")
def service():
    yield inject.instance(PayrollService)


@patch.object(PayrollRepository, 'get_employee_payroll_entries')
def test_when_no_entries_return_empty(mock_get_employee_payroll_entries, service):
    mock_get_employee_payroll_entries.return_value = []

    result = service.get_employee_report()

    assert result is not None, result
    assert len(result) == 0, result


@patch.object(PayrollRepository, 'get_employee_payroll_entries')
def test_when_employee1_entries_exist_return_proper_data(mock_get_employee_payroll_entries, service):
    # (time_report_id, date, hours_worked, employee_id, job_group)
    employee1_entry1 = (1, "04/01/2020", 10, 1, "A")
    expected = [{'employeeId': 1, 'payPeriod': {'startDate': '2020-01-01', 'endDate': '2020-01-15'}, 'amountPaid': '$200.00'}]
    mock_get_employee_payroll_entries.return_value = [employee1_entry1]

    result = service.get_employee_report()

    assert result is not None, result
    assert sorted(expected) == sorted(result), result


@patch.object(PayrollRepository, 'get_employee_payroll_entries')
def test_when_employee1_entries_exist_return_proper_data2(mock_get_employee_payroll_entries, service):
    # (time_report_id, date, hours_worked, employee_id, job_group)
    employee1_entry1 = (1, "17/01/2020", 10, 1, "A")
    expected = [{'employeeId': 1, 'payPeriod': {'startDate': '2020-01-16', 'endDate': '2020-01-31'}, 'amountPaid': '$200.00'}]
    mock_get_employee_payroll_entries.return_value = [employee1_entry1]

    result = service.get_employee_report()

    assert result is not None, result
    assert sorted(expected) == sorted(result), result

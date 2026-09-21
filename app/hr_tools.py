employees = {
    "EMP001": {
        "name": "Rahul Sharma",
        "department": "Engineering",
        "role": "Software Engineer",
        "manager": "Anita Verma",
        "annual_leave_balance": 18,
        "sick_leave_balance": 10,
    },
    "EMP002": {
        "name": "Priya Singh",
        "department": "Human Resources",
        "role": "HR Executive",
        "manager": "Neha Kapoor",
        "annual_leave_balance": 20,
        "sick_leave_balance": 12,
    },
     "EMP003": {
        "name": "Tauqeer Hussain",
        "department": "Human Resources",
        "role": "HR Executive",
        "manager": "Neha Kapoor",
        "annual_leave_balance": 20,
        "sick_leave_balance": 12,
    },
    
}

hr_policies = {
    "annual_leave": {
        "title": "Annual Leave Policy",
        "description": "Confirmed employees receive 24 days of annual leave per year.",
    },
    "sick_leave": {
        "title": "Sick Leave Policy",
        "description": "Employees receive 12 days of sick leave per year.",
    },
    "carry_forward": {
        "title": "Leave Carry Forward Policy",
        "description": "Employees can carry forward a maximum of 10 unused annual leave days.",
    },
}


def get_employee_profile(employee_id):
    employee = employees.get(employee_id)

    if employee is None:
        return {
            "success": False,
            "message": "Employee not found.",
        }

    return {
        "success": True,
        "employee": employee,
    }


def get_employee_leave_balance(employee_id):
    employee = employees.get(employee_id)

    if employee is None:
        return {
            "success": False,
            "message": "Employee not found.",
        }

    return {
        "success": True,
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "annual_leave_balance": employee["annual_leave_balance"],
        "sick_leave_balance": employee["sick_leave_balance"],
    }


def get_hr_policy(policy_name):
    policy = hr_policies.get(policy_name)

    if policy is None:
        return {
            "success": False,
            "message": "HR policy not found.",
        }

    return {
        "success": True,
        "policy": policy,
    }
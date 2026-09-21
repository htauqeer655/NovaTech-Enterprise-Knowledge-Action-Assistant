from openai import OpenAI
from dotenv import load_dotenv
from app.tools import create_it_ticket, get_ticket, list_tickets
from app.hr_tools import (
    get_employee_profile,
    get_employee_leave_balance,
    get_hr_policy,
)
from app.notifications import send_pushover_notification
import json

load_dotenv()

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_it_ticket",
            "description": "Create a new IT support ticket for an employee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {
                        "type": "string",
                        "description": "The IT issue reported by the employee."
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority of the IT issue."
                    }
                },
                "required": ["issue", "priority"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket",
            "description": "Get the details and status of an existing IT support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ID of the IT ticket, for example IT-0001."
                    }
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tickets",
            "description": "List all IT support tickets.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_employee_profile",
            "description": "Get an employee's HR profile using their employee ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID such as EMP001."
                    }
                },
                "required": ["employee_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_employee_leave_balance",
            "description": "Get an employee's current annual and sick leave balance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID such as EMP001."
                    }
                },
                "required": ["employee_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hr_policy",
            "description": "Get a specific HR policy from the mock HR system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "policy_name": {
                        "type": "string",
                        "enum": [
                            "annual_leave",
                            "sick_leave",
                            "carry_forward"
                        ],
                        "description": "The HR policy to retrieve."
                    }
                },
                "required": ["policy_name"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are NovaTech's Enterprise Action Assistant.

IT tools:
- Use create_it_ticket when the user explicitly asks to create, raise, or open an IT ticket.
- Use get_ticket when the user asks about an existing IT ticket.
- Use list_tickets when the user asks to see all IT tickets.

HR tools:
- Use get_employee_profile when the user asks for employee profile or employee information.
- Use get_employee_leave_balance when the user asks about an employee's leave balance.
- Use get_hr_policy when the user asks about a specific HR policy.

Do not invent employee information.
Do not create an IT ticket unless the user explicitly asks you to create, raise, or open one.
"""


def run_agent(user_message):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        tools=tools,
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name

    arguments = json.loads(
        tool_call.function.arguments
    )

    if tool_name == "create_it_ticket":

        result = create_it_ticket(
            issue=arguments["issue"],
            priority=arguments["priority"]
        )

        notification_message = (
            f"New IT ticket created.\n"
            f"Ticket ID: {result['ticket_id']}\n"
            f"Issue: {result['issue']}\n"
            f"Priority: {result['priority']}\n"
            f"Status: {result['status']}"
        )

        notification_result = send_pushover_notification(
            notification_message,
            title="NovaTech IT Ticket"
        )

        if notification_result["success"]:
            notification_status = "Pushover notification sent."
        else:
            notification_status = "Ticket created, but Pushover notification failed."

        return (
            "IT ticket created successfully.\n"
            f"Ticket ID: {result['ticket_id']}\n"
            f"Issue: {result['issue']}\n"
            f"Priority: {result['priority']}\n"
            f"Status: {result['status']}\n"
            f"{notification_status}"
        )

    elif tool_name == "get_ticket":

        result = get_ticket(
            arguments["ticket_id"]
        )

        if result is None:
            return "I could not find that IT ticket."

        return (
            "Ticket found.\n"
            f"Ticket ID: {result['ticket_id']}\n"
            f"Issue: {result['issue']}\n"
            f"Priority: {result['priority']}\n"
            f"Status: {result['status']}"
        )

    elif tool_name == "list_tickets":

        results = list_tickets()

        if not results:
            return "There are no IT tickets."

        output = "IT tickets:\n"

        for ticket in results:
            output += (
                f"\nTicket ID: {ticket['ticket_id']}\n"
                f"Issue: {ticket['issue']}\n"
                f"Priority: {ticket['priority']}\n"
                f"Status: {ticket['status']}\n"
            )

        return output

    elif tool_name == "get_employee_profile":

        result = get_employee_profile(
            arguments["employee_id"]
        )

        if not result["success"]:
            return result["message"]

        employee = result["employee"]

        return (
            "Employee profile found.\n"
            f"Employee ID: {arguments['employee_id']}\n"
            f"Name: {employee['name']}\n"
            f"Department: {employee['department']}\n"
            f"Role: {employee['role']}\n"
            f"Manager: {employee['manager']}"
        )

    elif tool_name == "get_employee_leave_balance":

        result = get_employee_leave_balance(
            arguments["employee_id"]
        )

        if not result["success"]:
            return result["message"]

        return (
            "Leave balance found.\n"
            f"Employee: {result['employee_name']}\n"
            f"Annual leave balance: "
            f"{result['annual_leave_balance']} days\n"
            f"Sick leave balance: "
            f"{result['sick_leave_balance']} days"
        )

    elif tool_name == "get_hr_policy":

        result = get_hr_policy(
            arguments["policy_name"]
        )

        if not result["success"]:
            return result["message"]

        policy = result["policy"]

        return (
            f"{policy['title']}\n"
            f"{policy['description']}"
        )

    return "I could not complete that request."
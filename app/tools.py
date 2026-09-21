from app.database import get_connection, initialize_database

initialize_database()


def create_it_ticket(issue, priority="medium"):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tickets (
            ticket_id,
            issue,
            priority,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "PENDING",
            issue,
            priority,
            "Open",
        )
    )

    new_id = cursor.lastrowid

    ticket_id = f"IT-{new_id:04d}"

    cursor.execute(
        """
        UPDATE tickets
        SET ticket_id = ?
        WHERE id = ?
        """,
        (ticket_id, new_id)
    )

    connection.commit()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        WHERE id = ?
        """,
        (new_id,)
    )

    ticket = dict(
        cursor.fetchone()
    )

    connection.close()

    return ticket


def get_ticket(ticket_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def list_tickets():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]
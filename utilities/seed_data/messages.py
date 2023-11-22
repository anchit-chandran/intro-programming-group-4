from datetime import datetime, timedelta
from utilities.sqlite3_date_formatter import convert_to_sqlite3_datetime
import random

from constants.message_priorities import Priority

messages_data = []
# Add 5 messages for admin
for i in range(5):
    sent_at = convert_to_sqlite3_datetime(
            datetime.now() - timedelta(minutes=(i * 60))
        )

    new_msg = {

        "message": f"Hey there, I'm message {i}",
        "sent_at": sent_at,
        "urgency": random.choice(list(Priority)).value,
        "is_resolved": random.choice([True, False]),
        "sender_id": 1,
        "receiver_id": random.choice([2, 3, 4]),
    }
    messages_data.append(new_msg)

# add 2 messages for each volunteer
for i in range(2, 5):
    for j in range(2):
        senders = [1,2,3,4]
        sent_at = convert_to_sqlite3_datetime(
            datetime.now() - timedelta(minutes=(i * 60))
        )

        new_msg = {
    
            "message": f"Hey there, I'm message {i}.{j}",
            "sent_at": sent_at,
            "urgency": random.choice(list(Priority)).value,
            "is_resolved": random.choice([True, False]),
            "sender_id": 1,
            "receiver_id": i,
        }
        messages_data.append(new_msg)

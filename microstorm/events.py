import redis
import json
import threading
from strictaccess import strict_access_control, public

@strict_access_control()
class EventSystem:
    def __init__(self):
        self._redis = redis.Redis(host="localhost", port=6379, decode_responses=True)

    @public
    def emit_event(self, event_type: str, data: dict):
        event = {
            "type": event_type,
            "data": data
        }
        self._redis.xadd(event_type, event)
        print(f"[EventSystem] Emitted event: {event_type} -> {data}")

    @public
    def listen_event(self, event_type: str, callback):
        def _listen():
            last_id = "$"  # Only new messages
            while True:
                response = self._redis.xread({event_type: last_id}, block=0, count=1)
                if response:
                    _, events = response[0]
                    for event_id, event_data in events:
                        data = json.loads(json.dumps(event_data))  # Convert field-value pairs
                        callback(data)
                        last_id = event_id

        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()
        print(f"[EventSystem] Listening to events: {event_type}")

# Instancia única
events = EventSystem()

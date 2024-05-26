
class Packet:
    def __init__(self, event_type, arrival_time, length=0, service_time=0):
        self.event_type = event_type
        self._arrival_time = arrival_time
        self._length = length
        self._service_time = service_time
        self._departure = None

    def departure(self, last_departure):
        """Return departure time."""
        #If the packet don't have to wait, the departure time is the arrival time plus the service time
        if self._arrival_time > last_departure:
            self._departure = self._arrival_time + self._service_time
        #If the packet have to wait, the departure time is the last departure time plus the service time
        else:
            self._departure = last_departure + self._service_time
        return self._departure

"""List of callbacks registered for events"""
_EVENT_SELECTION_MEMBERS 	= []
_EVENT_INSERT_MEMBERS 		= []
_EVENT_CLICKED_MEMBERS		= []

PUBLISHER_EVENT_SELECTION = 0
PUBLISHER_EVENT_INSERT    = 1
PUBLISHER_EVENT_CLICKED	  = 2


def register_to_event(event_type, callback):
	"""This function is called by the unit that wants to be informed about the event"""
	global _EVENT_SELECTION_MEMBERS
	global _EVENT_INSERT_MEMBERS
	global _EVENT_CLICKED_MEMBERS
	
	if PUBLISHER_EVENT_SELECTION == event_type:
		_EVENT_SELECTION_MEMBERS.append(callback)

	if PUBLISHER_EVENT_INSERT == event_type:
		_EVENT_INSERT_MEMBERS.append(callback)

	if PUBLISHER_EVENT_CLICKED == event_type:
		_EVENT_CLICKED_MEMBERS.append(callback)


def trigger_event(event_type,*args):
	"""This function is called by the unit that sends the event"""
	global _EVENT_SELECTION_MEMBERS
	global _EVENT_INSERT_MEMBERS
	global _EVENT_CLICKED_MEMBERS
		
	if PUBLISHER_EVENT_SELECTION == event_type:
		for _callback in _EVENT_SELECTION_MEMBERS:
			_callback(args)

	if PUBLISHER_EVENT_INSERT == event_type:
		for _callback in _EVENT_INSERT_MEMBERS:
			_callback(args)

	if PUBLISHER_EVENT_CLICKED == event_type:
		for _callback in _EVENT_CLICKED_MEMBERS:
			_callback(args)

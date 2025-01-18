import sparkplug_b.sparkplug_b_pb2 as sparkplug_b

# Initialize the payload
payload = sparkplug_b.Payload()

# Create PropertyValue objects for each channel using dictionaries
value_ch1 = {"type": 3, "int_value": 1000}
value_ch2 = {"type": 3, "int_value": 1000}
value_ch3 = {"type": 3, "int_value": 1000}
value_ch4 = {"type": 3, "int_value": 1000}

# Create a PropertySet object for the channel data using a dictionary
channel_property_set = {
    "keys": ["ch1", "ch2", "ch3", "ch4"],
    "values": [value_ch1, value_ch2, value_ch3, value_ch4],
}

# Create a PropertyValue that contains a PropertySetList using a dictionary
property_set_list_value = {
    "type": 21,  # PropertySetList type
    "propertysets_value": [channel_property_set],
}

# Create another PropertyValue (e.g., standalone integer) using a dictionary
standalone_property_value = {"type": 3, "int_value": 5}

# Create the full properties object using a dictionary
properties = {
    "keys": ["gain", "range"],
    "values": [property_set_list_value, standalone_property_value],
}

# Create a metric object with the properties
metric = sparkplug_b.Payload.Metric(properties=properties)

# Add the metric to the payload
payload.metrics.append(metric)

# At this point, `payload` is ready for serialization

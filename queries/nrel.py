queries = [
"""SELECT * WHERE {
?ahu a brick:AHU .
?mat a brick:Mixed_Air_Temperature_Sensor .
?sat a brick:Supply_Air_Temperature_Sensor .
?ccv a brick:Cooling_Valve .
?ccv_pos a brick:Position_Sensor .
?ahu brick:hasPoint ?mat .
?ahu brick:hasPoint ?sat .
?ahu brick:hasPart ?ccv .
?ccv brick:hasPoint ?ccv_pos
""",

"""SELECT * WHERE {
?ch a brick:Chiller .
?ct a brick:Cooling_Tower .
?chwp a brick:Chilled_Water_Pump .
?cdwp a brick:Condenser_Water_Pump .
?chwp_meter a brick:Power_Sensor .
?cdwp_meter a brick:Power_Sensor .
?chst a brick:Chilled_Water_Supply_Temperature_Sensor .
?chrt a brick:Chilled_Water_Return_Temperature_Sensor .
?chsfs a brick:Chilled_Water_Supply_Flow_Sensor .
?ct brick:feeds ?ch .
?ch brick:hasPart ?chwp .
?ch brick:hasPart ?cdwp .
?chwp brick:hasPoint ?chwp_meter .
?cdwp brick:hasPoint ?cdwp_meter .
?ch brick:hasPoint ?chst .
?ch brick:hasPoint ?chrt .
?ch brick:hasPoint ?chsfs
}""",

"""SELECT * WHERE {
?ch a brick:Chiller .
?chspt a brick:Chilled_Water_Supply_Temperature_Setpoint .
?chst a brick:Chilled_Water_Supply_Temperature_Sensor .
?chrt a brick:Chilled_Water_Return_Temperature_Sensor .
?ch brick:hasPoint ?chspt .
?ch brick:hasPoint ?chst .
?ch brick:hasPoint ?chrt .
?ccv    a brick:Cooling_Valve .
?ccv_pos a brick:Position_Sensor .
?ccv    brick:hasPoint ?ccv_pos .
?ch brick:feeds+ ?ccv
""",


"""SELECT * WHERE {
?oat_damper a brick:Outside_Damper .
?pos a brick:Damper_Position_Command .
?oat_damper brick:hasPoint ?pos .
?oat a brick:Outside_Air_Temperature_Sensor
}""",

# """,
# # Relevant poin
# brick:Heating_Temperature_Setpoint
# brick:Cooling_Temperature_Setpoint
# brick:Air_Flow_Setpoint
# brick:Occupancy_Status, brick:Occupancy_Sensor

# # Occupied/Unoccupied flavors (some work to do on Brick here)
# brick:Occupied_Heating_Temperature_Deadband_Setpoint
# brick:Occupied_Cooling_Temperature_Deadband_Setpoint
# brick:Unoccupied_Air_Temperature_Heating_Setpoint
# brick:Unoccupied_Air_Temperature_Cooling_Setpoint
# """,

"""SELECT * WHERE {
?ch a brick:Chiller .
?chspt a brick:Chilled_Water_Supply_Temperature_Setpoint .
?chst a brick:Chilled_Water_Supply_Temperature_Sensor .
?chrt a brick:Chilled_Water_Return_Temperature_Sensor .
?chsfs a brick:Chilled_Water_Supply_Flow_Sensor .
?ch brick:hasPoint ?chspt .
?ch brick:hasPoint ?chst .
?ch brick:hasPoint ?chrt .
?ch brick:hasPoint ?chsfs .
?chill_meter a brick:Power_Sensor .
?ch brick:hasPoint ?chill_meter .
?cnd a brick:Condenser .
?swts a brick:Supply_Water_Temperature_Sensor .
?cnd brick:hasPoint ?swts .
?ch brick:hasPart ?cnd .
?pump_meter a brick:Power_Sensor .
?chpmp a brick:Chilled_Water_Pump .
?chpmp brick:hasPoint ?pump_meter .
?ch brick:hasPart ?chpmp
}
""",

"""SELECT * WHERE {
?ahu a brick:Air_Handler_Unit
?dps a brick:Differential_Pressure_Sensor
?ahu brick:hasPart* ?x .
?x brick:hasPoint ?dps
}""",


"""SELECT * WHERE {
?ahu a brick:Air_Handler_Unit .
?supfan a brick:Supply_Fan .
?ahu brick:hasPart ?supfan .
?speed a brick:Speed_Sensor .
?power a brick:Power_Sensor .
?supfan brick:hasPoint ?speed .
?supfan brick:hasPoint ?power
}""",
]

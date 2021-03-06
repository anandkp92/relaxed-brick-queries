queries = [
    """SELECT * WHERE {
    ?temp a brick:Temperature_Sensor .
    ?hsp a brick:Heating_Temperature_Setpoint .
    ?csp a brick:Cooling_Temperature_Setpoint .
    ?equip a brick:Terminal_Unit .
    ?equip brick:hasPoint ?hsp .
    ?equip brick:hasPoint ?csp .
    ?equip brick:hasPoint ?temp .
    ?equip brick:feeds+ ?zone .
    ?zone a brick:HVAC_Zone .
    ?zone brick:isPartOf ?floor
    }
    """,

    """SELECT * WHERE {
?boiler a brick:Boiler .
?sup a brick:Supply_Water_Temperature_Sensor .
?ret a brick:Return_Water_Temperature_Sensor .
?boiler brick:hasPoint ?sup .
?boiler brick:hasPoint ?ret
}
    """,
    """ SELECT * WHERE {
?zone a brick:HVAC_Zone .
?afs a brick:Air_Flow_Sensor .
?zdt a brick:Discharge_Air_Temperature_Sensor .
?equip a brick:Terminal_Unit .
?equip brick:hasPoint ?zdt, ?afs .
?equip brick:feeds ?zone .
?ahu a brick:AHU .
?ahu_temp a brick:Temperature_Sensor .
?ahu brick:hasPoint ?ahu_temp .
?ahu brick:feeds+ ?equip .
?hv a brick:Heating_Valve .
?valve_pos a brick:Valve_Command .
?hv brick:hasPoint ?valve_pos .
?ahu brick:hasPart ?hv .
?equip brick:hasPoint ?hv
}
    """,

    """ SELECT * WHERE {
?chw_sp a brick:Chilled_Water_Supply_Temperature_Setpoint .
?hw_sp a brick:Hot_Water_Supply_Temperature_Setpoint .
?chw_sp brick:isPointOf ?equip .
?equip brick:feeds ?ahu .
?hw_sp brick:isPointOf ?equip .
?equip brick:feeds ?ahu .
?ahu a brick:Air_Handler_Unit .
?sup_air_sp a brick:Supply_Air_Temperature_Deadband_Setpoint .
?ahu brick:hasPoint ?sup_air_sp
}
""",

""" SELECT * WHERE {
?hw_supply_sp a brick:Hot_Water_Supply_Temperature_Setpoint .
?vlv a brick:Heating_Valve .
?vlv_pos a brick:Valve_Command .
?equip a brick:HVAC .
?hw_supply_sp brick:isPointOf ? thing .
?thing brick:feeds+ ?equip .
?equip brick:hasPart ?vlv
}
""",
""" SELECT * WHERE {
?ahu a brick:Air_Handler_Unit .
?sat_sensor a brick:Supply_Air_Temperature_Sensor .
?oat_sensor a brick:Outside_Air_Temperature_Sensor .
?zone_temp a brick:Zone_Air_Temperature_Sensor .
?zone_sp a brick:Zone_Air_Temperature_Setpoint .
?ahu brick:hasPoint ?sat_sensor .
?ahu brick:hasPoint ?oat_sensor .
?ahu brick:feeds+ ?x .
?x brick:hasPoint ?zone_temp .
?x brick:hasPoint ?zone_sp
}
""",
""" SELECT * WHERE {
?min_afs a brick:Min_Air_Flow_Setpoint_Limit .
?afs a brick:Air_Flow_Setpoint .
?vav a brick:VAV .
?vav brick:hasPoint ?min_afs .
?vav brick:hasPoint ?afs
}
""",

""" SELECT * WHERE {
?zts a brick:Zone_Air_Temperature_Sensor .
?zone a brick:HVAC_Zone .
?zts brick:isPointOf ?zone .
?zone brick:isFedBy+ ?ahu .
?ahu a brick:Air_Handler_Unit .
?fan a brick:Fan .
?status a brick:Fan_Status .
?fan brick:hasPoint ?status .
?fan brick:isPartOf ?ahu .
?oat a brick:Outside_Air_Temperature_Sensor
}
""",

""" SELECT * WHERE {
?rd a brick:Return_Damper .
?md a brick:Outside_Damper .
?rd brick:hasPoint ?rd_cmd .
?rd_cmd a brick:Damper_Position_Command .
?md brick:hasPoint ?md_cmd .
?md_cmd a brick:Damper_Position_Command .
?ahu a brick:Air_Handler_Unit .
?ahu brick:hasPart ?rd .
?ahu brick:hasPart ?md
}
""",

""" SELECT * WHERE {
?hv a brick:Heating_Valve .
?vlv_cmd a brick:Valve_Command .
?hv brick:hasPoint ?vlv_cmd .
?zafs a brick:Air_Flow_Sensor .
?dat a brick:Discharge_Air_Temperature_Sensor .
?vav a brick:VAV .
?zone a brick:HVAC_Zone .
?vav brick:feeds+ ?zone .
?vav brick:hasPart ?hv .
?vav brick:hasPoint ?zafs .
?vav brick:hasPoint ?dat .
?ahu brick:feeds+ ?vav .
?ahu brick:hasPoint ?ahu_temp .
?ahu_temp a brick:Temperature_Sensor
}
""",
]
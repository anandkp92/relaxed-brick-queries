queries = [
"""SELECT * WHERE { ?s ?p ?o }""",
"""SELECT ?point ?point_type WHERE {
    ?point rdf:type brick:Point .
    ?point rdf:type ?point_type 
}""",
 "SELECT ?meter WHERE { ?meter rdf:type brick:Green_Button_Meter }",
""" SELECT ?t WHERE { ?t rdf:type brick:Weather_Temperature_Sensor }""",
"""SELECT ?sensor WHERE {
    ?sensor rdf:type brick:Zone_Air_Temperature_Sensor .
    ?sensor brick:isPointOf ?equip 
}""",
"""SELECT ?sp WHERE {
    ?sp rdf:type brick:Zone_Air_Temperature_Setpoint .
    ?sp brick:isPointOf ?equip
}""",
 "SELECT ?meter WHERE { ?meter rdf:type brick:Building_Electric_Meter }",
 "SELECT ?point WHERE { ?point rdf:type brick:Occupancy_Sensor }",
 """SELECT ?tstat ?room ?zone ?state ?temp ?hsp ?csp WHERE {
            ?tstat brick:hasLocation ?room .
            ?zone brick:hasPart ?room .
            ?tstat brick:hasPoint ?state .
            ?tstat brick:hasPoint ?temp .
            ?tstat brick:hasPoint ?hsp .
            ?tstat brick:hasPoint ?csp .
            ?zone rdf:type brick:Zone .
            ?tstat rdf:type brick:Thermostat .
            ?state rdf:type brick:Thermostat_Status .
            ?temp  rdf:type brick:Temperature_Sensor  .
            ?hsp   rdf:type brick:Supply_Air_Temperature_Heating_Setpoint .
            ?csp   rdf:type brick:Supply_Air_Temperature_Cooling_Setpoint
        }
    """,
"""SELECT ?sensor ?sp ?equip WHERE {
    ?sensor    rdf:type     brick:Air_Flow_Sensor .
    ?sp    rdf:type     brick:Air_Flow_Setpoint .
    ?sensor    brick:isPointOf ?equip .
    ?sp    brick:isPointOf ?equip
}""",
    """SELECT ?cooling_point ?heating_point ?ahu WHERE {
        ?cooling_point rdf:type brick:Cooling_Valve_Command .
        ?heating_point rdf:type brick:Heating_Valve_Command .
        ?ahu brick:hasPoint ?cooling_point .
        ?ahu brick:hasPoint ?heating_point
    }""",
"""SELECT * WHERE {
    ?equip        rdf:type   brick:VAV .
    ?equip        brick:isFedBy+                 ?ahu .
    ?vlv          rdf:type                    ?vlv_type .
    ?ahu          brick:hasPoint                 ?upstream_ta .
    ?equip        brick:hasPoint                 ?dnstream_ta .
    ?upstream_ta  rdf:type   brick:Supply_Air_Temperature_Sensor .
    ?dnstream_ta  rdf:type   brick:Supply_Air_Temperature_Sensor .
    ?equip        brick:hasPoint                 ?vlv .
    ?vlv          rdf:type   brick:Valve_Command
}""",
    """SELECT * WHERE {
        ?equip        rdf:type   brick:VAV .
        ?equip        brick:hasPoint                 ?air_flow .
        ?air_flow     rdf:type   brick:Supply_Air_Flow_Sensor
    }""",
 """SELECT * WHERE {
        ?vlv        rdf:type   brick:Valve_Command .
        ?vlv        rdf:type                    ?vlv_type .
        ?equip      brick:hasPoint                 ?vlv .
        ?equip      rdf:type   brick:Air_Handling_Unit .
        ?air_temps  rdf:type   brick:Supply_Air_Temperature_Sensor .
        ?equip      brick:hasPoint                 ?air_temps .
        ?air_temps  rdf:type                    ?temp_type
    }""",
"""SELECT * WHERE {
        ?vlv        rdf:type   brick:Valve_Command .
        ?vlv        rdf:type                    ?vlv_type .
        ?equip      brick:hasPoint                 ?vlv .
        ?equip      rdf:type   brick:Air_Handling_Unit .
        ?air_temps  rdf:type   brick:Return_Air_Temperature_Sensor .
        ?equip      brick:hasPoint                 ?air_temps .
        ?air_temps  rdf:type                    ?temp_type
    }""",
"""SELECT ?vav WHERE {
    ?vav rdf:type brick:VAV
}""",
#"""SELECT DISTINCT ?sensor ?room
#WHERE {
#
#    ?sensor rdf:type brick:Zone_Temperature_Sensor .
#    ?room rdf:type brick:Room .
#    ?vav rdf:type brick:VAV .
#    ?zone rdf:type brick:HVAC_Zone .
#
#    ?vav brick:feeds+ ?zone .
#    ?zone brick:hasPart ?room .
#
#    {?sensor brick:isPointOf ?vav }
#    UNION
#    {?sensor brick:isPointOf ?room }
#}""",
"""SELECT ?sensor ?room WHERE {
    ?sensor rdf:type brick:Zone_Temperature_Sensor .
    ?room rdf:type brick:Room .
    ?vav rdf:type brick:VAV .
    ?zone rdf:type brick:HVAC_Zone .
    ?vav brick:feeds+ ?zone .
    ?zone brick:hasPart ?room .
    ?vav brick:hasPoint ?sensor
}""",
# """SELECT ?vlv_cmd ?vav
# WHERE {
#   {  ?vlv_cmd rdf:type brick:Reheat_Valve_Command }
#   UNION
#   { ?vlv_cmd rdf:type brick:Cooling_Valve_Command }
# ?vav rdf:type brick:VAV .
# ?vav brick:hasPoint+ ?vlv_cmd .
# }""",
"""SELECT ?floor ?room ?zone WHERE {
    ?floor rdf:type brick:Floor .
    ?room rdf:type brick:Room .
    ?zone rdf:type brick:HVAC_Zone .

    ?room brick:isPartOf+ ?floor .
    ?room brick:isPartOf+ ?zone
}""",
]

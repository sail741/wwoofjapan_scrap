
params_keep_all = {
    "output_file": "output.txt",
    "display_eta": True,
    "list_columns": [
        "id",
        "qty_wwoofers",
        "island",
        "region",
        "relation_wwoofers",
        "feeding_restriction",
        "tasks",
        "date",
        "city",
        "prefecture",
        "host_xp",
        "staying_time",
        "url"
    ],
    "criterias": [
    ]
}


params_keep_all_small_output = {
    "output_file": "output.txt",
    "display_eta": True,
    "list_columns": [
        "id",
        "url"
    ],
    "criterias": [
    ]
}


params_couple_with_restriction = {
    "output_file": "output.txt",
    "display_eta": True,
    "list_columns": [
        "id",
        "qty_wwoofers",
        "island",
        "region",
        "relation_wwoofers",
        "feeding_restriction",
        "tasks",
        "date",
        "city",
        "prefecture",
        "host_xp",
        "staying_time",
        "url"
    ],
    "criterias": [
        {
            "name": "qty_wwoofers",
            "required": True,
            "type": "string",
            "allowed_values": [],
            "banned_values": ["One only"]
        },
        {
            "name": "relation_wwoofers",
            "required": True,
            "type": "string",
            "allowed_values": ["couple", "different gender", "A wife & husband"],
            "banned_values": []
        },
        {
            "name": "date",
            "required": True,
            "type": "string",
            "allowed_values": ["October", "Almost all year round", "All year round"],
            "banned_values": []
        },
        {
            "name": "host_xp",
            "required": True,
            "type": "int",
            "min_value": 5,
            "max_value": None
        },
        {
            "name": "feeding_restriction",
            "required": True,
            "type": "feeding",
            "remove": True

        }
    ]
}

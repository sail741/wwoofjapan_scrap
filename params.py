
params_keep_all = {
    "output_file": "output.txt",
    "display_eta": True,
    "criterias": [
        {
            "_description": "The quantity of wwoofer allowed as text",
            "div_id": "cbfv_293",
            "required": False,
            "type": "string",
            "allowed_values": [],
            "banned_values": []
        },
        {
            "_description": "The relations between the wwoofer as text",
            "div_id": "cbfv_296",
            "required": False,
            "type": "string",
            "allowed_values": [],
            "banned_values": []
        },
        {
            "_description": "The date when the wwoofing is enabled as text",
            "div_id": "cbfv_290",
            "required": False,
            "type": "string",
            "allowed_values": [],
            "banned_values": []
        },
        {
            "_description": "Since how many years the hosts does wwoofing",
            "div_id": "cbfv_542",
            "required": False,
            "type": "int",
            "min_value": None,
            "max_value": None
        },
        {
            "_description": "What kind of feeding is allowed",
            "div_id": "cbfv_318",
            "required": False,
            "type": "feeding",
            "remove": False
        }
    ]
}

params_couple_with_restriction = {
    "output_file": "output.txt",
    "display_eta": True,
    "criterias": [
        {
            "_description": "The quantity of wwoofer allowed as text",
            "div_id": "cbfv_293",
            "required": True,
            "type": "string",
            "allowed_values": [],
            "banned_values": ["One only"]
        },
        {
            "_description": "The relations between the wwoofer as text",
            "div_id": "cbfv_296",
            "required": True,
            "type": "string",
            "allowed_values": ["couple", "different gender", "A wife & husband"],
            "banned_values": []
        },
        {
            "_description": "The date when the wwoofing is enabled as text",
            "div_id": "cbfv_290",
            "required": True,
            "type": "string",
            "allowed_values": ["October", "Almost all year round", "All year round"],
            "banned_values": []
        },
        {
            "_description": "Since how many years the hosts does wwoofing",
            "div_id": "cbfv_542",
            "required": True,
            "type": "int",
            "min_value": 5,
            "max_value": None
        },
        {
            "_description": "What kind of feeding is allowed",
            "div_id": "cbfv_318",
            "required": True,
            "type": "feeding",
            "remove": True

        }
    ]
}

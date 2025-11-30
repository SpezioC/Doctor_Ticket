alert_dict = {
    "asap":35,
    "urgent":40,
    "everything blocked":90,
    "angry customer":80,
    "highest priority":40,
    "customer impact":100
}
problem_dict = {
    "payment error": 100,
    "login not working": 130,
    "server down": 150,
    "timeout": 55,
    "production stopped": 170,
    "desing": 20,
    "pipe leak": 120,
    "no hot water": 80,
}
negative_dict = {
    "suggestion":20,
    "feature request":25,
    "visual improvement":15,
    "layout":10,
    "color":10,
    "idea":10,
    "low priority":20
}
priority_thresholds = [
    ("low", 50),
    ("medium", 80),
    ("high", 130),
    ("critical", 999)
]

# To link the problem analysis with the position (where),
# I decided to use the problem_tag as the connection point.
maintenance_area_dict = {
    "payment error": "informatics",
    "login not working": "informatics",
    "server down": "informatics",
    "timeout": "informatics",
    "production stopped": "informatics",

    "pipe leak": "hydraulics",
    "no hot water": "hydraulics",

    "desing": "general",
    "layout": "general",
    "visual improvement": "general",
    
}
where_tuple = (
    "building 1",
    "building 2",
    "building 3"
)


# I dediced to check only for problem the correct word
value_dict = {
    "payent":"payment",
    "eror":"error",
    "log":"login",
    "serv":"server",
    "time-out":"timeout",
    "prod":"production",
    "stop":"stopped",
    "sistem":"system"
}


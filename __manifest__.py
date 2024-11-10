{
    "name": "GLDF JSON Integration",
    "version": "0.1",
    "summary": "Integrate GLDF files using gldf_rs_python for JSON representation",
    "category": "Inventory",
    "author": "Holger Trahe",
    "depends": [
        "base",
        "mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/gldf_file_views.xml",
        "views/lighting_product_views.xml",
    ],
    "installable": True,
    "application": True,
}
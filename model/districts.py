from flask import jsonify
import json

class maintenance:
    def getGeoJSON():
        
        with open("datasets/maintenanceAssesmentDistricts/Shaperfile/maintenance_assessment_districts_datasd.geojson") as f:
            geojson_data = json.load(f)
            
        return jsonify(geojson_data)
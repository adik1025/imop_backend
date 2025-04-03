#!/bin/bash
# Use this script to re-download scripts from the SD Open Data portal (data.sandiego.gov)

# Pavement Condition Assessments is not needed; not updated frequently

# Streets Repair Line Segments
wget https://seshat.datasd.org/gis_streets_repair_segs/sd_paving_segs_datasd.csv --directory-prefix=datasets/streetsRepairLineSegments -O datasets/streetsRepairLineSegments/sd_paving_segs_datasd.csv

# Pothole Repair Requests
wget https://seshat.datasd.org/get_it_done_potholes/get_it_done_pothole_requests_datasd.csv --directory-prefix=datasets/potholeRepairRequests -O datasets/potholeRepairRequests/get_it_done_pothole_requests_datasd.csv

# Streets Repair Projects
wget https://seshat.datasd.org/streets_repair_projects/sd_paving_datasd.csv --directory-prefix=datasets/streetsRepairProjects -O datasets/streetsRepairProjects/sd_paving_datasd.csv

# Maintenance assessment districts
wget https://seshat.datasd.org/gis_maintenance_assessment_districts/maintenance_assessment_districts_datasd.csv --directory-prefix=datasets/maintenanceAssessmentDistricts -O datasets/maintenanceAssessmentDistricts/maintenance_assessment_districts_datasd.csv

# Facility Condition Index ratings for City buildings
wget https://seshat.datasd.org/fci_city_buildings/facilities_assessment_datasd.csv --directory-prefix=datasets/facilityConditionIndexRatings -O datasets/facilityConditionIndexRatings/facilities_assessment_datasd.csv
#!/bin/bash

# Streets Repair Projects
wget https://seshat.datasd.org/streets_repair_projects/sd_paving_datasd.csv --directory-prefix=datasets/streetsRepairProjects -O datasets/streetsRepairProjects/sd_paving_datasd.csv

# Pothole Repair Requests
wget https://seshat.datasd.org/get_it_done_potholes/get_it_done_pothole_requests_datasd.csv --directory-prefix=datasets/potholeRepairRequests -O datasets/potholeRepairRequests/get_it_done_pothole_requests_datasd.csv

# Facility Condition Index ratings for City buildings
wget https://seshat.datasd.org/fci_city_buildings/facilities_assessment_datasd.csv --directory-prefix=datasets/facilityConditionIndexRatings -O datasets/facilityConditionIndexRatings/facilities_assessment_datasd.csv
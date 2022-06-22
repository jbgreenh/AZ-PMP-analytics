# AZ-PMP-analytics
  
### setup
```
python3.10 setup.py install
pip310 install -r requirements.txt
```
### usage
add the required files from `required_files.txt` to the data folder of the script you wish to run  
run the python script in the folder
  
### compliance_pharmacists
monthly checks for pharmacist registration and pharmacist usage  
  
### pharmacy_cleanup
checks delinquent pharmacies for status in igov for updating manage pharmacies reporting exceptions  
  
### reg_checks
check prescriber lists for registration in awarxe

### signups
generate a file with the two data tabs for the monthly signups and county lists report  

### deas
to update the base DEA file, add a new ``cs_active.txt`` to the data folder and run ``az_prescriber_deas.py``

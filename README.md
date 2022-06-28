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
generate a filtered version of the dea file  

### unregistered_prescribers
WIP  

### clearinghouse_check
check ``az_pharmacy_deas`` for any pharmacies not in the ``clearinghouse``

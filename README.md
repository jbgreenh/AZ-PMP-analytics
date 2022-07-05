# AZ-PMP-analytics
  
### setup
using python 3.10  
```
python setup.py install
pip install -r requirements.txt
```
### usage
add or update the required files from `required_files.txt` to the data folder of the script you wish to run  
run the python script in the folder
  
### compliance_pharmacists
monthly checks for pharmacist registration and pharmacist usage  
  
### pharmacy_cleanup
checks delinquent pharmacies for status in igov for updating manage pharmacies reporting exceptions  
  
### reg_checks
check prescriber lists for registration in awarxe with ``presc_reg_check.py``  
check pharmacist lists for registration in awarxe with ``pharm_reg_check.py``  

### signups
generate a file with the two data tabs for the monthly signups and county lists report  

### deas
generate a filtered version of the dea file  

### unregistered_prescribers
generate a list for each board of their prescribers who are unregistered in awarxe (WIP)  

### clearinghouse_check
check ``az_pharmacy_deas`` for any pharmacies not in the ``clearinghouse``  

### medical_marijuana
check medical marijuana list for registration and usage (WIP)  

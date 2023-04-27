# AZ-PMP-analytics
  
### setup
using python 3.10+ (you may need to add --user to the end of the first command)  
```
pip install .
pip install -r requirements.txt
```
if you ever need to update all required packages:    
```
pip uninstall utils
pip install .
pip install -r requirements.txt
```  
for uploading .ipynb files without their output:  
https://gist.github.com/33eyes/431e3d432f73371509d176d0dfb95b6e

### usage
add (or update) the required files from `required_files.txt` to the data folder of the script you wish to run  
run the python script in the folder
  
### compliance_pharmacists
monthly checks for pharmacist registration and pharmacist usage  
  
### pharmacy_cleanup
checks delinquent pharmacies for status in igov for updating manage pharmacies reporting exceptions  
  
### reg_checks
check prescriber lists for registration in awarxe with ``presc_reg_check.py``  
check pharmacist lists for registration in awarxe with ``pharm_reg_check.py``  

### signups
generate a file for the monthly signups and county lists report  

### deas
generate a filtered version of the dea file  

### unregistered_prescribers
generate a list for each board of their prescribers who are unregistered in awarxe  

### clearinghouse_check
check ``az_pharmacy_deas`` for any pharmacies not in the clearinghouse  

### medical_marijuana
check medical marijuana list for registration and usage  
``mm1.py`` generates files and copies the prescribers for manual matching to the clipboard  
``mm2.py`` combines the manual matches with the generated matches and the lookups to produce the final report  

### naloxone  
find sum of naloxone doses dispensed and generate email body  

### scorecard
generate the monthly scorecard for % of prescriber PMP usage  

### exclude_ndcs  
generate and update lists of opiate antagonist ndcs to exclude from awarxe reports  

### temp
miscellaneous scripts for adhoc reporting  

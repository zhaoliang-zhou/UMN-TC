README.md



# py: 
Contains Python3 notebooks fo the Equity OKR project. The most important files are: race_ebm_funcs.py and main.py

## file description

### merge_race_ebm_measures_included.ipynb
* query predicted_race data from hive, all variabels included, added gender, dob, age (calculated from dob)
* query ebm data measures from Medinsight - include member number, ebm label, ebm category, ebm numerator, ebm denominator, ebm end date. Filter - include all members with specified (over/underuse) measures
* specified ebm end date 2020-12
* join the ebm data and predict_race data by member number (12 digits)


### race_ebm_tables.ipynb
* py notebook for producing OKR tables
* overuse/underuse by race
* specific ebm by race


### main.ipynb
* the original document to produce main.py


### race_ebm_funcs.ipynb
* the original document to produce race_ebm_funcs.py


### chi_square_tests
* chi-square tests for overuse + underuse at aggregate level


# R
contains R notebook for equity OKR analysis
## file description
### ebm_analysis.md 
Rmarkdown files for the ebm analysis. glmer models for overuse data and underuse data. This notebook also contains some EDA, differet methods other than glmer, test for terms, and goodness-of-fit tests for the models. 

Note:
* recommand download the notebook to run in local Rstudio
* recommand output as html 
* remember to install the libraries
* recommand running the main.py notebook under py folder first. main.py creates over.df and under.df which are used in this R notebook


# restricted
Contains saved data mostly in csv format. Contains PHI and DO NOT commit/push to GitHub! 
## file description
### race_ebm_analysis
Analysis data set for Equity OKR produced from the file merge_race_ebm_measures_included
* contains variables: member_number, member_id, age, gender, ebm_label, ebm end date



### over_tab 
table for specific overuse ebm for each race

### under_tab
table for specific underuse ebm for each race 

### over_under_tab
table for general overuse/underuse by each race

### underuse_df
* produced from race_ebm_tables 
* dataframe contains all the members with underuse ebm 

### overuse_df 
* produced from race_ebm_tables 
* dataframe contains all the members with overuse ebm 


### neighborhood_deprivation_index
Non Phi NDI data. Contains fips and adi_natrank. 
* adi_natrank: range 1- 100 from no deprivation - deprived
* continuous measure of socioeconomics status



# Workflow/Important decisions/log
## initial data pulling
* get predicted_race data
* create age variable from predicted_race data from the dob
* get ebm data from Milliman 
* from ebm data, select rows with specified overuse and underuse measures (measures selected with help from Tamra, Jaclyn, and Alex)
* get NDI data
* merge predicted_race data, ebm data, and ndi data on member ID and fips
* when merge, used select distinct. So no replicates (same member and same ebm measure) 
* in the main.py, ebm end date is an input argument which can be specified by user 
* after merge, N = 42166
* create over/underuse variable, over if the row ebm measure belongs to overuse, under if the ebm measure belongs to underuse
* save the data to restricted file 
* change variable unver/underuse to categorical data type
* create 2 separate datasets, 1 for overuse measures, and 1 for underuse measures. 

## create tables
* from overall data, create table for overuse and underuse by different race
* from overuse data, create table: specific overuse measures by different race
* from underuse data, create table: specific underuse measures by different race
* percentage calculated as: sum numerator/sum denominator


## analysis (R)


## Wednesday 7/7
During meeting with Jaclyn and Tamra, decided to drop follwoing measures: 
overuse: 
IQI_34_TOTAL_2017 - Vaginal Birth After Cesarean (VBAC) Rate, All (Overall) drop 


underuse: 
NCS_2020 - Non-Recommended Cervical Cancer Screening in Adolescent Females      drop
NYU_EM_ED_PA_2016 - NYU ED Utilization Algorithm: Emergent, ED Care Needed, Preventable/Avoidable   drop


The following should take inverse: 
overuse: 
AAB_2020C - Avoidance of Antibiotic Treatment for Acute Bronchitis/Bronchiolitis (Total) (take inverse)
CWP_2020C - Appropriate Testing for Pharyngitis (Total) (take inverse)
URI_2020C - Appropriate Treatment for Upper Respiratory Infection (take inverse)

underuse: none




## Tuesday 7/13
From Slack channel with Tamra and Jaclyn, decided to drop the ebm with insufficient denominator (less than 10). 
Below are the measures removed: 

### Overuse: 
* APC_TOTAL_2019 - Use of Multiple Concurrent Antipsychotics in Children and Adolescents (Total)

### Underuse:
* ADD_R1_2020C - Follow-Up Care for Children Prescribed ADHD Medication: Initiation Phase
* ADD_R2_2020C - Follow-Up Care for Children Prescribed ADHD Medication: Continuation & Maintenance Phase
* APP_TOTAL_2020 - Use of First-Line Psychosocial Care for Children and Adolescents on Antipsychotics (Total)
* FUA30_TOTAL_2020 - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 30 days (Overall)
* FUA7_TOTAL_2020 - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 07 days (Overall)
* FUH_30_TOTAL_2020 - Follow-Up After Hospitalization for Mental Illness: Total (30 Days Post-Discharge)
* FUH_7_TOTAL_2020 - Follow-Up After Hospitalization for Mental Illness: Total (7 Days Post-Discharge)
* FUM_30_TOTAL_2020 - Follow-Up After Emergency Department Visit for Mental Illness (Total)-30 Day Follow-Up
* FUM_7_TOTAL_2020 - Follow-Up After Emergency Department Visit for Mental Illness (Total)-7 Day Follow-Up
* SAA_2020 - Adherence to Antipsychotic Medications for Individuals with Schizophrenia
* SPC_R1_TOTAL_2020 - Statin Therapy for Patients with Cardiovascular Disease, Rate 1: Received Statin Therapy (Total)
* SPC_R2_TOTAL_2020 - Statin Therapy for Patients with Cardiovascular Disease, Rate 2: Statin Adherence 80% (Total)
* W15_V00_2020C - Well-Child Visits in the First 15 Months of Life: 0 Visits
* W15_V01_2020C - Well-Child Visits in the First 15 Months of Life: 1 Visit
* W15_V02_2020C - Well-Child Visits in the First 15 Months of Life: 2 Visits
* W15_V03_2020C - Well-Child Visits in the First 15 Months of Life: 3 Visits
* W15_V04_2020C - Well-Child Visits in the First 15 Months of Life: 4 Visits
* W15_V05_2020C - Well-Child Visits in the First 15 Months of Life: 5 Visits
* W15_V06+_2020C - Well-Child Visits in the First 15 Months of Life: 6 or more Visits

In addition, only focuses on the race group white, black, and hispanic

please email zhou1561@umn.edu if you have any questions. 
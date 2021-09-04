#import library
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import sys
import numpy as np
import race_ebm_funcs as ref

# starburst access credentials
username = input('Enter your jumpcloud username: ')
print('Enter your password:')
conn = ...connect.presto(username=username, phi=True, starburst=True)

#get the original data from starburst
end_date = input('EBM end date(year-month): ') #in format year-month. Ex. 2020-12
race_ebm_df = ref.get_data(conn, end_date)

# #filter the data based on the ebm end date, select the rows with specified ebm end date
# end_date = input('EBM end date: ') #input need to be in format year-month. Ex. 2020-12
# race_ebm_df  = ref.filter_end_date(race_ebm_df, end_date)

#create another column for over/underuse
#Create under/overuse based on EBM measure label
underuse = [
'APP_TOTAL_2020',# - Use of First-Line Psychosocial Care for Children and Adolescents on Antipsychotics (Total)',
'PPC_PN_2020C',#  - Prenatal and Postpartum Care: Prenatal Care',
'PPC_PP_2020C',#  - Prenatal and Postpartum Care: Postpartum Care',
'ADD_R1_2020C',#  - Follow-Up Care for Children Prescribed ADHD Medication: Initiation Phase',
'ADD_R2_2020C',#  - Follow-Up Care for Children Prescribed ADHD Medication: Continuation & Maintenance Phase',
'FUA30_TOTAL_2020',#  - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 30 days (Overall)',
'FUA7_TOTAL_2020',#  - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 07 days (Overall)',
'FUH_30_TOTAL_2020',#  - Follow-Up After Hospitalization for Mental Illness: Total (30 Days Post-Discharge)',
'FUH_7_TOTAL_2020',#  - Follow-Up After Hospitalization for Mental Illness: Total (7 Days Post-Discharge)',
'FUM_30_TOTAL_2020',#  - Follow-Up After Emergency Department Visit for Mental Illness (Total)-30 Day Follow-Up',
'FUM_7_TOTAL_2020',#  - Follow-Up After Emergency Department Visit for Mental Illness (Total)-7 Day Follow-Up',
'SAA_2020',#  - Adherence to Antipsychotic Medications for Individuals with Schizophrenia',
'SPC_R1_TOTAL_2020',#  - Statin Therapy for Patients with Cardiovascular Disease, Rate 1: Received Statin Therapy (Total)',
'SPC_R2_TOTAL_2020',#  - Statin Therapy for Patients with Cardiovascular Disease, Rate 2: Statin Adherence 80% (Total)',
'CDC_A1C_T_2020C',#  - Comprehensive Diabetes Care: Hemoglobin A1c (HbA1c) Testing',
'PQA_BB_2018',#  - Percentage of members 18 years and older who met the PDC threshold of 80% for beta-blockers during the measurement period.',
'PQA_RASA_2018',#  - Percentage of members 18 years and older who met the PDC threshold of 80% for Renin Angiotensin System Antagonists during the measurement period.',
#'NYU_EM_ED_PA_2016',#  - NYU ED Utilization Algorithm: Emergent, ED Care Needed, Preventable/Avoidable',
#'NCS_2020',#  - Non-Recommended Cervical Cancer Screening in Adolescent Females',
'BCS_NON_MCR_2020C',#  - Breast Cancer Screening',
'CHL_TOTAL_2020C',#  - Chlamydia Screening in Women (Total)',
'COL_NON_MCR_2020C',#  - Colorectal Cancer Screening',
'IMA_HPV_2020',#  - Immunizations for Adolescents: HPV Vaccine',
'IMA_MEN_2020',#  - Immunizations for Adolescents: Meningococcal Conjugate or Meningococcal Polysaccharide Vaccine',
'IMA_TD_2020',#  - Immunizations for Adolescents: Tdap Vaccine',
'W15_V00_2020C',#  - Well-Child Visits in the First 15 Months of Life: 0 Visits',
'W15_V01_2020C',#  - Well-Child Visits in the First 15 Months of Life: 1 Visit',
'W15_V02_2020C',#  - Well-Child Visits in the First 15 Months of Life: 2 Visits',
'W15_V03_2020C',#  - Well-Child Visits in the First 15 Months of Life: 3 Visits',
'W15_V04_2020C',#  - Well-Child Visits in the First 15 Months of Life: 4 Visits',
'W15_V05_2020C',#  - Well-Child Visits in the First 15 Months of Life: 5 Visits',
'W15',#_V06+_2020C - Well-Child Visits in the First 15 Months of Life: 6 or more Visits',
'W34_2020C'#  - Well-Child Visits in the Third, Fourth, Fifth and Sixth Years of Life'  		
           ]
           
overuse = [
#'NYU_EM_PCT_2016',#  - NYU ED Utilization Algorithm: Emergent, Primary Care Treatable',
'NYU_NON_EM_2016',#  - NYU ED Utilization Algorithm: Non-Emergent',
'AAB_2020C',#  - Avoidance of Antibiotic Treatment for Acute Bronchitis/Bronchiolitis (Total)',
'APC_TOTAL_2019',#  - Use of Multiple Concurrent Antipsychotics in Children and Adolescents (Total)',
'HDO_2020',#  - Use of Opioids at High Dosage',
'LBP_2020C',#  - Use of Imaging Studies for Low Back Pain',
'UOP_NUM1_2020',#  - Use of Opioids from Multiple Providers (Multiple Prescribers)',
'UOP_NUM2_2020',#  - Use of Opioids from Multiple Providers (Multiple Pharmacies)',
'UOP_NUM3_2020',#  - Use of Opioids from Multiple Providers (Multiple Prescribers and Multiple Pharmacies)',
'URI_2020C',#  - Appropriate Treatment for Upper Respiratory Infection',
'CWP_2020C',#  - Appropriate Testing for Pharyngitis (Total)',
'IQI_21_TOTAL_2017'#,  - Cesarean Delivery Rate, Uncomplicated (Overall)',
#'IQI_34_TOTAL_2017'#  - Vaginal Birth After Cesarean (VBAC) Rate, All (Overall)'
          ]

#adding the over/underuse column
race_ebm_df = ref.add_ebm_col(overuse, underuse, race_ebm_df)

#convert over/underuse col to categorical variable
race_ebm_df = ref.convert_cat(race_ebm_df)

#save separate datasets for underuse and overuse
race_ebm_df.to_csv(r'.../restricted /main_race_ebm_analysis.csv', index = False)
overuse_df = race_ebm_df[race_ebm_df['over/underuse'] == 'over']
overuse_df.to_csv(r'.../restricted /main_overuse_df.csv', index = False)
underuse_df = race_ebm_df[race_ebm_df['over/underuse'] == 'under']
underuse_df.to_csv(r'.../restricted /main_underuse_df.csv', index = False)

#read the datasets 
race_ebm_df = pd.read_csv ('.../restricted /main_race_ebm_analysis.csv')
over_df = pd.read_csv ('.../restricted /main_overuse_df.csv')
under_df = pd.read_csv ('.../restricted /main_underuse_df.csv')

#get the race proportion table
ref.race_prop_tab(race_ebm_df)

#overuse and underuse vs. race
ref.over_under_tab(race_ebm_df)

#table for overuse measures by race 
ref.ebm_tab(over_df)

#table for underuse measures by race 
ref.ebm_tab(under_df)


#import library
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import sys
sys.path.append('../../../../DataScience/lib/')
import pymei
from dev.bind_prod_utils import utils as dev_utils
import numpy as np

#sql query to get the data, ebm end date as an argument
def get_data(conn, end_date):  
    query1 = '''
    with race_data as (
	select 
		race.*,
		m.member_number,
		m.dob,
		m.gender,
		floor(date_diff('DAY', m.dob, current_date) / 365.25) as age
	from hive.data_science_analytics.race_predict_v3_parquet race
	left join hive.data_layer_prod.bind_vw_latest_member as m on race.member_id = m.member_id
    ),
    milliman_data as (
    select
      dim_member.member_id as member_number,
      dim_ebm.ebm_measure_label,
      dim_ebm.ci_measure_cat,
      fact_ebm.numerator,
      fact_ebm.denominator,
      dim_date_ebm.yearmo_name
    from milliman_current.qe.fact_ebm as fact_ebm
    left join milliman_current.QE.DIM_DATE_EBM as DIM_DATE_EBM on (FACT_EBM.EBM_DATE_INT = DIM_DATE_EBM.YEARMO_KEY)
    left join milliman_current.qe.dim_ebm as dim_ebm on fact_ebm.ebm_key = dim_ebm.ebm_key
    left join milliman_current.qe.dim_member as dim_member on fact_ebm.member_key = dim_member.member_key
    where
  (
    ebm_measure_label in (
--starting here all underuse
'APP_TOTAL_2020 - Use of First-Line Psychosocial Care for Children and Adolescents on Antipsychotics (Total)',
'PPC_PN_2020C - Prenatal and Postpartum Care: Prenatal Care',
'PPC_PP_2020C - Prenatal and Postpartum Care: Postpartum Care',
'ADD_R1_2020C - Follow-Up Care for Children Prescribed ADHD Medication: Initiation Phase',
'ADD_R2_2020C - Follow-Up Care for Children Prescribed ADHD Medication: Continuation & Maintenance Phase',
'FUA30_TOTAL_2020 - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 30 days (Overall)',
'FUA7_TOTAL_2020 - Follow-Up After Emergency Department Visit for Alcohol and Other Drug Abuse or Dependence : 07 days (Overall)',
'FUH_30_TOTAL_2020 - Follow-Up After Hospitalization for Mental Illness: Total (30 Days Post-Discharge)',
'FUH_7_TOTAL_2020 - Follow-Up After Hospitalization for Mental Illness: Total (7 Days Post-Discharge)',
'FUM_30_TOTAL_2020 - Follow-Up After Emergency Department Visit for Mental Illness (Total)-30 Day Follow-Up',
'FUM_7_TOTAL_2020 - Follow-Up After Emergency Department Visit for Mental Illness (Total)-7 Day Follow-Up',
'SAA_2020 - Adherence to Antipsychotic Medications for Individuals with Schizophrenia',
'SPC_R1_TOTAL_2020 - Statin Therapy for Patients with Cardiovascular Disease, Rate 1: Received Statin Therapy (Total)',
'SPC_R2_TOTAL_2020 - Statin Therapy for Patients with Cardiovascular Disease, Rate 2: Statin Adherence 80%% (Total)',
'CDC_A1C_T_2020C - Comprehensive Diabetes Care: Hemoglobin A1c (HbA1c) Testing',
'PQA_BB_2018 - Percentage of members 18 years and older who met the PDC threshold of 80%% for beta-blockers during the measurement period.',
'PQA_RASA_2018 - Percentage of members 18 years and older who met the PDC threshold of 80%% for Renin Angiotensin System Antagonists during the measurement period.',
--'NYU_EM_ED_PA_2016 - NYU ED Utilization Algorithm: Emergent, ED Care Needed, Preventable/Avoidable',
--'NCS_2020 - Non-Recommended Cervical Cancer Screening in Adolescent Females',
'BCS_NON_MCR_2020C - Breast Cancer Screening',
'CHL_TOTAL_2020C - Chlamydia Screening in Women (Total)',
'COL_NON_MCR_2020C - Colorectal Cancer Screening',
'IMA_HPV_2020 - Immunizations for Adolescents: HPV Vaccine',
'IMA_MEN_2020 - Immunizations for Adolescents: Meningococcal Conjugate or Meningococcal Polysaccharide Vaccine',
'IMA_TD_2020 - Immunizations for Adolescents: Tdap Vaccine',
'W15_V00_2020C - Well-Child Visits in the First 15 Months of Life: 0 Visits',
'W15_V01_2020C - Well-Child Visits in the First 15 Months of Life: 1 Visit',
'W15_V02_2020C - Well-Child Visits in the First 15 Months of Life: 2 Visits',
'W15_V03_2020C - Well-Child Visits in the First 15 Months of Life: 3 Visits',
'W15_V04_2020C - Well-Child Visits in the First 15 Months of Life: 4 Visits',
'W15_V05_2020C - Well-Child Visits in the First 15 Months of Life: 5 Visits',
'W15_V06+_2020C - Well-Child Visits in the First 15 Months of Life: 6 or more Visits',
'W34_2020C - Well-Child Visits in the Third, Fourth, Fifth and Sixth Years of Life',
 --starting here all overuse
--'NYU_EM_PCT_2016 - NYU ED Utilization Algorithm: Emergent, Primary Care Treatable',
'NYU_NON_EM_2016 - NYU ED Utilization Algorithm: Non-Emergent',
'AAB_2020C - Avoidance of Antibiotic Treatment for Acute Bronchitis/Bronchiolitis (Total)',
'APC_TOTAL_2019 - Use of Multiple Concurrent Antipsychotics in Children and Adolescents (Total)',
'HDO_2020 - Use of Opioids at High Dosage',
'LBP_2020C - Use of Imaging Studies for Low Back Pain',
'UOP_NUM1_2020 - Use of Opioids from Multiple Providers (Multiple Prescribers)',
'UOP_NUM2_2020 - Use of Opioids from Multiple Providers (Multiple Pharmacies)',
'UOP_NUM3_2020 - Use of Opioids from Multiple Providers (Multiple Prescribers and Multiple Pharmacies)',
'URI_2020C - Appropriate Treatment for Upper Respiratory Infection',
'CWP_2020C - Appropriate Testing for Pharyngitis (Total)',
'IQI_21_TOTAL_2017 - Cesarean Delivery Rate, Uncomplicated (Overall)'
--'IQI_34_TOTAL_2017 - Vaginal Birth After Cesarean (VBAC) Rate, All (Overall)'
    					  )
AND DIM_DATE_EBM.YEARMO_NAME in ('{end_date}') --ebm end date 
  )
    )
 select distinct 
	*,
	n.adi_natrank,
	n.adi_staternk 
from milliman_data mm
left join race_data r on r.member_number = mm.member_number
left join hive.data_science_analytics.geocoded_members_parquet geo on geo.member_id = r.member_id
left join hive.data_science_analytics.ndi_parquet n on n.fips = geo.block_group 
order by 1,2'''.format(end_date = end_date)
    df =  pd.read_sql(query1, conn)
    return df

#specify the end date
# def filter_end_date(test_df, end_date):
#     mask = test_df['yearmo_name'].str.contains(end_date) 
#     test_df = test_df[mask]
#     return test_df

#add over/underuse col to the dataframe
def add_ebm_col(overuse, underuse, df):
    df['over/underuse'] = pd.np.where(df.ebm_measure_label.str.contains('|'. join(overuse)), "over",
                          pd.np.where(df.ebm_measure_label.str.contains('|'. join(underuse)), "under","NA"
                          ))
    return df

#convert datatype to categorical for over/underuse and ebm measure label: 
def convert_cat(df):
    df['over/underuse'] = df['over/underuse'].astype('category')
    df['ebm_measure_label'] = df['ebm_measure_label'].astype('category')
    return df 

#get the race porportion table
def race_prop_tab(df): 
    return df['predicted_race'].value_counts(normalize = True)

#create table: overuse/under use VS. race
def over_under_tab(df):
    g = df.groupby('over/underuse')

    #white:
    white_list = g.apply(lambda x: x[x['predicted_race'] == 'white']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'white']['denominator'].sum())

    #black:
    black_list = g.apply(lambda x: x[x['predicted_race'] == 'black']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'black']['denominator'].sum())

    #hispanic
    hispanic_list = g.apply(lambda x: x[x['predicted_race'] == 'hispanic']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'hispanic']['denominator'].sum())

    #api:
    api_list = g.apply(lambda x: x[x['predicted_race'] == 'api']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'api']['denominator'].sum())
    
    #aian:
    aian_list = g.apply(lambda x: x[x['predicted_race'] == 'aian']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'aian']['denominator'].sum())
    
    #2prace
    prace_list = g.apply(lambda x: x[x['predicted_race'] == '2prace']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == '2prace']['denominator'].sum())

    tab2_df = pd.DataFrame(np.array([[white_list[0], 
                                 black_list[0], 
                                 hispanic_list[0], 
                                 api_list[0], 
                                 aian_list[0], 
                                 prace_list[0]], #overuse
                                [white_list[1], 
                                 black_list[1], 
                                 hispanic_list[1], 
                                 api_list[1], 
                                 aian_list[1], 
                                 prace_list[1]]]),#underuse
                   columns=['white', 'black', 'hispanic', 'api', 'aian', '2prace'],
                   index = ['over', 'under'] )

    return tab2_df

def ebm_tab(df):
    g = df.groupby('ebm_measure_label')
    #white:
    white_list = g.apply(lambda x: x[x['predicted_race'] == 'white']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'white']['denominator'].sum())
    
    #black:
    black_list = g.apply(lambda x: x[x['predicted_race'] == 'black']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'black']['denominator'].sum())
    
    #hispanic
    hispanic_list = g.apply(lambda x: x[x['predicted_race'] == 'hispanic']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'hispanic']['denominator'].sum())
    
    #api:
    api_list = g.apply(lambda x: x[x['predicted_race'] == 'api']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'api']['denominator'].sum())
    
    #aian:
    aian_list = g.apply(lambda x: x[x['predicted_race'] == 'aian']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == 'aian']['denominator'].sum())
    
    #2prace
    prace_list = g.apply(lambda x: x[x['predicted_race'] == '2prace']['numerator'].sum()) / g.apply(lambda x: x[x['predicted_race'] == '2prace']['denominator'].sum())
    tab = pd.concat([white_list, black_list,hispanic_list, api_list, aian_list, prace_list], axis=1)
    tab.columns = ['White', 'Black', 'Hispanic', 'API', 'AIAN', '2prace']
    return tab




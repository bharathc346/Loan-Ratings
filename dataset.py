import argparse
import csv
import json
import random
from collections import defaultdict
from constants import MOODY_2_OBLIGOR, to_tier

# concacatenate csv files into one file
def concat_csv(in_files, out_file):
    total = []
    for i, in_file in enumerate(in_files):
        with open(in_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if i != 0 and line_count == 0:
                    line_count += 1
                else:
                    total.append(row)

    with open(out_file, 'w') as of:
        writer = csv.writer(of)
        for row in total:
            writer.writerow(row)

# turn csv file into json for readability
def to_json(in_files, out_file):
    ind_2_feature, total = {}, []
    for in_file in in_files:
        with open(in_file) as f:
            line_count = 0
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                temp = {}
                if line_count == 0:
                    for i in range(len(row)):
                        ind_2_feature[i] = row[i]
                else:
                    for i in range(len(row)):
                        temp[ind_2_feature[i]] = row[i]
                    total.append(temp)
                line_count += 1

    with open(out_file, 'w') as f:
        json.dump(total, f)

def sample_json(in_file, out_file):
    with open(in_file, 'r') as f:
        total = json.load(f)

    sample = []
    for i in range(10):
        sample.append(random.choice(total))

    with open(out_file, 'w') as f:
        json.dump(sample,f)

def gather_response(in_file, out_file):
    with open(in_file, 'r') as f:
        total = json.load(f)

    cleaned = []
    for entry in total:
        if entry['CUSTOMER_RATING_CD'] == '' or entry['CUSTOMER_CURRENT_OBLIGOR_RATING'] == '' or entry['FACILITY_LGD_RATING_CODE'] == '':
            continue
        fa_r = entry['FACILITY_LGD_RATING_CODE']
        ob_r = int(entry['CUSTOMER_CURRENT_OBLIGOR_RATING'])
        tier = to_tier(fa_r, ob_r)
        del entry['FACILITY_LGD_RATING_CODE']
        del entry['CUSTOMER_CURRENT_OBLIGOR_RATING']
        del entry['CUSTOMER_RATING_CD']
        entry['TIER'] = tier
        cleaned.append(entry)
    print(len(cleaned))

    with open(out_file, 'w') as f:
        json.dump(cleaned, f)

def predictor_dist(in_file, pred_name):
    with open(in_file, 'r') as f:
        total = json.load(f)

    temp = defaultdict(int)
    for entry in total:
        temp[entry[pred_name]] +=1

    print('Dist of {}:'.format(pred_name))
    print(temp)

def clean_for_regression(in_file, out_file):
    with open(in_file, 'r') as f:
        total = json.load(f)

    cleaned = []
    for entry in total:

        del entry['COLLATERAL_ID']
        del entry['SNAP_DT']
        del entry['FACILITY_ID']
        del entry['WCIS_CUSTOMER_ID']
        del entry['CUSTOMER_CURRENT_OBLIGOR_RATING_DATE']
        del entry['CUSTOMER_PREVIOUS_OBLIGOR_RATING']
        del entry['CUSTOMER_PROPOSED_OBLIGOR_RATING']
        del entry['CUSTOMER_CREDIT_RATING_AGENCY']
        del entry['CUSTOMER_POD_RATING_DESC']
        del entry['FACILITY_LGD_RATING_DATE']
        del entry['FACILITY_HIGHER_RISK_INDICATOR']
        del entry['FACILITY_TYPE_DESC']
        del entry['FACILITY_DEPT_LEVEL_5_DESC']
        del entry['VALUATION_DATE']
        del entry['LGD_SELECTED_VALUATION_IND']
        del entry['LGD_SELECTED_VALUATION_TYPE']
        del entry['HIGH_RISK_IDENTIFIED_DATE']
        del entry['HIGH_RISK_COLLATERAL_IND']
        del entry['OCCUPANCY']
        del entry['LEASE_AREA_TYPE']
        del entry['TOTAL_LEASE_AREA']
        del entry['NOI_STATEMENT_ID']
        del entry['OVERALL_CONDITION']
        del entry['PERCENT_UNDER_RENT_REG']
        del entry['PROPERTY_STREET']
        del entry['PROPERTY_ZIP_CODE']
        del entry['COLLATERAL_CATEGORY_CODE']
        del entry['COLLATERAL_CATEGORY']
        del entry['COLLATERAL_SUBCATEGORY_CODE']
        del entry['COLLATERAL_SUBCATEGORY']
        del entry['COLLATERAL_TYPE_CODE']
        del entry['COLLATERAL_TYPE_DESC']

        cleaned.append(entry)

    with open(out_file, 'w') as f:
        json.dump(cleaned, f)

def clean_empty_vals(in_file, out_file):
    with open(in_file, 'r') as f:
        total = json.load(f)

    cleaned = []
    for entry in total:
        if entry['LOAN_TO_VALUE'] == ' ':
            continue

        any_nan = False
        for key in entry:
            if entry[key] == "":
                any_nan = True
                break

        # data type conversions
        # entry['CUSTOMER_PREVIOUS_OBLIGOR_RATING'] = int(entry['CUSTOMER_PREVIOUS_OBLIGOR_RATING']) if entry['CUSTOMER_PREVIOUS_OBLIGOR_RATING'] else 0
        # # entry['CUSTOMER_PROPOSED_OBLIGOR_RATING'] = int(entry['CUSTOMER_PROPOSED_OBLIGOR_RATING']) if entry['CUSTOMER_PROPOSED_OBLIGOR_RATING'] else 0

        if entry['CUSTOMER_RISK_INDICATOR']:
            if entry['CUSTOMER_RISK_INDICATOR'] == 'N':
                entry['CUSTOMER_RISK_INDICATOR'] = 0
            else:
                entry['CUSTOMER_RISK_INDICATOR'] = 1

        # if entry['LGD_SELECTED_VALUATION_IND']:
        #     if entry['LGD_SELECTED_VALUATION_IND'] == 'No':
        #         entry['LGD_SELECTED_VALUATION_IND'] = 0
        #     else:
        #         entry['LGD_SELECTED_VALUATION_IND'] = 1

        entry['COLLATERAL_VALUE'] = float(entry['COLLATERAL_VALUE']) if entry['COLLATERAL_VALUE'] else 0
        if entry['LOAN_TO_VALUE']:
            if '%' in entry['LOAN_TO_VALUE']:
                entry['LOAN_TO_VALUE'] = float(entry['LOAN_TO_VALUE'][:entry['LOAN_TO_VALUE'].find('%')])
            else:
                entry['LOAN_TO_VALUE'] = entry['LOAN_TO_VALUE'].replace(',','.') if ',' in entry['LOAN_TO_VALUE'] else entry['LOAN_TO_VALUE']
                entry['LOAN_TO_VALUE'] = float(entry['LOAN_TO_VALUE'])

        entry['NOI'] = float(entry['NOI']) if entry['NOI'] else 0.0
        entry['ACTUAL_DSCR'] = float(entry['ACTUAL_DSCR']) if entry['ACTUAL_DSCR'] else 0.0
        entry['OS_LTV'] = float(entry['OS_LTV']) if entry['OS_LTV'] else 0.0
        entry['LTV_MPE'] = float(entry['LTV_MPE']) if entry['LTV_MPE'] else 0.0
        entry['OS_DEBTYIELD'] = float(entry['OS_DEBTYIELD']) if entry['OS_DEBTYIELD'] else 0.0
        entry['MPE_DEBTYIELD'] = float(entry['MPE_DEBTYIELD']) if entry['MPE_DEBTYIELD'] else 0.0

        flag = entry['NOI'] == 0.0 and entry['ACTUAL_DSCR'] == 0.0 and entry['OS_LTV'] == 0.0 and entry['LTV_MPE'] == 0.0 and entry['OS_DEBTYIELD'] == 0.0 and entry['MPE_DEBTYIELD'] == 0.0

        if not any_nan and not flag:
            cleaned.append(entry)

    #remove duplicates
    res_list = list({frozenset(item.items()) : item for item in cleaned}.values())

    print('Total of {} data points for regression'.format(len(res_list)))
    with open(out_file, 'w') as f:
        json.dump(res_list,f)

def to_csv(in_file, out_file):
    with open(in_file, 'r') as f:
        total = json.load(f)
    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['CUSTOMER_RISK_INDICATOR', 'COLLATERAL_VALUE', 'LOAN_TO_VALUE', 'NOI', 'ACTUAL_DSCR', 'OS_LTV', 'LTV_MPE', 'OS_DEBTYIELD', 'MPE_DEBTYIELD', 'TIER'])
        for entry in total:
            row = [
                # entry['CUSTOMER_PREVIOUS_OBLIGOR_RATING'],
                entry['CUSTOMER_RISK_INDICATOR'],
                # entry['LGD_SELECTED_VALUATION_IND'],
                entry['COLLATERAL_VALUE'],
                entry['LOAN_TO_VALUE'],
                entry['NOI'],
                entry['ACTUAL_DSCR'],
                entry['OS_LTV'],
                entry['LTV_MPE'],
                entry['OS_DEBTYIELD'],
                entry['MPE_DEBTYIELD'],
                entry['TIER']
            ]
            writer.writerow(row)

def sample_csv(in_file, out_file):
    total = []
    with open(in_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            total.append(row)

    count = 0
    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        while count < 3000:
            writer.writerow(random.choice(total))
            count += 1

def main():
    in_file = '/Users/bharathc/Desktop/Projects/Econometrics/all_years.json'
    out_file = '/Users/bharathc/Desktop/Projects/Econometrics/clean_regression_data.json'
    clean_for_regression(in_file, out_file)
    sample_file = '/Users/bharathc/Desktop/Projects/Econometrics/sample_regression.json'
    sample_json(out_file, sample_file)

    in_file = '/Users/bharathc/Desktop/Projects/Econometrics/clean_regression_data.json'
    out_file = '/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.json'
    clean_empty_vals(in_file, out_file)

    # predictor_dist(out_file, 'LGD_SELECTED_VALUATION_IND')

    in_file = '/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.json'
    out_file = '/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.csv'
    to_csv(in_file, out_file)

    # in_file = '/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.csv'
    # out_file = '/Users/bharathc/Desktop/Projects/Econometrics/sample_regression_data.csv'
    # sample_csv(in_file, out_file)


if __name__ == '__main__':
    main()

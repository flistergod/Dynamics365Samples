import logging
import azure. functions as func
from re import I
from pandas import json_normalize
from pandas import pivot_table
from pandas import DataFrame
from pandas import merge
from pandas import concat
from pulp import LpProblem
from pulp import LpVariable
from pulp import LpMinimize
from pulp import lpSum
from pulp import value
from requests import post


def processData(test_res_list, test_demand_list, test_preference_list, test_rotation_list, weeks):

    test_res = json_normalize(test_res_list)
    test_demand = json_normalize(test_demand_list)
    test_preference = json_normalize(test_preference_list)
    test_rotation = json_normalize(test_rotation_list)

    test_res['category'] = test_res['category'].str.lower()
    test_res.category = test_res.category.str.replace(' ','_')

    test_demand['category'] = test_demand['category'].str.lower()
    test_demand.category = test_demand.category.str.replace(' ','_')

    test_preference_always = test_preference[test_preference.type == 'Always']
    test_preference_specific = test_preference[test_preference.type == 'Specific']

    est_preference_always = test_preference_always.drop(['type','specific_start','specific_finish'], axis = 1)
    test_preference_specific = test_preference_specific.drop(['type'], axis = 1)

    test_preference_always = test_preference_always.fillna('-')
    test_preference_specific = test_preference_specific.fillna('-')

    model = LpProblem(name="shift_allocation", sense=LpMinimize)

    n_week = 1 # we can change it to any number for which we are trying to solve this problem
    test_days = list(test_demand.start.unique()) # Number of days coming from the data

    x = {(i,j,k,l):LpVariable(name="x{},{},{},{}".format(i,j,k,l), lowBound=0, cat="Binary")
            for i in (test_res.resource.unique()) 
            for j in (test_demand.category.unique()) 
            for k in (weeks)
            for l in (test_days)}

    r_al = {(i):LpVariable(name="r_al_{}".format(i), lowBound=0, cat="Integer")
        for i in (test_preference_always.resource_id)}

    r_al_sh = {(i,l):LpVariable(name="r_al_sh_{},{}".format(i,l), lowBound=0, cat="Integer")
        for i in (test_preference_always.resource_id)
        for l in (test_days)}

    r_sp = {(i):LpVariable(name="r_sp_{}".format(i), lowBound=0, cat="Integer")
        for i in (test_preference_specific.resource_id)}

    r_sp_sh = {(i,l):LpVariable(name="r_sp_sh_{},{}".format(i,l), lowBound=0, cat="Integer")
                for i in (test_preference_specific.resource_id)
                for l in (test_days)}

    for l in (test_days):
        for k in (test_demand.time_template.unique()):
            for i in (test_res.resource.unique()):
                temp_df = test_res[(test_res.resource == i)]
                model += lpSum([x[i,j,k,l] for j in (temp_df.category)]) <= 1

    for l in (test_days):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            model += lpSum([x[i,j,k,l] for j in (temp_df.category) for k in (test_demand.time_template.unique())]) <= 1

    for l in range(len(test_days)-1):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            #print(plp.lpSum([(x[i,j,'Day',test_days[l]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1)
            model += lpSum([(x[i,j,'Day',test_days[l]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1

    for l in range(len(test_days)-1):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            #print(plp.lpSum([(x[i,j,'Mid Morning',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1)
            model += lpSum([(x[i,j,'Mid Morning',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1

    for l in range(len(test_days)-1):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            #print(plp.lpSum([(x[i,j,'Mid Afternoon',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1)
            model += lpSum([(x[i,j,'Mid Afternoon',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1

    for l in range(len(test_days)-1):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            #print(plp.lpSum([(x[i,j,'Afternoon',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1)
            model += lpSum([(x[i,j,'Afternoon',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Night',test_days[l+1]]) for j in (temp_df.category)]) <= 1

    for l in range(len(test_days)-1):
        for i in (test_res.resource.unique()):
            temp_df = test_res[(test_res.resource == i)]
            #print(plp.lpSum([(x[i,j,'Night',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]]) for j in (temp_df.category)]) <= 1)
            model += lpSum([(x[i,j,'Night',test_days[l]] + x[i,j,'Day',test_days[l+1]] + x[i,j,'Mid Morning',test_days[l+1]] + x[i,j,'Mid Afternoon',test_days[l+1]] + x[i,j,'Afternoon',test_days[l+1]]) for j in (temp_df.category)]) <= 1

    for i in (test_res.resource.unique()):
        temp_df = test_res[(test_res.resource == i)]
        model += lpSum([x[i,j,k,l] for l in (test_demand.start.unique())
                            for k in (test_demand.time_template.unique()) for j in (temp_df.category)]) <= 5
                            
    for l in (test_days):
        temp_df = test_demand #previous -> temp_df = test_demand[test_demand.start == l]
        res_demand_cnt = pivot_table(temp_df, values='start', index=['category'],
                        columns=['time_template'], aggfunc='count')
        res_demand_cnt = res_demand_cnt.fillna(0)
        for k in (test_demand.time_template.unique()):
            for j in (test_demand.category.unique()):
                temp_df = test_res[(test_res.category == j)]
                model += lpSum([x[i,j,k,l] for i in (temp_df.resource)])-res_demand_cnt.loc[j,k] <= 0

    for i in (test_preference_always.resource_id):
        temp_df = test_res[(test_res.resource == i)]
        off_day_idx = test_preference_always[test_preference_always.resource_id == i].iloc[0,2].split(',')
        off_day = []
        if off_day_idx[0] == '-':
            continue
        else:        
            for idx in range(len(off_day_idx)):
                off_day.append(test_days[int(off_day_idx[idx])])
        model += lpSum([x[i,j,k,l] for l in (off_day)
                                for k in (test_demand.time_template.unique()) for j in (temp_df.category)]) == r_al[i]

    for l in (test_days):
        for i in (test_preference_always.resource_id):
            temp_df = test_res[(test_res.resource == i)]
            non_pref_sh = []
            if test_preference_always[test_preference_always.resource_id == i].iloc[0,3] == '-':
                continue
            else:
                for npsh in (test_demand.time_template.unique()):
                    if test_preference_always[test_preference_always.resource_id == i].iloc[0,3] == npsh:
                        continue
                    else:
                        non_pref_sh.append(npsh)
            model += lpSum([x[i,j,k,l] for k in (non_pref_sh) for j in (temp_df.category)]) == r_al_sh[i,l]

    for i in (test_preference_specific.resource_id):
        temp_df = test_res[(test_res.resource == i)]
        off_day_idx = test_preference_specific[test_preference_specific.resource_id == i].iloc[0,2].split(',')
        off_day = []
        if off_day_idx[0] == '-':
            continue
        else:        
            for idx in range(len(off_day_idx)):
                off_day.append(test_days[int(off_day_idx[idx])])
        model += lpSum([x[i,j,k,l] for l in (off_day)
                                for k in (test_demand.time_template.unique()) for j in (temp_df.category)]) == r_sp[i]

    for i in (test_preference_specific.resource_id):
        temp_df = test_res[(test_res.resource == i)]
        spec_start = list(test_preference_specific[test_preference_specific.resource_id == i].specific_start)
        spec_end = list(test_preference_specific[test_preference_specific.resource_id == i].specific_finish)
        start_idx = test_days.index(spec_start[0])
        end_idx = test_days.index(spec_end[0])
        test_days_new = []
        for idx in range(end_idx - start_idx + 1):
            test_days_new.append(test_days[idx])
        for l in test_days_new:
            non_pref_sh = []
            if test_preference_specific[test_preference_specific.resource_id == i].iloc[0,3] == '-':
                continue
            else:
                for npsh in (test_demand.time_template.unique()):
                    if test_preference_specific[test_preference_specific.resource_id == i].iloc[0,3] == npsh:
                        continue
                    else:
                        non_pref_sh.append(npsh)
            model += lpSum([x[i,j,k,l] for k in (non_pref_sh) for j in (temp_df.category)]) == r_sp_sh[i,l]
    ###
    for l in test_days:
        for i in test_rotation.resource:
            sh = test_rotation[test_rotation.resource == i].iloc[0,2]
            temp_df = test_res[(test_res.resource == i)]
            non_pref_sh = []
            for npsh in (test_demand.time_template.unique()):
                if sh == npsh:
                    continue
                else:
                    non_pref_sh.append(npsh)
            model += lpSum([x[i,j,k,l] for k in (non_pref_sh) for j in (temp_df.category)]) == 0

    sh = 0
    for l in (test_days):
        temp_df = test_demand #previous -> temp_df = test_demand[test_demand.start == l]
        res_demand_cnt = pivot_table(temp_df, values='start', index=['category'],
                        columns=['time_template'], aggfunc='count')
        res_demand_cnt = res_demand_cnt.fillna(0)
        for k in (test_demand.time_template.unique()):
            for j in (test_demand.category.unique()):
                temp_df = test_res[(test_res.category == j)]
                sh_k = res_demand_cnt.loc[j,k]-lpSum([x[i,j,k,l] for i in (temp_df.resource)])
                sh = sh + sh_k
                model += 2*sh + lpSum([r_al[i] for i in (test_preference_always.resource_id)]) + lpSum([r_al_sh[i,l] for i in (test_preference_always.resource_id) for l in (test_days)]) + lpSum([r_sp[i] for i in (test_preference_specific.resource_id)]) + lpSum([r_sp_sh[i,l] for i in (test_preference_specific.resource_id) for l in (test_days)])

    model.solve()
    value(model.objective)

    for v in model.variables():
        if v.varValue>0:
            print(v.name, "=", v.varValue)

    out = []
    res = []
    cat = []
    shift = []
    date = []
    for l in test_demand.start.unique():
        for k in test_demand.time_template.unique():
            for j in test_demand.category.unique():
                temp_df = test_res[(test_res.category == j)]
                #print(temp_df)
                for i in temp_df.resource.unique():
                    #print(x[i,j,k,l])
                    for v in model.variables():
                        #print(v.name)
                        if str(x[i,j,k,l]) == str(v.name):
                            res.append(i)
                            cat.append(j)
                            shift.append(k)
                            date.append(l)
                            out.append(v.varValue)
                        else:
                            continue

    out_df = DataFrame(list(zip(res, cat, shift, date, out)), columns =['allocated_resource', 'category', 'shift', 'date', 'val'])

    out_df = out_df[out_df['val'] != 0]
    out_df = out_df.reset_index(drop=True)

    out_df = out_df.sort_values(by = ['date', 'category'], ascending = [True, True])

    out_df = out_df.drop(['val'], axis = 1)

    #out_df.to_csv('../data/out_shift.csv')
    out_df_json = out_df.to_json(orient = 'records')
    final_df = DataFrame()
    shift_id = []
    res_id = []
    for l in out_df.date.unique():
        for k in out_df['shift'].unique():
            for j in out_df.category.unique():
                temp_shift = test_demand[(test_demand.category == j) & (test_demand.time_template == k) & (test_demand.start == l)].shift_id
                temp_shift = temp_shift.reset_index(drop=True)
                #print(temp_shift)
                temp_df = out_df[(out_df.category == j) & (out_df['shift'] == k) & (out_df.date == l)].allocated_resource
                temp_df = temp_df.reset_index(drop=True)
                #print(temp_df.allocated_resource)
                concatenated = concat([temp_shift, temp_df], axis=1)
                final_df = concat([final_df,concatenated],axis = 0)

    final_df = final_df.fillna('-')

    final_df = merge(test_demand, final_df, on="shift_id", how="left")
    final_df_json = final_df.to_json(orient = 'records')
    
    url='https://prod-112.westus.logic.azure.com:443/workflows/c20b16e84c60488398fd51a63ccbfcf1/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=6cKFwqSehs9ianUaGDrp9w4BUBWL6Dn8aJlONiCzRUg'
    #body={"data":final_df_json}
    body = final_df_json
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*"
        }
    r=post(url,data=body, headers=headers)
    #final_df.to_csv('../data/allocation_nonove~
    # rtime.csv')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging. info('Python HTTP trigger function processed a request.')
   
    test_res_list  = req. params.get('test_res_list')
    test_demand_list  = req. params.get('test_demand_list')
    test_preference_list  = req. params.get('test_preference_list')
    test_rotation_list  = req. params.get('test_rotation_list')
    weeks  = req. params.get('weeks')

    if not(test_res_list or test_demand_list or test_preference_list or test_rotation_list or weeks):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            test_res_list = req_body.get('test_res_list')
            test_demand_list = req_body.get('test_demand_list')
            test_preference_list = req_body.get('test_preference_list')
            test_rotation_list = req_body.get('test_rotation_list')
            weeks = req_body.get('weeks')
    
    if (test_res_list and test_demand_list and test_preference_list and test_rotation_list and weeks):

        processData(test_res_list, test_demand_list, test_preference_list, test_rotation_list, weeks)
        return func.HttpResponse(f"Data will be sent via POST", status_code=200)

    else:
        return func.HttpResponse("Please pass the correct parameters the query string or in the request body",status_code=400)
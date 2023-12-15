from database import mongodb_config
from pymongo import MongoClient
import certifi
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import base64
import json


def connect_to_mongodb(connection_string):
    try:
        #client = MongoClient(connection_string, tlsCAFile=certifi.where())
        client = MongoClient(mongodb_config.conn_str)
    except Exception as e:
        print("Not able to connect to MongoDb at this moment")
        print(e)
    return client

def get_distinct(collection):
    try:
        distinct_val_list_client = []
        distinct_val_list_domain = []
        distinct_val_list_pillar = []
        distinct_val_list_lever = []
        distinct_val_list_variables = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        distinct_val_list_client = collection_obj.distinct("client")
        distinct_val_list_domain = collection_obj.distinct("domain")
        distinct_val_list_pillar = collection_obj.distinct("pillar")
        distinct_val_list_lever = collection_obj.distinct("lever")
        distinct_val_list_variables = collection_obj.distinct("variables")
    except Exception as e:
        print(e)
    return distinct_val_list_client,distinct_val_list_domain,distinct_val_list_pillar,distinct_val_list_lever,distinct_val_list_variables

def get_distinct_values(collection,field):
    try:
        distinct_val_list = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        distinct_val_list = collection_obj.distinct(field)
    except Exception as e:
        print(e)
    return distinct_val_list

def insert_one_doc(collection,data):
    try:
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        collection_obj.insert_one(data)
    except Exception as e:
        print(e)
    return True

def insert_many_doc(collection,data):
    try:
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        collection_obj.insert_many(data)
    except Exception as e:
        print(e)
        return False
    return True

def update_one_doc(collection,filter_dict,updated_data_dict):
    try:
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        collection_obj.update_one(
            filter_dict,
            {"$set": updated_data_dict},
            upsert=False
        )
    except Exception as e:
        print(e)
    return True

def delete_one_doc(collection,query):
    try:
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        myquery = query
        collection_obj.delete_one(myquery)
    except Exception as e:
        print(e)
    return True


def get_user_collection_dump():
    try:
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["user"]
        data = collection_obj.find({},
                                    {
                                        "_id":0,
                                        "password":0,
                                        #'user_unique_id':0
                                    }
                                )
    except Exception as e:
        print(e)
    return list(data)

def get_pillar_collection_dump(query={}):
    try:
        returned_data = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["pillar"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            returned_data = list(data)
        else:
            data = [{'pillar_unique_id': '', 'pillar_name': '', 'pillar_weightage': ''}]
            returned_data = data
    except Exception as e:
        print(e)
    return returned_data

def get_lever_collection_dump(query={}):
    try:
        returned_data = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["lever"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            returned_data = list(data)
        else:
            data = [{'lever_unique_id': '', 'lever_name': '', 'pillar_name': ''}]
            returned_data =  data
    except Exception as e:
        print(e)
    return returned_data

def get_variable_collection_dump(query={}):
    try:
        returned_data = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["variable"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            returned_data = list(data)
        else:
            data = [{'variable_unique_id': '', 'variable_name': '', 'lever_name': ''}]
            returned_data = data
        #print(data)
    except Exception as e:
        print(e)
    return returned_data

def get_question_collection_dump(query={}):
    try:
        returned_data = []
        data_dict = {}
        data_list=[]
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["question"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            for d in data:
                data_dict = d
                data_dict["options"] = json.dumps(d["options"])
                data_dict["option_internal_score"] = json.dumps(d["option_internal_score"])
                data_dict["option_absolute_score"] = json.dumps(d["option_absolute_score"])
                data_list.append(data_dict)
            returned_data = data_list
        else:
            data = [{'question_text': '', 'variable_name': '' , 'question_type': '', 'no_of_options': '', 'options': '[]', 'option_absolute_score': '[]', 'option_internal_score': '[]', 'question_group': '', 'question_group_primary_member': '','doc_upload_flag': '','question_unique_id': '','weightage': ''}]
            returned_data =  data
    except Exception as e:
        print(e)
    return returned_data

def get_assessment_collection_dump(query={}):
    try:
        returned_data = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["survey_dtl"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            returned_data = list(data)
        else:
            data = [{'survey_unique_id': '', 'status': '', 'survey_name': '', 'template_name': '', 'pillar': '', 'lever': '', 'variable': '', 'question_text': '', 'question_unique_id': ''}]
            returned_data =  data
    except Exception as e:
        print(e)
    return returned_data
    

def get_assessment_template_collection_dump(query={}):
    try:
        data_dict = {}
        data_list=[]
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["template"]
        item_count = collection_obj.count_documents({})
        if item_count > 0:
            data = collection_obj.find(query,
                                        {
                                            "_id":0,
                                        }
                                    )
            #print(data)
            for d in data:
                data_dict = d
                data_dict["associated_levers"] = json.dumps(d["associated_levers"])
                data_list.append(data_dict)
            return data_list
        else:
            data = [{'template_unique_id': '', 'template_name': '', 'associated_levers': '[]'}]
            return data
    except Exception as e:
        print(e)

def is_user_id_unique(user_id):
    try:
        is_user_id_unique = True
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["user"]
        user_dtl = collection_obj.aggregate([
                        {'$match': {
                            '$and' : [
                                 {'user_id': user_id}
                            ]
                        }}
                    ])
        for user in user_dtl:
            #print(user)
            is_user_id_unique = False
        #print(is_user_id_unique)
    except Exception as e:
        print(e)
    return is_user_id_unique

def get_user_role(user_id):
    try:
        user_role = ""
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["user"]
        user_dtl = collection_obj.aggregate([
                        {'$match': {
                            '$and' : [
                                 {'user_id': user_id}
                            ]
                        }}
                    ])
        for user in user_dtl:
            #print(user)
            user_role = user["user_type"]
        #print(user_role)
    except Exception as e:
        print(e)
    return user_role

def user_exists(username, password):
    try:
        user_exists = False
        user_type=""
        #print(base64.b64decode(password))
        #client = MongoClient(mongodb_config.conn_str)
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection = db["user"]
        user_dtl = collection.aggregate([
                        {'$match': {
                            '$and' : [
                                 {'user_id': username},
                                 {'password': password}
                            ]
                        }}
                    ])
        for user in user_dtl:
            #print(user)
            user_type = user["user_type"]
            user_exists = True
        return user_exists,user_type
    except Exception as e:
        print(e)

def create_table_from_df(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col.upper()) for col in columns]+[html.Th("ACTION")])]
    rows = [
        html.Tr(
            [html.Td(cell) for cell in row] + [
                html.Td(
                        dbc.DropdownMenu(
                                label="Action",
                                size="sm",
                                children=[
                                    dbc.DropdownMenuItem("Edit",id={"user_unique_id": row[1],"action":"edit"}),
                                    dbc.DropdownMenuItem("Delete",id={"user_unique_id": row[1],"action":"delete"}),
                                ],
                            ),
                    )
            ]
        ) for row in values
    ]
    table = [
        html.Thead(header,style={"backgroundColor":"PaleTurquoise"}), 
        html.Tbody(rows)
    ]
    #print(rows)
    return table


def get_distinct_survey_id():
    try:
        distinct_val_list = []
        client = connect_to_mongodb(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db["survey_dtl"]
        distinct_val_list = collection_obj.distinct("survey_unique_id")
    except Exception as e:
        print(e)
    return distinct_val_list


def get_survey_questions(collection,client_dd_val,domain_dd_val):
    try:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        collection_obj = db[collection]
        data = collection_obj.find({
                                        "client": { '$in' : [client_dd_val] },
                                        "domain": { '$in' : [domain_dd_val] },
                                        #"pillar": { '$in' : [pillar_dd_val] },
                                        #"lever": { '$in' : [lever_dd_val] },
                                        #"variable": { '$in' : [variable_dd_val] }
                                    },
                                    {
                                        "_id":0,
                                        "options":0,
                                        "option_internal_score":0,
                                        "option_absolute_score":0,
                                        "question_type":0,
                                        "doc_upload_flag":0,
                                        "weightage":0,
                                        "options_count":0
                                    }
                                )
        #print(list(data))
    except Exception as e:
        print(e)
    return list(data)


def get_survey_dtls(survey_id):
    try:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        survey_dtl_collection_obj = db["survey_dtl"]
        pipeline = [
                    { '$match': {"survey_unique_id": str(survey_id)} },
                    { 
                        '$lookup': {
                        'from': 'question',
                        'localField': 'question_unique_id',
                        'foreignField': 'question_unique_id',
                        'as': 'question'
                        }
                    },
                    {'$unwind': {'path': '$question','preserveNullAndEmptyArrays': True}},
                    { 
                        '$lookup': {
                        #'from': 'survey_score',
                        'from': 'survey_response',
                        'pipeline' : [{ '$match': {"survey_unique_id": str(survey_id)} }],
                        'localField': 'question_unique_id',
                        'foreignField': 'question_unique_id',
                        'as': 'question_scores'
                        }
                    },
                    {'$unwind': {'path': '$question_scores','preserveNullAndEmptyArrays': True}},
                    ]
        surveys_coll_aggr=survey_dtl_collection_obj.aggregate(pipeline)
        #print(list(surveys_coll_aggr))
    except Exception as e:
        print(e)
    return list(surveys_coll_aggr)



def get_survey_progress(survey_id):
    try:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        survey_dtl_collection_obj = db["survey_dtl"]
        overall_progress_percent = 0
        returned_dict = {}
        #survey_score_collection_obj = db["survey_score"]
        survey_response_collection_obj = db["survey_response"]
        total_survey_questions=survey_dtl_collection_obj.count_documents({"survey_unique_id": str(survey_id)})
        total_survey_answered=survey_response_collection_obj.count_documents({"survey_unique_id": str(survey_id)})
        overall_progress_percent = (total_survey_answered/total_survey_questions) * 100
        returned_dict["overall_progress_percent"] = round(overall_progress_percent,2)
        for pillar in ["Environment", "Social","Governance"]:
            number_of_survey_questions = survey_dtl_collection_obj.count_documents({"survey_unique_id": str(survey_id),'pillar': str(pillar)})
            pipeline = [
                    { '$match': {"survey_unique_id": str(survey_id)} },
                    { 
                        '$lookup': {
                        'from': 'survey_dtl',
                        'localField': 'question_unique_id',
                        'foreignField': 'question_unique_id',
                        'as': 'surveydtl'
                        }
                    },
                    {'$unwind': {'path': '$surveydtl','preserveNullAndEmptyArrays': True}},
                    ]
            survey_question_answered=survey_response_collection_obj.aggregate(pipeline)
            #print(list(survey_question_answered))
            number_of_survey_question_answered = len([q  for q in list(survey_question_answered) if q["surveydtl"]["pillar"] == pillar])
            #print("{} {}".format(pillar,number_of_survey_question_answered))
            if number_of_survey_questions ==0:
                progress_percent = 100
            else:
                progress_percent = (number_of_survey_question_answered/number_of_survey_questions) * 100
            returned_dict[pillar+"_progress_percent"] = round(progress_percent,2)
        #print(returned_dict)
    except Exception as e:
        print(e)
    return returned_dict


def get_max_possible_scores(survey_id):
    #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
    client = connect_to_mongodb(mongodb_config.conn_str)
    #client = MongoClient(mongodb_config.conn_str)
    db = client["esg"]
    survey_dtl_collection_obj = db["survey_dtl"]
    returned_dict_pillars = {}
    returned_dict_levers = {}
    e_score = 0
    s_score = 0
    g_score = 0
    total_possible_score = 0
    pipeline = [
                { '$match': {"survey_unique_id": str(survey_id)} },
                { 
                    '$lookup': {
                    'from': 'question',
                    'localField': 'question_unique_id',
                    'foreignField': 'question_unique_id',
                    'as': 'question'
                    }
                },
                {'$unwind': {'path': '$question','preserveNullAndEmptyArrays': True}},
                ]
    surveys_coll_aggr=survey_dtl_collection_obj.aggregate(pipeline)
    question_dtl_list = list(surveys_coll_aggr)
    for q in question_dtl_list:
        if q['question']['question_type'] == "multi_select":
            total_possible_score = sum([float(o) for o in  q['question']['option_absolute_score']])
            #total_possible_score = max([float(o) for o in  q['question']['option_absolute_score']])
        if q['question']['question_type'] == "single_select":
            total_possible_score = sum([float(o) for o in  q['question']['option_absolute_score']])
            #total_possible_score = max([float(o) for o in  q['question']['option_absolute_score']])

        total_possible_score = total_possible_score * float(q["weightage"])

        if q['pillar'] == 'Environment':
            e_score += total_possible_score
        if q['pillar'] == 'Social':
            s_score += total_possible_score
        if q['pillar'] == 'Governance':
            g_score += total_possible_score 
        
        if q['pillar'] + "###" +q['lever'] in returned_dict_levers:
            returned_dict_levers[q['pillar'] + "###" +q['lever']] = float(returned_dict_levers[q['pillar'] + "###" +q['lever']]) + total_possible_score
        else:
            returned_dict_levers[q['pillar'] + "###" +q['lever']] = total_possible_score

    returned_dict_pillars["e_possible_score"] = e_score
    returned_dict_pillars["s_possible_score"] = s_score
    returned_dict_pillars["g_possible_score"] = g_score

    return returned_dict_pillars, returned_dict_levers
def get_df_from_jsons(path):
    import  json
    path = path
    file_list = [file for file in os.listdir(path) if file.endswith(".json")]
    all_data = []
    for f_name in file_list:
        with open(path + "/" + f_name) as json_files:
            json_data = json.load(json_files)
            all_data.append(json_data)
    #creating function which takes a json file and converts it to a dataframe       
    def json_df(json_data):
        df_1 =  json_normalize(json_data.get(list(json_data.keys())[0]))
        main_keys = []
        value_list = []
        for k, v in json_data.get(list(json_data.keys())[1]).items():
            main_keys.append(k)
            value_list.append(v)
            df = pd.DataFrame(value_list)
            df.index = main_keys
        val = df_1["2. Symbol"].values
        df['symbol'] = val[0]
        return df

    all_json = []
    for json in all_data:
        j = json_df(json)
        all_json.append(j)
    #gives df of all companies together
    my_df_all = pd.concat(all_j)
    return my_df_all

import yaml

with open('params.yml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    params_list = yaml.load(file, Loader=yaml.FullLoader)

    print(params_list)


# with open('_variables.yml') as file:
#     # The FullLoader parameter handles the conversion from YAML
#     # scalar values to Python the dictionary format
#     params_list = yaml.load(file, Loader=yaml.FullLoader)

#     print(params_list)   


#writing

dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
{'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

with open('new_file.yml', 'w') as file:
    documents = yaml.dump(dict_file, file)

new_dict = { "Validation" :{
                "Size": 1920,
                "Auto": "75.84%",
                "Features": 70,
                "Purpose": "Hyperparameter tuning"
                }
            }

with open('params.yml', 'a') as file:
    file.write("\n")
    documents = yaml.dump(new_dict, file)    
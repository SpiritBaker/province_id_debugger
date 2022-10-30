
import os
import re
from pathlib import Path


terrain_file_path = Path("map/terrain.txt")
continent_file_path = Path("map/continent.txt")
area_file_path = Path("map/area.txt")
trade_nodes_file_path = Path("common/tradenodes/00_tradenodes.txt")
province_history_path = Path("history/provinces/")
default_file_path = Path("map/default.map")
definition_file_path = Path("map/definition.csv")
positions_file_path = Path("map/positions.txt")
climate_file_path = Path("map/climate.txt")
localisation_file_path = Path("localisation")

terrain_present = terrain_file_path.is_file()
continent_present = continent_file_path.is_file()
area_present = area_file_path.is_file()
trade_nodes_present = trade_nodes_file_path.is_file()
default_present = default_file_path.is_file()
definition_present = definition_file_path.is_file()
positions_present = positions_file_path.is_file()
climate_present = climate_file_path.is_file()
province_history_present = province_history_path.is_dir()
localisation_present = province_history_path.is_dir()

# Unused
terrain_id = []
continent_id = []
area_id = []
trade_nodes_id = []
# To form a filter list
wasteland_id = []
sea_or_lake_id = []


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def definition_file():
    province_id = []
    comment = '#'
    province = "province;red;green;blue;x;x"
    semicolon = ";"
    path = definition_file_path
    with open(path) as file:
        while line := file.readline().rstrip().replace('\t', '').replace('\n', '').replace(' ', ''):
            line = line.split(comment, 1)[0].replace(province, "").removesuffix(";")
            id_line = line.split(semicolon, 1)[0].split('\n')
            province_id += id_line
    return province_id


def definition_file_input():
    definition_names = []
    comment = '#'
    province = "province;red;green;blue;x;x"
    path = definition_file_path
    with open(path) as file:
        while line := file.readline().rstrip().replace('\t', '').replace('\n', '').replace(' ', ''):
            line = line.split(comment, 1)[0].replace(province, "").removesuffix(";").replace(";", " ")
            id_line = line.split('\n')
            id_line[:] = [x for x in id_line if x]
            definition_names += id_line
    return definition_names


def position_file():
    province_id = []
    path = positions_file_path
    with open(path, "r") as f:
        for line in f:
            if re.match(r"^\d+.*$", line):  # Searching for lines that start with a number
                line = line.split('=', 1)[0].replace('\t', '').replace('\n', '').replace(' ', '')
                temp_line = str(line).rstrip('\n').strip().split()
                province_id += temp_line
                #print(temp_line)
    return province_id


def terrain_file():
    province_id = []
    start = 'terrain_override = {'
    end = '}'
    path = terrain_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    province_id += temp_line
    return province_id


def continent_file():
    province_id = []
    start = '{'
    end = '}'
    path = continent_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    province_id += temp_line
    return province_id

    
def area_file():
    province_id = []
    start = '{'
    end = '}'
    path = area_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    province_id += temp_line
    return province_id
    

def trade_nodes_file():
    province_id = []
    start = 'members={'
    end = '}'
    path = trade_nodes_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    province_id += temp_line
    return province_id


def sea_tile():
    global sea_or_lake_id
    start_sea = 'sea_starts = {'
    end = '}'
    path = default_file_path
    found_type = False
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            if start_sea in line.strip():
                found_type = True
                continue

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    sea_id = []
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split()
                    sea_id += temp_line
                    sea_or_lake_id += sea_id
    return sea_or_lake_id


def lake_tile():
    global sea_or_lake_id
    start_lake = 'lakes = {'
    end = '}'
    path = default_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line1 in f:
            if start_lake in line1.strip():
                found_type = True
                continue

            if found_type:
                if end in line1.strip():
                    found_type = False
                else:
                    comment = '#'
                    lake_id = []
                    line1 = line1.split(comment, 1)[0]
                    temp_line1 = str(line1).rstrip('\n').strip().split()
                    lake_id += temp_line1
                    sea_or_lake_id += lake_id
    return sea_or_lake_id


def wasteland():
    global wasteland_id
    start = 'impassable = {'
    end = '}'
    path = climate_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split()
                    wasteland_id += temp_line
    return wasteland_id


def localisation_files(localisation_file_path):
    folder = localisation_file_path
    files = os.listdir(folder)
    keyword = ' PROV'
    id_line = []
    for file in files:
        if os.path.isfile(os.path.join(folder, file)):
            f = open(os.path.join(folder, file), 'r', encoding='utf-8-sig')
            for line in f:
                if keyword in line and line.startswith(keyword):
                    line = line.split('PROV_', 1)[0].split('PROVINCE', 1)[0].split('PROVIRO_', 1)[0].split('PROVINCIAL', 1)[0].replace('\t', '').replace('\n', '')
                    line = line.replace('"', '').replace("'", '').replace(' ', '').removeprefix("PROV").replace(':0', ' ').replace(':1', ' ').replace(':', ' ')
                    line = line.split()
                    line[:] = [x for x in line if x]
                    id_line += line
            f.close()
    return id_line


def localisation_file_input(localisation_file_path):
    folder = localisation_file_path
    files = os.listdir(folder)
    localisation_list = []
    keyword = ' PROV'
    for file in files:
        if os.path.isfile(os.path.join(folder, file)):
            f = open(os.path.join(folder, file), 'r', encoding='utf-8-sig')
            for line in f:
                if keyword in line and line.startswith(keyword):
                    line = line.split('PROV_', 1)[0].split('PROVINCE', 1)[0].split('PROVIRO_', 1)[0].split('PROVINCIAL', 1)[0].replace('\t', '').replace('\n', '')
                    line = line.replace('"', '').removeprefix(" PROV").replace(':0', ' ').replace(':1', ' ').replace(':', ' ')
                    temp_line = line.split('\n')
                    temp_line[:] = [x for x in temp_line if x]
                    localisation_list += temp_line
            f.close()
    return localisation_list


# Getting File names from history/provinces
def province_history_files(province_history_path):
    province_history_names = [f.name for f in os.scandir(province_history_path) if f.is_file()]
    province_history_id = [x[:4].replace('-', '').replace(' ', '') for x in province_history_names]
    return province_history_id


# For saving history/provinces names into a separate file
def province_history_files_name(province_history_path):
    province_history_names = [f.name for f in os.scandir(province_history_path) if f.is_file()]
    province_history_names = [x.replace('-', '').replace('.txt', '') for x in province_history_names]
    return province_history_names


def find_duplicate(province_id):
    duplicate = []
    uniques = []
    for number in province_id:
        if number not in uniques:
            uniques.append(number)
        else:
            duplicate.append(number)
    return duplicate


# filtering Wasteland, Sea tiles and Lakes
def filter_list(province_history_id):
    compare_list = sea_or_lake_id + wasteland_id
    province_history_id = [x for x in province_history_id if x not in compare_list]
    return province_history_id


# used for Filtering loc
def integer_filter(id_line):
    province_id = [token for token in id_line if all(char.isdigit() or char == int for char in token)]
    return province_id


# Missing id's
def missing_province_id(province_history_id,province_id):
    missing_id = list(set(province_history_id).difference(province_id))
    return missing_id


if default_present is True:
    sea_tile()
    lake_tile()
if climate_present is True:
    wasteland()


if province_history_present is True:
    province_history_id = province_history_files(province_history_path)
    print("Loading File names from history/provinces/")
    if definition_present is True:
        province_id = definition_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(missing_province_id(province_history_id, province_id))
        print(f"Definition.csv Missing id:{missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if positions_present is True:
        province_id = position_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(missing_province_id(province_history_id, province_id))
        print(f"Position.csv Missing id:{missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if terrain_present is True:
        province_id = terrain_file()
        terrain_id = terrain_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Terrain.txt Missing id:{missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        province_id = continent_file()
        continent_id = continent_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Continent.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        province_id = area_file()
        area_id = area_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id,province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Area.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        province_id = trade_nodes_file()
        trade_nodes_id = trade_nodes_file()
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"TradeNodes.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if localisation_present is True:
        id_line = localisation_files(localisation_file_path)
        province_id = integer_filter(id_line)
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Localisation Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    else:
        pass
if province_history_present is False:
    if definition_present is True:
        province_id = definition_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Definition.csv Duplicate id:{duplicate}{os.linesep}")
    if positions_present is True:
        province_id = position_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Position.csv Duplicate id:{duplicate}{os.linesep}")
    if terrain_present is True:
        province_id = terrain_file()
        terrain_id = terrain_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Terrain.txt Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        province_id = continent_file()
        continent_id = continent_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Continent.txt Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        province_id = area_file()
        area_id = area_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Area.txt Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        province_id = trade_nodes_file()
        trade_nodes_id = trade_nodes_file()
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"TradeNodes.txt Duplicate id:{duplicate}{os.linesep}")
    if localisation_present is True:
        id_line = localisation_files(localisation_file_path)
        province_id = integer_filter(id_line)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Localisation Duplicate id:{duplicate}{os.linesep}")
    else:
        pass
else:
    pass

input_a = input("To print all history/province id's type: 'id', 'name', 'loc', 'def'\nTo Save to a txt file type: 'save id', "
                "'save name', 'save loc', 'save def'\n")

if input_a == "name":
    province_history_names = province_history_files_name(province_history_path)
    province_history_names = str(natural_sort(province_history_names))
    print(province_history_names)

if input_a == "id":
    province_history_id = province_history_files(province_history_path)
    province_history_id = str(natural_sort(province_history_id))
    print(province_history_id)

if input_a == "loc":
    localisation_list = str(natural_sort(localisation_file_input(localisation_file_path)))
    print(localisation_list)

if input_a == "def":
    definition_names = str(natural_sort(definition_file_input()))
    print(definition_names)

if input_a == "save loc":
    localisation_list = str(natural_sort(localisation_file_input(localisation_file_path)))
    with open('loc_names.txt', 'w', encoding='utf8') as output:
        output.write(localisation_list)
    print("Saved")

if input_a == "save name":
    province_history_names = province_history_files_name(province_history_path)
    province_history_names = str(natural_sort(province_history_names))
    with open('province_names.txt', 'w', encoding='utf8') as output:
        output.write(province_history_names)
    print("Saved")

if input_a == "save id":
    province_history_id = province_history_files(province_history_path)
    province_history_id = str(natural_sort(province_history_id))
    with open('province_id.txt', 'w', encoding='utf8') as output:
        output.write(province_history_id)
    print("Saved")

if input_a == "save def":
    definition_names = str(natural_sort(definition_file_input()))
    with open('definition.txt', 'w', encoding='utf8') as output:
        output.write(definition_names)
    print("Saved")
else:
    pass

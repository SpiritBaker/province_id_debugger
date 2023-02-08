
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


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def definition_file():
    province_id = []
    definition_names = []
    comment = '#'
    province = "province;red;green;blue;x;x"
    semicolon = ";"
    path = definition_file_path
    with open(path) as file:
        while line := file.readline().rstrip().replace('\t', '').replace('\n', '').replace(' ', ''):
            line = line.split(comment, 1)[0].replace(province, "").removesuffix(";")
            id_line = line.split(semicolon, 1)[0].split('\n')
            province_id += id_line
            line = line.replace(";", " ")
            name_line = line.split('\n')
            name_line = [x for x in name_line if x]
            definition_names += name_line
    return province_id, definition_names


def position_file():
    province_id = []
    path = positions_file_path
    with open(path, "r") as f:
        for line in f:
            if re.match(r"^\d+.*$", line):  # Searching for lines that start with a number
                line = line.split('=', 1)[0].replace('\t', '').replace('\n', '').replace(' ', '')
                temp_line = str(line).rstrip('\n').strip().split()
                province_id += temp_line
    return province_id


def terrain_file():
    start = 'terrain_override = {'
    end = '}'
    path = terrain_file_path
    return start, end, path


def continent_file():
    start = '{'
    end = '}'
    path = continent_file_path
    return start, end, path

    
def area_file():
    start = '{'
    end = '}'
    path = area_file_path
    return start, end, path
    

def trade_nodes_file():
    start = 'members={'
    end = '}'
    path = trade_nodes_file_path
    return start, end, path


def read_from_file(start, end, path):
    province_id = []
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


def climate_file():
    wasteland_id = []
    start_wasteland = 'impassable = {'
    end = '}'
    path = climate_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start_wasteland in line.strip():
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


def default_file():
    sea_or_lake_id = []
    start_sea = 'sea_starts = {'
    start_lake = 'lakes = {'
    end = '}'
    path = default_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start_sea in line.strip():
                found_type = True
                continue

            if start_lake in line.strip():
                found_type = True
                continue

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split()
                    sea_or_lake_id += temp_line
    return sea_or_lake_id


def localisation_files():
    folder = localisation_file_path
    files = os.listdir(folder)
    keyword = ' PROV'
    id_line = []
    localisation_list = []
    for file in files:
        if os.path.isfile(os.path.join(folder, file)):
            f = open(os.path.join(folder, file), 'r', encoding='utf-8-sig')
            for line in f:
                if keyword in line and line.startswith(keyword):
                    line = line.split('PROV_', 1)[0].split('PROVINCE', 1)[0].split('PROVIRO_', 1)[0].split('PROVINCIAL', 1)[0].replace('\t', '').replace('\n', '')
                    line = line.replace('"', '').replace("'", '').replace(' ', '').removeprefix("PROV").replace(':0', ' ').replace(':1', ' ').replace(':', ' ')
                    temp_line = line.split('\n')
                    temp_line = [x for x in temp_line if x]
                    localisation_list += temp_line
                    line = line.split()
                    line = [x for x in line if x]
                    id_line += line
            f.close()
    return id_line, localisation_list


# Getting File names from history/provinces
def province_history_files():
    province_history_names = [f.name for f in os.scandir(province_history_path) if f.is_file()]
    province_history_id = [x.split('-', 1)[0].replace(' ', '') for x in province_history_names]
    province_history_names = [x.replace('-', '').replace('.txt', '') for x in province_history_names]
    return province_history_id, province_history_names


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
    sea_or_lake_id = default_file()
if climate_present is True:
    wasteland_id = climate_file()


if province_history_present is True:
    province_history_id, province_history_names = province_history_files()
    print("Loading File names from history/provinces/")
    if definition_present is True:
        province_id, definition_names = definition_file()
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
        start, end, path = terrain_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Terrain.txt Missing id:{missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        start, end, path = continent_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Continent.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        start, end, path = area_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id,province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"Area.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        start, end, path = trade_nodes_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        missing_province_id(province_history_id, province_id)
        missing_id = natural_sort(filter_list(missing_province_id(province_history_id, province_id)))
        print(f"TradeNodes.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if localisation_present is True:
        id_line, localisation_list = localisation_files()
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
        start, end, path = terrain_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Terrain.txt Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        start, end, path = continent_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Continent.txt Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        start, end, path = area_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Area.txt Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        start, end, path = trade_nodes_file()
        province_id = read_from_file(start, end, path)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"TradeNodes.txt Duplicate id:{duplicate}{os.linesep}")
    if localisation_present is True:
        id_line, localisation_list = localisation_files()
        province_id = integer_filter(id_line)
        duplicate = natural_sort(find_duplicate(province_id))
        print(f"Localisation Duplicate id:{duplicate}{os.linesep}")
    else:
        pass
else:
    pass

input_a = input("To print all history/province id's type: 'id', 'name', 'loc', 'def'\nTo Save to a txt file type: 'save id', "
                "'save name', 'save loc', 'save def'\n")

print_commands = {
    "name": province_history_names,
    "id": province_history_id,
    "loc": localisation_list,
    "def": definition_names
}

save_commands = {
    "save name": province_history_names,
    "save id": province_history_id,
    "save loc": localisation_list,
    "save def": definition_names
}

if input_a in print_commands.keys():
    print(str(natural_sort(print_commands.get(input_a))))

elif input_a in save_commands.keys():
    save_output = str(natural_sort(save_commands.get(input_a)))
    with open('province_id.txt', 'w', encoding='utf8') as output:
        output.write(save_output)
    print("Saved")
else:
    pass

input_file_path1 = 'data/input/XXXX.tel'
input_file_path2 = 'data/input/place_txt.txt'
output_file_path1 = 'data/output/ic_data.jsonl'
output_file_path2 = 'data/output/components_data.jsonl'
output_file_path3 = 'data/output/netlist.jsonl'
# {
#     packages: [{
#         type,
#         desc,
#         ref
#     }],
#     a_properties: [],
#     nets: []
# }

# used to process XXXX.tel
def process_packages(target, x_dict):
    res_item = {}
    target = target.split(';')
    desc_list = target[0].split('!')
    res_item['desc'] = desc_list[2].strip().replace("'", '')
    res_item['ref'] = target[1].strip().split(' ')
    x_dict[desc_list[0].strip().replace("'", '')] = res_item

def process_properties(target, x_dict):
    res_item = {}
    target = target.split(';')
    desc_list = target[0].strip().split(' ')
    res_item['value'] = desc_list[1].replace("'", '')
    res_item['ref'] = target[1].strip().split(' ')
    x_dict[desc_list[0]] = res_item

def process_nets(target, x_dict):
    res_item = {}
    target = target.split(';')
    res_item['ref'] = target[1].strip().split(' ')
    x_dict[target[0].strip().replace("'", '')] = res_item

tel_dict = {}
with open(input_file_path1, 'r+', encoding='utf-8') as f:
    cur_key = ''
    cur_dict = {}
    cur_target = ''
    unused_list = ['schedule', 'end']
    for line in f.readlines():
        line = line.strip()
        if line[0] == '$':
            if len(cur_key) != 0 and cur_key not in unused_list:
                tel_dict[cur_key] = cur_dict
                cur_dict = {}
            cur_key = line[1:].lower()
            continue
        if line[-1] == ',':
            cur_target = cur_target + ' ' + line[:-1]
            continue
        cur_target = cur_target + ' ' + line
        # print(cur_target)
        if cur_key == 'packages':
            process_packages(cur_target, cur_dict)
        elif cur_key == 'a_properties':
            process_properties(cur_target, cur_dict)
        elif cur_key == 'nets':
            process_nets(cur_target, cur_dict)
        cur_target = ''


# used to process place.txt

def process_ic_component(target, x_dict):
    res_item = {}
    target = target.split('!')
    res_item['symbol_x'] = eval(target[1].strip())
    res_item['symbol_y'] = eval(target[2].strip())
    res_item['rotation'] = eval(target[3].strip())
    res_item['mirror'] = target[4].strip() == 'm'
    res_item['symbol_name'] = target[5].strip()
    x_dict[target[0].strip()] = res_item

place_dict = {}
with open(input_file_path2, 'r+', encoding='utf-8') as f:
    start = False
    for line in f.readlines():
        if line[0] == 'C':
            start = True
        if start:
            process_ic_component(line, place_dict)

# to modularize by ic_component

def dis(x1,y1,x2,y2):
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)

# initialize
ic_adj_dict = {}
for item in place_dict:
    if item[0] == 'U' or item[0] == 'J' or item[0] == 'M':
        ic_adj_dict[item] = []
    ic_adj_dict['GND'] = []

# calculate netlist
for key in tel_dict['nets']:
    # special porcess with GND
    if key == 'GND':
        for item in tel_dict['nets'][key]['ref']:
            item = item.split('.')
            # if item[0][0] != 'U' and item[0][0] != 'J':
            if item[0][0] != 'U':
                if item[0] not in ic_adj_dict['GND']:
                    ic_adj_dict['GND'].append(item[0])
        continue
    
    ref_list = []
    index = 0
    for item in tel_dict['nets'][key]['ref']:
        item = item.split('.')
        if item[0] not in ref_list:
            ref_list.append(item[0])

    # modularize by distance
    for item1 in ref_list:
        if item1[0] != 'U' and item1[0] != 'J':
            x1 = place_dict[item1]['symbol_x']
            y1 = place_dict[item1]['symbol_y']
            min_dis = 1e10
            min_ref = ''
            for item2 in ref_list:
                if item2[0] == 'U' or item2[0] == 'J':
                    x2 = place_dict[item2]['symbol_x']
                    y2 = place_dict[item2]['symbol_y']
                    cur_dis = dis(x1,y1,x2,y2)
                    if cur_dis < min_dis:
                        min_dis = cur_dis
                        min_ref = item2

            if min_ref != '':
                if item1 not in ic_adj_dict[min_ref]:
                    ic_adj_dict[min_ref].append(item1)

ic_dict = {}
ic_dict['GND'] = ic_adj_dict['GND']
for i in ic_adj_dict:
    # print(ic_adj_dict[i])
    if i != 'GND':
        ic_dict[i] = place_dict[i]
        ic_dict[i]['adj'] = ic_adj_dict[i]

import jsonlines
with jsonlines.open(output_file_path1, mode='w') as writer:
    for i in ic_dict:
        # optional, only record IC components with adj 
        if i != 'GND' and ic_dict[i]['adj'] == []:
            continue
        writer.write({i:ic_dict[i]})
with jsonlines.open(output_file_path2, mode='w') as writer:
    for i in place_dict:
        writer.write({i:place_dict[i]})
with jsonlines.open(output_file_path3, mode='w') as writer:
    for i in tel_dict['nets']:        
        writer.write({i:tel_dict['nets'][i]})

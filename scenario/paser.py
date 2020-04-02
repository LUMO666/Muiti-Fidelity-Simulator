import yaml
def parse_senario(senario_file):
    with open(senario_file) as f:
        raw_senario_dict = yaml.load(f, Loader=yaml.FullLoader)
    assert 'common' in raw_senario_dict.keys() , "senario file has no 'common' propoties"
    senario_dict = {'common':raw_senario_dict['common'] , 'default_agent' : raw_senario_dict['default_agent']}
    # build agent list
    agent_list = {}
    for key,group in raw_senario_dict['agent_groups'].items():
        number = group['num']
        group_list = []
        for _ in range(number):
            group_list.append({})
        for (k,v) in group.items():
            coef = None
            if k.startswith('deg_'):
                coef = 3.1415926/180.0
                k = k[4:]
            if not isinstance(v,list):
                for idx in range(number):
                    if coef is None:
                        group_list[idx][k] = v
                    else:
                        group_list[idx][k] = v*coef
            else:
                for idx in range(number):
                    if coef is None:
                        group_list[idx][k] = v[idx]
                    else:
                        group_list[idx][k] = v[idx]*coef
                    
        agent_list[key]=group_list
    senario_dict['agent_groups'] = agent_list

    fence_list = {}
    if 'fence_group' in raw_senario_dict:
        for key,group in raw_senario_dict['fence_group'].items():
            fence = {}
            for (k,v) in group.items():
                coef = None
                if k.startswith('deg_'):
                    coef = 3.1415926/180.0
                    k = k[4:]
                if not isinstance(v,list):
                    if coef is None:
                        fence[k] = v
                    else:
                        fence[k] = v*coef
                else:
                    fence[k] = []
                    for v_v in v:
                        if coef is None:
                            fence[k].append(v_v)
                        else:
                            fence[k].append(v_v*coef)
            fence_list[key] = fence
    senario_dict['fence_list'] = fence_list
    return senario_dict
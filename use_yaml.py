
class use_yaml():
    #TODO : yamlが使えるようになったら修正
    def load_csv(self, path):
        yaml_dic = {}
        with open(path, mode='r') as f:
            for line in f:
                items = line.split(',')
                if len(items) == 2:
                    yaml_dic[items[0]] = items[1].strip()
                else:
                    item = ''
                    for i in range(len(items) - 1):
                        item += items[i + 1].strip()
                    yaml_dic[items[0]] = item
        return yaml_dic

            

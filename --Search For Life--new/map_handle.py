import json
def SaveMap(index, data):
     with open('Maps\\' + str(index) + '.json', 'w') as map_file:
                json.dump(data, map_file)
def MakeMap(index, map_width, map_height):
         data = [[]]
         for x in range(map_width):
            data.append([])
            for y in range(map_height) : 
               data[x].append(str(0))       
         with open('Maps\\' + str(index) + '.json', 'w') as map_file:
                    json.dump(data, map_file)                  
                    
def LoadMap(index):
          with open('Maps\\' + str(index)) as map_file:
             data = json.load(map_file) 
          map_height = len(data[0])
          map_width = len(data)  
          return data, map_height, map_width

def GetData(dat):
     with open('Data\\editordata.json', 'w') as datafile:
          json.dump(dat, datafile)
     
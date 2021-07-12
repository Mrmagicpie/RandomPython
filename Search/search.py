import os, json 
from datetime import datetime 

start = datetime.now()
location = str(input("Where should I search: ")).strip()

if not os.path.isdir(location):
    print("Please input a valid path")
    exit(1)

location = os.path.abspath(location)
name  = str(input("Name to search: ")).strip()
save  = str(input("Should I save to json? (y/n) ")).lower()
save  = (save in {"y", "yes"})

if save:
    save = True 
    print("Please note - This will overide that file.")
    save_location = str(input("What file should I save it in? "))
    save_location = save_location.replace(".json", "") + ".json"

found = set()
    
class ItemFound:
    def __init__(self, name: str, dir: str):
        self.name = name 
        self.dir  = dir 
    
    def __hash__(self):
        return hash((self.name, self.dir))

    def __eq__(self, obj):
        if not isinstance(obj, ItemFound):
            return False 
        return self.name == obj.name and self.dir == obj.dir 

def list_dir(dir: str):
    try:
        return (os.listdir(dir), True)
    except PermissionError:
        return ([], False) 

def search_directory(contents: list):
    for item in contents:
        item_path = os.path.join(location, item)
        if os.path.isdir(item_path):
            item_path = list_dir(item_path)
            if not item_path[1]:
                continue 
            search_directory(item_path[0])
        
        if name in item:
            found.add(ItemFound(item, item_path))

contents = list_dir(location)
if not contents[1]:
    print(f"Cannot access: {location}")
    exit(1)

search_directory(contents[0])
print(f"Took: {str(datetime.now() - start)}")
print(f"Items found:")
for item in found:
    print("\tItem:")
    print(f"\t\tName: {item.name}")
    print(f"\t\tLocation: {item.dir}")

if not save:
    exit(0)

print(f"Saving to {save_location}")

try:
    f = open(save_location, "w", encoding="UTF-8")
except:
    print("There was an error saving to that file. Please try again with a different name.")
    exit(1)

final_json = list()
for item in found:
    final_json.append({"name": item.name, "location": item.dir})
    
json.dump(final_json, f)
f.close()

print(f"Saved to {save_location}")

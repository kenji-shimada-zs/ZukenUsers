import pathlib,re
log_file=pathlib.Path(__file__).parent.joinpath("debug.log")

class Users():
    def __init__(self):
        self.UserList=[]
    def add_user(self,match):
        self.UserList.append([match.group("kind"),match.group("user"),match.group("computer")])
    def remove_user(self,match):
        self.UserList.remove([match.group("kind"),match.group("user"),match.group("computer")])

def UserList(log:pathlib.Path):
    Users_data=Users()
    with open(log) as log_f:
        log_lines = log_f.readlines()
    
    pattern=r'\d*:\d*:\d* \(zuken\) (?P<in_out>.*?): "(?P<kind>.*?)" (?P<user>.*?)@(?P<computer>.*?) '
    for line in log_lines:
        match=re.search(pattern,line)
        if match is not None:
            if   match.group("in_out") == "OUT":
                Users_data.add_user(match)
            elif match.group("in_out") == "IN":
                Users_data.remove_user(match)
    return Users_data.UserList

if __name__=="__main__":
    User_data=UserList(log_file)
    for i in User_data:
        print(i,end="\n")
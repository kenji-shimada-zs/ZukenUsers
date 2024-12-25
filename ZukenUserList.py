import pathlib,re,subprocess,pandas
log_file=pathlib.WindowsPath(r'\\uranus\license\debug.log')
if log_file.exists() == False:
    raise FileExistsError(f"{log_file} is not found")
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
        if line == log_lines[-5]:
            print()
        match=re.search(pattern,line)
        if match is not None:
            if   match.group("in_out") == "OUT":
                Users_data.add_user(match)
            elif match.group("in_out") == "IN":
                Users_data.remove_user(match)
    return Users_data.UserList

def get_user_info(user):
    cmd=f'net user {user} /domain'
    result=subprocess.run(cmd, capture_output=True, text=True)
    #参考:https://atmarkit.itmedia.co.jp/ait/articles/0609/02/news014.html
    result_line = result.stdout.splitlines()
    for line in result_line:
        list_a=re.split(' {2,}',line)
        try:
            if list_a[0] == 'フル ネーム':
                return str(list_a[1]).replace('\u3000','')
        except:
            next

def get() -> pandas.DataFrame:
    User_data=UserList(log_file)
    for i in range(len(User_data)):
        User_data[i].append(get_user_info(User_data[i][1]))
    User_data_df=pandas.DataFrame(data=User_data,columns=["kind","ID","PC-ID","FullName"])
    print(User_data_df)
    return User_data_df 
    
if __name__=="__main__":
    get()
    input("finish")
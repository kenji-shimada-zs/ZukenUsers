import pathlib,re,subprocess
log_file=pathlib.Path(__file__).parent.joinpath("debug.log")
network_path=r'\\uranus\CR8000\part_temp.csv'
path=pathlib.WindowsPath(network_path)
print(path.exists())
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
if __name__=="__main__":
    fullname=get_user_info("00090405348")
    User_data=UserList(log_file)
    for i in User_data:
        print(i,end="\n")
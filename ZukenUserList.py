import pathlib,re,subprocess,pandas,paramiko
import paramiko.client
log_file=pathlib.WindowsPath(r'\\uranus\license\debug.log')
#if log_file.exists() == False:
#    raise FileExistsError(f"{log_file} is not found")
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
def UserList2():
    # 接続
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh.connect(hostname="10.18.176.61", username='administrator', password='kwicrn1HW')
        #stdin, stdout, stderr = ssh.exec_command("hostname")
        stdin, stdout, stderr = ssh.exec_command("C:\\zuken\\license\\lmutil.exe lmstat -a")
        raw_data=list(stdout)
    
    return split_license_list(raw_data)

    #for line in raw_data:
    #    if "Users of" in line:
    #        license_name=re.search(pattern=r"[A-Z]{2}[0-9]{4}",string=line)[0]
def split_license_list(raw_data:list):
    """_summary_

    Args:
        raw_data (list): _description_
    """
    user_list = []
    raw_data_str="".join(raw_data)
    raw_data_split=raw_data_str.split("Users of ")
    for n in range(1,len(raw_data_split)):
        license=raw_data_split[n]
        match=re.search(pattern=r"(?P<license_name>[A-Z]{2}[0-9]{4}):  \(Total of (?P<license_total>\d+) licenses? issued;  Total of (?P<license_used>\d+) licenses? in use\)",string=license)
        license_name =str(match.group("license_name"))
        license_total=int(match.group("license_total"))
        license_used =int(match.group("license_used"))
        if license_used > 0:
            license_users=raw_data_split[7].split("floating license")[1].split("\r\n")
            license_users=[a for a in license_users if a != ""]
            for license_user in license_users:
                pattern=r"(?P<username>\w+)\s(?P<user_pc>\w+)\s(?P<user_pc2>\w+)\s\((?P<version>[a-z,A-Z,0-9,.]+)\)"
                match=re.search(string=license_user,pattern=pattern)
                username=match.group("username")
                user_pc =match.group("user_pc")
                user_list.append([license_name,license_total,license_used,username,get_user_info(username),user_pc])
    return user_list
        
def get() -> pandas.DataFrame:
    User_data=UserList2()
    User_data_df=pandas.DataFrame(data=User_data,columns=["license","license_total","license_used","ID","FullName","PC-ID"])
    print(User_data_df)
    return User_data_df 
    
if __name__=="__main__":
    get()
    input("finish")
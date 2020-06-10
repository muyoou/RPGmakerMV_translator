#腾讯API对接
import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 

ErrorNum = 0
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
        print("服务端错误：")
        print(err)
        if ErrorNum <= 8:
            ErrorNum+=1
            time.sleep(0.3)
            tran(input)
        else:
            ErrorNum = 0

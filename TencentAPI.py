#腾讯API对接
import json
import time
import config
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 

ErrorNum = 0
def tran(input):
    try: 
        cred = credential.Credential(config.ApiID,config.ApiKEY ) 
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
        print(err.code)
        if err.code=='InvalidCredential':
            print("翻译API不存在")
            return 'API_ERR'
        elif err.code=='RequestLimitExceeded':
            print("连接频繁")
            time.sleep(0.3)
            return tran(input)

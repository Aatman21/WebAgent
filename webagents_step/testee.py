import json
import requests

CLIENT_ID='MDSR_Firefall'
CLIENT_SECRET='s8e-8CGebu-kO3Vt_ICCNzQU8sCVYCHqcuFq'
AUTH_KEY='eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6Ik1EU1JfRmlyZWZhbGxfc3RnIiwidHlwZSI6ImF1dGhvcml6YXRpb25fY29kZSIsImNsaWVudF9pZCI6Ik1EU1JfRmlyZWZhbGwiLCJ1c2VyX2lkIjoiTURTUl9GaXJlZmFsbEBBZG9iZUlEIiwiYXMiOiJpbXMtbmExLXN0ZzEiLCJvdG8iOmZhbHNlLCJjcmVhdGVkX2F0IjoiMTY4MTE0NTIxNDk1MCIsInNjb3BlIjoic3lzdGVtIn0.Yoz7IPhmIBV2uNKl1CJJ9rJ0HmvDBQFbh0AihlHdsOa1E3yBs7WB9ilTCUVodifg8gh1yw4QRllV1NKS2RYeiGxQU7rXAF7SEnH_X_Tqdl735PBnBFL8sW_x76dzmT6MZIzynz8Ywu57qztvFnHoLMfJ7HsNt7rkOqF3IZByOinxyJzRTwMfygHSKjoQx6A4S7LbuQWjlqDbM9RaeCcakMEqGvSKqkLQvtMg40ZQYSNELoFtbATfwuVrHWOglAQS4A2FR24ziop137imu4HrTr-syDYki8VWV27WuGGo632_K2vJwqbaYjZvyrtsuBLH3fGGgXgyM5EA_Jk_lcMFog'
IMS_URL='https://ims-na1-stg1.adobelogin.com/ims/token/v2'
AZURE_CHAT_COMPLETION_START= 'https://firefall-stage.adobe.io/v1/chat/completions/conversations'
AZURE_CHAT_COMPLETION= 'https://firefall-stage.adobe.io/v1/chat/completions'
AZURE_COMPLETIONS='https://firefall-stage.adobe.io/v1/completions'

def get_response(prompt):
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTH_KEY,
        'grant_type': 'authorization_code',
    }
    response = requests.post(IMS_URL, data=params)
    temp_auth_token=json.loads(response.text)['access_token']

    def get_openai_response(azure_url, json_data, temp_auth_token):
        headers = {
            'x-gw-ims-org-id': CLIENT_ID,
            'x-api-key': CLIENT_ID,
            'Authorization': f'Bearer {temp_auth_token}',
            'Content-Type': 'application/json',
        }
        response = requests.post(azure_url, headers=headers, json=json_data)
        return json.loads(response.text)

    json_data = {
        "messages": [{
            "role": "system",
            "content": "You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions."
        }],
        "llm_metadata": {
            "model_name": "gpt-4-turbo",
            "temperature": 0.3,
            "max_tokens": 256,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "llm_type": "azure_chat_openai"
        },
    }
    openai_response = get_openai_response(AZURE_CHAT_COMPLETION_START, json_data, temp_auth_token)
    conversation_id = openai_response['conversation_id']

    json_data={
        "conversation_id": conversation_id,
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "llm_metadata": {
            "model_name": "gpt-4-turbo",
            "temperature": 0.3,
            "max_tokens": 256,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "llm_type": "azure_chat_openai",
            "n": 1
        },
    }
    openai_response = get_openai_response(AZURE_CHAT_COMPLETION, json_data, temp_auth_token)
    return openai_response["generations"][0][0]["text"]

def main():
    prompt=input("Enter prompt: ")
    response=get_response(prompt)
    print(response)

def caller(prompt):
    return get_response(prompt)

if __name__=="__main__":
    main()
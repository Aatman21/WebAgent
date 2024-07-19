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
            "content": "You are an excellent assistant skilled at identifying changes after clicking an element on a webpage. You focus/attention on and list down all the important information that got focussed in very very detail after the click which is present in the 'after' accessibility. Avoid any useless and non-crucial information which doesn't help me know the exact functionality of the clicked element, keep the response as detailed as possible but without non-sense."
        }],
        "llm_metadata": {
            "model_name": "gpt-35-turbo-1106",
            "temperature": 0.2,
            "max_tokens": 256,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "llm_type": "azure_chat_openai"
        },
    }
    openai_response = get_openai_response(AZURE_CHAT_COMPLETION_START, json_data, temp_auth_token)
    conversation_id = openai_response['conversation_id']
    """Here provide an example input and response"""
    json_data={
        "conversation_id": conversation_id,
        "messages":[
            {
                "role": "user",
                "content": """
Before: Tab 0 (current): Dashboard / Magento Admin

[1] RootWebArea 'Dashboard / Magento Admin' focused: True
	[94] link 'Magento Admin Panel'
		[103] img 'Magento Admin Panel'
	[6] menubar '' orientation: horizontal
		[8] link '\ue604 DASHBOARD'
		[12] link '\ue60b SALES'
		[16] link '\ue608 CATALOG'
		[20] link '\ue603 CUSTOMERS'
		[24] link '\ue609 MARKETING'
		[28] link '\ue602 CONTENT'
		[32] link '\ue60a REPORTS'
		[36] link '\ue60d STORES'
		[40] link '\ue610 SYSTEM'
		[44] link '\ue612 FIND PARTNERS & EXTENSIONS'
	[146] heading 'Dashboard'
	[148] link '\ue600 admin'
	[150] link '\ue607'
	[824] textbox '\ue60c' required: False
	[54] main ''
		[119] StaticText 'Scope:'
		[155] button 'All Store Views' hasPopup: menu
		[158] link '\ue633 What is this?'
		[126] button 'Reload Data'
		[828] HeaderAsNonLandmark ''
			[830] StaticText 'Advanced Reporting'
		[831] StaticText "Gain new insights and take command of your business' performance, using our dynamic product, order, and customer reports tailored to your customer data."
		[832] link 'Go to Advanced Reporting \ue644'
		[835] StaticText 'Chart is disabled. To enable the chart, click '
		[836] link 'here'
		[1062] StaticText 'Revenue'
		[962] StaticText '$0.00'
		[1063] StaticText 'Tax'
		[1064] StaticText 'Shipping'
		[1065] StaticText 'Quantity'
		[63] tablist '' multiselectable: False orientation: horizontal
			[65] tab 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Bestsellers' expanded: True selected: True controls: grid_tab_ordered_products_content
				[73] link 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Bestsellers'
			[67] tab 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Most Viewed Products' expanded: False selected: False controls: ui-id-1
				[75] link 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Most Viewed Products'
			[69] tab 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... New Customers' expanded: False selected: False controls: ui-id-2
				[77] link 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... New Customers'
			[71] tab 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Customers' expanded: False selected: False controls: ui-id-3
				[79] link 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Customers'
		[85] tabpanel 'The information in this tab has been changed. This tab contains invalid data. Please resolve this before saving. Loading... Bestsellers'
			[996] table ''
				[1066] row ''
					[1067] columnheader 'Product' required: False
					[1068] columnheader 'Price' required: False
					[1069] columnheader 'Quantity' required: False
				[1070] row 'http://localhost:7780/admin/catalog/product/edit/id/20/'
					[1075] gridcell 'Quest Lumaflex™ Band' required: False
					[1076] gridcell '$19.00' required: False
					[1077] gridcell '6' required: False
				[1071] row 'http://localhost:7780/admin/catalog/product/edit/id/33/'
					[1078] gridcell 'Sprite Yoga Strap 6 foot' required: False
					[1079] gridcell '$14.00' required: False
					[1080] gridcell '6' required: False
				[1072] row 'http://localhost:7780/admin/catalog/product/edit/id/29/'
					[1081] gridcell 'Sprite Stasis Ball 65 cm' required: False
					[1082] gridcell '$27.00' required: False
					[1083] gridcell '6' required: False
				[1073] row 'http://localhost:7780/admin/catalog/product/edit/id/25/'
					[1084] gridcell 'Sprite Stasis Ball 55 cm' required: False
					[1085] gridcell '$23.00' required: False
					[1086] gridcell '5' required: False
				[1074] row 'http://localhost:7780/admin/catalog/product/edit/id/13/'
					[1087] gridcell 'Overnight Duffle' required: False
					[1088] gridcell '$45.00' required: False
					[1089] gridcell '5' required: False
		[841] StaticText 'Lifetime Sales'
		[844] StaticText '$0.00'
		[848] StaticText 'Average Order'
		[855] StaticText 'Last Orders'
		[856] table ''
			[887] row ''
				[888] columnheader 'Customer' required: False
				[889] columnheader 'Items' required: False
				[890] columnheader 'Total' required: False
			[891] row 'http://localhost:7780/admin/sales/order/view/order_id/299/'
				[896] gridcell 'Sarah Miller' required: False
				[897] gridcell '5' required: False
				[898] gridcell '$194.40' required: False
			[892] row 'http://localhost:7780/admin/sales/order/view/order_id/65/'
				[899] gridcell 'Grace Nguyen' required: False
				[900] gridcell '4' required: False
				[901] gridcell '$190.00' required: False
			[893] row 'http://localhost:7780/admin/sales/order/view/order_id/125/'
				[902] gridcell 'Matt Baker' required: False
				[903] gridcell '3' required: False
				[904] gridcell '$151.40' required: False
			[894] row 'http://localhost:7780/admin/sales/order/view/order_id/136/'
				[905] gridcell 'Lily Potter' required: False
				[906] gridcell '4' required: False
				[907] gridcell '$188.20' required: False
			[895] row 'http://localhost:7780/admin/sales/order/view/order_id/230/'
				[908] gridcell 'Ava Brown' required: False
				[909] gridcell '2' required: False
				[910] gridcell '$83.40' required: False
		[861] StaticText 'Last Search Terms'
		[862] table ''
			[911] row ''
				[912] columnheader 'Search Term' required: False
				[913] columnheader 'Results' required: False
				[914] columnheader 'Uses' required: False
			[915] row 'http://localhost:7780/admin/search/term/edit/id/25/'
				[920] gridcell 'tanks' required: False
				[921] gridcell '23' required: False
				[922] gridcell '1' required: False
			[916] row 'http://localhost:7780/admin/search/term/edit/id/19/'
				[923] gridcell 'nike' required: False
				[924] gridcell '0' required: False
				[925] gridcell '3' required: False
			[917] row 'http://localhost:7780/admin/search/term/edit/id/1/'
				[926] gridcell 'Joust Bag' required: False
				[927] gridcell '10' required: False
				[928] gridcell '4' required: False
			[918] row 'http://localhost:7780/admin/search/term/edit/id/11/'
				[929] gridcell 'hollister' required: False
				[930] gridcell '1' required: False
				[931] gridcell '19' required: False
			[919] row 'http://localhost:7780/admin/search/term/edit/id/13/'
				[932] gridcell 'Antonia Racer Tank' required: False
				[933] gridcell '23' required: False
				[934] gridcell '2' required: False
		[867] StaticText 'Top Search Terms'
		[868] table ''
			[935] row ''
				[936] columnheader 'Search Term' required: False
				[937] columnheader 'Results' required: False
				[938] columnheader 'Uses' required: False
			[939] row 'http://localhost:7780/admin/search/term/edit/id/11/'
				[944] gridcell 'hollister' required: False
				[945] gridcell '1' required: False
				[946] gridcell '19' required: False
			[940] row 'http://localhost:7780/admin/search/term/edit/id/1/'
				[947] gridcell 'Joust Bag' required: False
				[948] gridcell '10' required: False
				[949] gridcell '4' required: False
			[941] row 'http://localhost:7780/admin/search/term/edit/id/13/'
				[950] gridcell 'Antonia Racer Tank' required: False
				[951] gridcell '23' required: False
				[952] gridcell '2' required: False
			[942] row 'http://localhost:7780/admin/search/term/edit/id/25/'
				[953] gridcell 'tanks' required: False
				[954] gridcell '23' required: False
				[955] gridcell '1' required: False
			[943] row 'http://localhost:7780/admin/search/term/edit/id/9/'
				[956] gridcell 'WP10' required: False
				[957] gridcell '1' required: False
				[958] gridcell '1' required: False

After: Tab 

[1121] RootWebArea 'Configuration / Settings / Stores / Magento Admin' focused: True
	[1575] link 'Magento Admin Panel'
		[1584] img 'Magento Admin Panel'
	[1126] menubar '' orientation: horizontal
		[1128] link '\ue604 DASHBOARD'
		[1132] link '\ue60b SALES'
		[1136] link '\ue608 CATALOG'
		[1140] link '\ue603 CUSTOMERS'
		[1144] link '\ue609 MARKETING'
		[1148] link '\ue602 CONTENT'
		[1152] link '\ue60a REPORTS'
		[1156] link '\ue60d STORES'
		[1160] link '\ue610 SYSTEM'
		[1164] link '\ue612 FIND PARTNERS & EXTENSIONS'
	[1625] heading 'Configuration'
	[1627] link '\ue600 admin'
	[1629] link '\ue607'
	[1205] textbox '\ue60c' required: False
	[1168] main ''
		[1600] StaticText 'Scope:'
		[1634] button 'Default Config' hasPopup: menu
		[1637] link '\ue633 What is this?'
		[1603] button 'Save Config'
		[1559] link '\ue615 Admin User Emails'
		[1474] group ''
			[1466] table ''
				[1430] LayoutTableRow ''
					[2519] LayoutTableCell '[global] Forgot Password Email Template'
					[1471] LayoutTableCell 'Forgot Admin Password (Default) Email template chosen based on theme fallback when "Default" option is selected.'
						[1442] combobox '[global] Forgot Password Email Template' disabled: True hasPopup: menu expanded: False
					[1500] LayoutTableCell 'Use system value'
						[1491] checkbox 'Use system value' checked: true
					[2520] LayoutTableCell ''
				[1414] LayoutTableRow ''
					[2521] LayoutTableCell '[global] Forgot and Reset Email Sender'
					[1415] LayoutTableCell 'General Contact'
						[1486] combobox '[global] Forgot and Reset Email Sender' disabled: True hasPopup: menu expanded: False
					[1535] LayoutTableCell 'Use system value'
						[1507] checkbox 'Use system value' checked: true
					[2522] LayoutTableCell ''
				[1508] row ''
					[2523] gridcell '[global] User Notification Template' required: False
					[1465] LayoutTableCell 'User Notification (Default) Email template chosen based on theme fallback when "Default" option is selected.'
						[1459] combobox '[global] User Notification Template' disabled: True hasPopup: menu expanded: False
					[1487] LayoutTableCell 'Use system value'
						[1412] checkbox 'Use system value' checked: true
					[2524] gridcell '' required: False
				[1527] row ''
					[2525] gridcell '[global] New User Notification Template' required: False
					[1510] LayoutTableCell 'New User Notification (Default) Email template chosen based on theme fallback when "Default" option is selected.'
						[1426] combobox '[global] New User Notification Template' disabled: True hasPopup: menu expanded: False
					[1475] LayoutTableCell 'Use system value'
						[1434] checkbox 'Use system value' checked: true
					[2526] gridcell '' required: False
		[1556] link '\ue615 Startup Page'
		[1505] group ''
			[1499] table ''
				[1503] row ''
					[2527] gridcell '[global] Startup Page' required: False
					[1432] LayoutTableCell 'Dashboard'
						[1520] combobox '[global] Startup Page' disabled: True hasPopup: menu expanded: False
					[1522] gridcell 'Use system value' required: False
						[1440] checkbox 'Use system value' checked: true
					[2528] gridcell '' required: False
		[1553] link '\ue615 Admin Base URL'
		[1504] group ''
			[1464] table ''
				[1449] LayoutTableRow ''
					[2529] LayoutTableCell '[global] Use Custom Admin URL'
					[1525] LayoutTableCell 'No'
						[1501] combobox '[global] Use Custom Admin URL' disabled: True hasPopup: menu expanded: False
					[1461] LayoutTableCell 'Use system value'
						[1529] checkbox 'Use system value' checked: true
					[2530] LayoutTableCell ''
				[1473] row ''
					[2542] gridcell '[global] Use Custom Admin Path' required: False
					[1488] gridcell 'No' required: False
						[1439] combobox '[global] Use Custom Admin Path' disabled: True hasPopup: menu expanded: False
					[1437] LayoutTableCell 'Use system value'
						[1476] checkbox 'Use system value' checked: true
					[2543] gridcell '' required: False
		[1550] link '\ue615 Security'
		[1427] group ''
			[1521] table ''
				[1455] LayoutTableRow ''
					[2555] LayoutTableCell '[global] Admin Account Sharing'
					[1479] LayoutTableCell 'Yes If set to Yes, you can log in from multiple computers into same account. Default setting No improves security.'
						[1502] combobox '[global] Admin Account Sharing' hasPopup: menu expanded: False
					[1447] LayoutTableCell 'Use system value'
						[1518] checkbox 'Use system value' checked: false
					[2556] LayoutTableCell ''
				[1433] LayoutTableRow ''
					[2557] LayoutTableCell '[global] Password Reset Protection Type'
					[1418] LayoutTableCell 'By IP and Email'
						[1490] combobox '[global] Password Reset Protection Type' disabled: True hasPopup: menu expanded: False
					[1411] LayoutTableCell 'Use system value'
						[1450] checkbox 'Use system value' checked: true
					[2558] LayoutTableCell ''
				[1534] row ''
					[2559] gridcell '[global] Recovery Link Expiration Period (hours)' required: False
					[1462] LayoutTableCell '2 Please enter a number 1 or greater in this field.'
						[1533] textbox '[global] Recovery Link Expiration Period (hours)' disabled: True required: False
					[1451] LayoutTableCell 'Use system value'
						[1516] checkbox 'Use system value' checked: true
					[2560] gridcell '' required: False
				[1570] row ''
					[2561] gridcell '[global] Max Number of Password Reset Requests' required: False
					[1566] LayoutTableCell '5 Limit the number of password reset request per hour. Use 0 to disable.'
						[1568] textbox '[global] Max Number of Password Reset Requests' disabled: True required: False
					[1569] LayoutTableCell 'Use system value'
						[1563] checkbox 'Use system value' checked: true
					[2562] gridcell '' required: False
				[1564] row ''
					[2563] gridcell '[global] Min Time Between Password Reset Requests' required: False
					[1565] gridcell '10 Delay in minutes between password reset requests. Use 0 to disable.' required: False
						[1561] textbox '[global] Min Time Between Password Reset Requests' disabled: True required: False
					[1567] gridcell 'Use system value' required: False
						[1562] checkbox 'Use system value' checked: true
					[2564] gridcell '' required: False
				[1526] row ''
					[2565] gridcell '[global] Add Secret Key to URLs' required: False
					[1456] LayoutTableCell 'No'
						[1423] combobox '[global] Add Secret Key to URLs' hasPopup: menu expanded: False
					[1509] LayoutTableCell 'Use system value'
						[1416] checkbox 'Use system value' checked: false
					[2566] gridcell '' required: False
"""
            },
            {
                "role": "assistant",
                "content": "The important information that got focussed after the click is: Admin User Emails, Startup Page, Admin Base URL, Security, General, Catelog, Security, Customers, Sales, Services and Advanced"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "llm_metadata": {
            "model_name": "gpt-35-turbo-1106",
            "temperature": 0.5,
            "max_tokens": 256,
            "top_p": 0.5,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "llm_type": "azure_chat_openai",
            "n": 1
        },
    }
    openai_response = get_openai_response(AZURE_CHAT_COMPLETION, json_data, temp_auth_token)
    return openai_response["generations"][0][0]["text"]

def main():
    """Input the before and after tree as input"""
    prompt1=""
    response=get_response(prompt1)
    print(response)



if __name__=="__main__":
    main()

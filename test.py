import requests

# URL（含查询参数）
url = 'https://admin-api.zaporder.com/api/report/order/listPage'
params = {
    }

# 请求头 Headers
headers = {
    'Accept': 'application/json, text/plain, */*',
    'X-Saas-Account-Id': '360287970189869705',
    'X-Saas-Org-Id': '20030343599528807',
    'X-Saas-Store-Id': '40000343599548767',
    'X-Saas-Tenant-Id': '10020343599448675'
}

# Cookies（从 -b 参数提取）
cookies_str = '_gcl_au=1.1.1818455277.1764382372; _ga=GA1.1.1762213707.1764382373; _ga_P8RN8E8C91=GS2.1.s1764382378$o1$g0$t1764382378$j60$l0$h0; _tt_enable_cookie=1; _ttp=01KB6P5278WTRK78DVME8NKTN5_.tt.1; _fbp=fb.1.1764382378427.39330903163692823; ttcsid=1764382378218::HE8bFNV91wp9mTP3rvhU.1.1764382378432.0; ttcsid_C8INMM59481MCTU3T390=1764382378217::OfBDRmNF4-1PMkOmQfPN.1.1764382378432.0; cto_bundle=sZgGb19Pc3IwVXIxR0JUVUNQMzc3TTM0Y0xBdGE5ckJOeFIxWW91TTFhUkN6bnhPY2ROUzBPcDQ0Smhod3FMdWZqaEZ1dGpuTGV5NFhKTG53JTJCRm5ZN0c5SW9qZEZVeGwlMkJkVnZCRFNzM3JEaTNLUlg4SzRXdHRKdyUyQnYlMkZRdXl0VktaTFpqbEdZeDYycVVrVWdJWFNrJTJGRzdXRERwb0RtNnc0eFJhUDJ6dDNOaXk4NVg0JTNE; _clck=1urdlfy%5E2%5Eg1f%5E0%5E2159; _clsk=1tcdaim%5E1764382380479%5E1%5E1%5Ek.clarity.ms%2Fcollect; ticket=GnS5v74AzyRPfkRIxRITUXvAlypwVBaw73-8YSvPC-AkzDtqxEAQANG7VOpGdM_0_Dr0EXwDy5Y_ySxo2Ujo7ovYqIKCdzCVIC-6KMI0woSZiKRquQgzEypMJ6xVH70lc2EWgvcPhE8ChJUwN0_Wk_u4WkftwjdRurARB_fbY__aiKaqdgo_LzP35Jf5S_BWyjVrHs19rDvCH4Eh_BN6PgMAAP__; _ga_VVCWHC0G6L=GS2.1.s1764382373$o1$g1$t1764382417$j16$l0$h186870712'

# 将 cookie 字符串转为字典
cookies = {}
for item in cookies_str.split('; '):
    if '=' in item:
        key, value = item.split('=', 1)
        cookies[key] = value

# 请求体（JSON 数据）
json_data = {
    "pageNum": 1,
    "pageSize": 50,
    "startDate": "2025-11-29",
    "endDate": "2025-11-29",
    "orderStatus": [],
    "sortRule": {
        "field": "",
        "order": ""
    }
}

# 发起 POST 请求
response = requests.post(
    url=url,
    params=params,
    headers=headers,
    cookies=cookies,
    json=json_data  # 自动设置 Content-Type 并序列化
)

# 打印响应
print("Status Code:", response.status_code)
print("Response Body:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
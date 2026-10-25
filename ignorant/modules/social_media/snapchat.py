from ignorant.core import *
from ignorant.localuseragent import *


async def snapchat(phone, country_code, client, out):
    name = "snapchat"
    domain = "snapchat.com"
    method = "register"
    frequent_rate_limit=False

    # Shared calling codes cannot be mapped to a single country. The original
    # table labels all +1 numbers as VI and all +44 numbers as JE.
    import phonenumbers
    parsed = phonenumbers.parse('+' + str(country_code) + str(phone))
    region = phonenumbers.region_code_for_number(parsed)
    if not region:
        out.append({"name": name, "domain": domain, "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False})
        return

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Origin': 'https://accounts.snapchat.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }
    try:
        response = await client.get("https://accounts.snapchat.com", headers=headers)
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False})
        return()

    data = {
      'phone_country_code': region,
      'phone_number': phone,
      'xsrf_token': response.cookies["xsrf_token"]
    }

    response = await client.post('https://accounts.snapchat.com/accounts/validate_phone_number', headers=headers, data=data)
    try:
        status = response.json()["status_code"]
        if status=="TAKEN_NUMBER":
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True})
        elif status=="OK":
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False})

        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False})
    except:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False})


import json
import hmac
import hashlib
import requests
import uuid
import time 
from django.conf import settings

def create_momo_payment(order_id, amount):
    endpoint = settings.MOMO_API_URL
    partnerCode = settings.MOMO_PARTNER_CODE
    accessKey = settings.MOMO_ACCESS_KEY
    secretKey = settings.MOMO_SECRET_KEY
    
  
    momo_order_id = f"{order_id}-{int(time.time())}"
  

    orderInfo = f"Thanh toan don hang {order_id}"
    redirectUrl = "http://localhost:8000/api/orders/payment/"
    ipnUrl = "http://localhost:8000/" 
    
    requestId = str(uuid.uuid4())
    requestType = "payWithATM"
    extraData = "" 
    str_amount = str(int(amount))


    rawSignature = (
        f"accessKey={accessKey}&amount={str_amount}&extraData={extraData}"
        f"&ipnUrl={ipnUrl}&orderId={momo_order_id}&orderInfo={orderInfo}" 
        f"&partnerCode={partnerCode}&redirectUrl={redirectUrl}"
        f"&requestId={requestId}&requestType={requestType}"
    )

    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    data = {
        'partnerCode': partnerCode,
        'partnerName': "Fashion Shop",
        'storeId': "MoMoTestStore",
        'requestId': requestId,
        'amount': str_amount,
        'orderId': momo_order_id,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }

    try:
        response = requests.post(endpoint, json=data)
        result = response.json()
        
        if result['resultCode'] == 0:
            return result['payUrl']
        else:
            print("MoMo Error:", result['message'])
            return None
    except Exception as e:
        print("Lỗi kết nối:", e)
        return None
from kavenegar import KavenegarAPI, APIException, HTTPException

def send_Otp_Code(phone_number, code):
    try:
        
        api = KavenegarAPI('4653706473737863534547722B755A4258684F54694F334C494C43756F4B71622F637A3845647731422F303D')
        params = {
            'sender' : '2000660110',
            'receptor': phone_number ,
            'message' : f"کد تایید شما {code}" 
            
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
        
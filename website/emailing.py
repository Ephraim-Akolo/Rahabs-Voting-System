import requests

def send_otp(email, otp):
    return send_mail('ephraimakolo2017@gmail.com', email, 'OTP', htmlbody.format(token=otp))

def send_mail(
    from_email:str, 
    to_email:str, 
    subject:str, 
    htmlbody:str,
    url:str = "https://api.elasticemail.com/v2/email/send", 
    ):
    header = {
        # 'Authorization': authorization,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }
    params = {
        "apikey": "C0D82DB57451D3013DCE0AB0518ED1A924E400EDC2F802ADE269ED3F5653018F06670845DFB7084E09B296ADEED76E40",
        'from': from_email,
        'to': to_email,
        'subject': subject,
        'bodyHtml': htmlbody
    }
    r = requests.get(url, params=params).json()
    return r['success'], r

htmlbody = '''
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}

        .container {{
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
            width: 300px;
        }}

        h1 {{
            color: #333;
        }}

        p {{
            color: #555;
        }}

        .otp {{
            font-size: 24px;
            color: #3498db;
            margin-bottom: 20px;
        }}

        .btn {{
            display: inline-block;
            background-color: #3498db;
            color: #fff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
        }}

        .footer {{
            margin-top: 20px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>OTP Verification</h1>
        <p>Your One-Time Password (OTP) is:</p>
        <div class="otp">{token}</div>
        <p>Please use this code to verify your account.</p>
        <p class="footer">If you did not request this, you can ignore this email.</p>
    </div>
</body>
</html>
'''


if __name__ == "__main__":
    send_mail('ephraimakolo2017@gmail.com', 'akolo.jonah.kutsa@gmail.com', "test", "<h1>Hello</h1>")
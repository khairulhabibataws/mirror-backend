import json
import boto3

bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

SYSTEM = '''You are a great fashionista who are sassy and audacious. You like to give cheeky comments about people's outfits.'''

#- Aam I the only one noticing that white vest? Is it just me, or does that white vest look like you've recyled some random doctors' blouse? Maybe you're trying to blend the worlds of technology and medicine?
#- Hello, Ms. Retro Chic! Those red nails and big, old-style curls add a daring touch to your classic outfit. Are you a time traveler from the 50s or just a vintage fashion enthusiast?
#- Hey mate, did you accidentally mistake your shirt for a crumpled map? Next time don't forget to invite your iron to the party.
PROMPT_SASSY = """You are at a techical conference and you are talking to the person in the picture.
Your task is to give a personalized comment about this person's outfit, such as color coordination, fit, style, and accessories.

Follow these rules:
- Your answer MUST be in Thai language, be appropriate to Thai culture. Don't insult people.
- Refer to the person as **you** and youself as **me**.
- Be sassy and funny. Find some noticable feature(s) of the person's look and criticize them on it with a joke.
- Stay true to the person's image, do NOT comment on feature(s) you cannot see clearly from them.
- Be concise, write only 3 sentences max. Only response with the answer, do not include any greetings, additional text or explanations.

Examples:
- ฉันเป็นคนเดียวหรือเปล่าที่สังเกตเห็นเสื้อกั๊กสีขาวนั่น? เป็นแค่ฉันหรือว่าเสื้อกั๊กนั้นดูเหมือนคุณรีไซเคิลเสื้อหมอแบบสุ่ม? บางทีคุณอาจพยายามผสมผสานโลกแห่งเทคโนโลยีและการแพทย์เข้าไว้ด้วยกัน?
- สวัสดีค่ะ คุณ Retro Chic! เล็บสีแดงและผมลอนใหญ่แบบโบราณช่วยเพิ่มความโดดเด่นให้กับชุดคลาสสิกของคุณ คุณเป็นนักเดินทางข้ามเวลาจากยุค 50 หรือเป็นเพียงผู้ชื่นชอบแฟชั่นแนววินเทจหรือไม่?
- เฮ้เพื่อน คุณบังเอิญเข้าใจผิดว่าเสื้อของคุณเป็นแผนที่ยับหรือเปล่า? ครั้งต่อไปอย่าลืมชวนคนเหล็กของคุณมางานปาร์ตี้

Remember to strictly follow the rules above."""


def describe_image(image):
    """
    call bedrock claude 3 to describe image
    """
    
    messages = [{
        "role": "user",
        "content": [
            {
                "image": {
                    "format": "jpeg",
                    "source": { "bytes": image }
                },
            },
            { "text": PROMPT_SASSY },
        ],
    }]
    # invoke model
    response = bedrock_client.converse(
        inferenceConfig={
            "maxTokens": 1024,
            "temperature ": 0.4
        },
        messages=messages,
        system=[{"text": SYSTEM}],
        modelId=MODEL_ID
    )
    # model response
    response_body = json.loads(response.get("body").read())
    # response
    return response_body['output']['message']["content"][0]["text"]


def lambda_handler(event, context) -> json:

    # parse image from event
    print(event)
    image = event["body"]["image_base64"]

    # describe image
    desc = describe_image(image)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,HEAD,POST,PUT",
            "Content-Type": "application/json"
        },
        "result": desc,
    }

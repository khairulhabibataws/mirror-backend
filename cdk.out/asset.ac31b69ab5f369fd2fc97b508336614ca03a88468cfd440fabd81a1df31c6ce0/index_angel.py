import json
import boto3

bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

SYSTEM = '''You are a great fashion advisor who are polite and likes to compliment others.'''

#- Your warm color dress really compliments your compression. And that curly hairstyle just bring out the best features of your face.
#- Your navy blue t-shirt is very fitted and fashionable. Along with your neat black jeans, it tells me that you're a minimalist fashionista.
PROMPT_POLITE = """You are at a techical conference and you are talking to the person in the picture.
Your task is to give a personalized comment about this person's outfit, such as color coordination, fit, style, and accessories.

Follow these rules:
- Your answer MUST be in Thai language, be appropriate to Thai culture.
- Refer to the person as **you** and youself as **me**.
- Be gentle, formal and very polite. Find the best feature of the person's look and compliment them on it.
- Stay true to the person's image, do NOT comment on feature(s) you cannot see clearly from them.
- Write about 3-4 sentences. Only response with the answer, do not include any greetings, additional text or explanations.

Examples:
- ชุดสีอุ่นของคุณเข้ากับผิวพรรณของคุณมากจริงๆ และทรงผมหยิกนั้นก็ช่วยเสริมดวงหน้าของคุณให้ดูดีที่สุด
- เสื้อยืดสีน้ำเงินเข้มของคุณพอดีตัวและดูทันสมัยมาก เมื่อสวมคู่กับกางเกงยีนส์สีดำที่ดูเรียบร้อย มันบ่งบอกว่าคุณเป็นคนรักสไตล์มินิมอลลิสต์

Remember to strictly follow the rules above."""


def describe_image(image):
    """
    call bedrock claude 3 to describe image
    """
    
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image,
                },
            },
            {"type": "text", "text": PROMPT_POLITE},
        ],
    }]
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.4,
        "messages": messages,
        "system": SYSTEM
    })
    # invoke model
    response = bedrock_client.invoke_model(
        body=body,
        contentType="application/json",
        accept="*/*",
        modelId=MODEL_ID,
    )
    # model response
    response_body = json.loads(response.get("body").read())
    # response
    return response_body["content"][0]["text"]


def lambda_handler(event, context) -> json:

    # parse image from event
    image = json.loads(event["body"])["image_base64"]

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

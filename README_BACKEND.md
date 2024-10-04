## Testing Endpoint

Here is a deployed endpoint ready for testing.

```py
https://nssp536cb9.execute-api.us-west-2.amazonaws.com/prod/
```

Just call a POST request with body as below:

```json
{
  "image_base64": "base64 image content"
}
```

For example, let's call a POST request.

```ts
const response = await fetch(ENDPOINT + "angel", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ image_base64: imageBase64 }),
});

// parse response update ui
const json = await response.json();
desc.innerText = json["result"];
```

## Introduction

Implement an api endpoint for describing images using Amazon Bedrock Claude 3 Models.

- A Lambda function implements few short example prompt
- Expose service via API Gateway

Project structure

```py
|--bin
   |--mirror-backend.ts
|--lambda
   |--index_angel.py
   |--index_devil.py
|--lib
   |--mirror-api-stack.ts
|--test
|--package.json
|--tsconfig.json
```

## Deploy CDK Stack

Clone the project

Bootstrap CDK (if you have not)

```py
cdk bootstrap
```

Go into the backend project

Install dependencies

```py
npm install package.json
```

Deploy the infrastructure

```py
export AWS_REGION=us-west-2
cdk --app 'npx ts-node --prefer-ts-exts bin/mirror-backend.ts' synth
cdk --app 'npx ts-node --prefer-ts-exts bin/mirror-backend.ts' deploy MirrorApiStack
```

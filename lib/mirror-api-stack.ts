// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Duration, Stack, StackProps } from "aws-cdk-lib";
import * as aws_lambda from "aws-cdk-lib/aws-lambda";
import * as aws_apigateway from "aws-cdk-lib/aws-apigateway";
import * as aws_iam from "aws-cdk-lib/aws-iam";

import { Construct } from "constructs";
import * as path from "path";

export class MirrorAPIStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    // role for lambda
    const role = new aws_iam.Role(this, "RoleForMirrorLambda", {
      assumedBy: new aws_iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    role.addToPolicy(
      new aws_iam.PolicyStatement({
        effect: aws_iam.Effect.ALLOW,
        actions: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        resources: ["*"],
      })
    );

    role.addToPolicy(
      new aws_iam.PolicyStatement({
        effect: aws_iam.Effect.ALLOW,
        actions: [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
        ],
        resources: [`arn:aws:bedrock:${this.region}::foundation-model/*`],
      })
    );

    // lambda function 1
    const angel_func = new aws_lambda.Function(this, "AngelLambdaFunction", {
      code: aws_lambda.Code.fromAsset(path.join(__dirname, "../lambda")),
      environment: {},
      runtime: aws_lambda.Runtime.PYTHON_3_12,
      memorySize: 2048,
      timeout: Duration.seconds(29),
      handler: "index_angel.lambda_handler",
      role: role,
    });

    // lambda function 2
    const devil_func = new aws_lambda.Function(this, "DevilLambdaFunction", {
      code: aws_lambda.Code.fromAsset(path.join(__dirname, "../lambda")),
      environment: {},
      runtime: aws_lambda.Runtime.PYTHON_3_12,
      memorySize: 2048,
      timeout: Duration.seconds(29),
      handler: "index_devil.lambda_handler",
      role: role,
    });

    // role for api gateway
    const roleForApiGw = new aws_iam.Role(
      this,
      "RoleForApiGwInvokeDrawPublic",
      {
        assumedBy: new aws_iam.ServicePrincipal("apigateway.amazonaws.com"),
      }
    );

    roleForApiGw.addToPolicy(
      new aws_iam.PolicyStatement({
        effect: aws_iam.Effect.ALLOW,
        actions: ["lambda:InvokeFunction"],
        resources: [angel_func.functionArn, `${angel_func.functionArn}:*`, devil_func.functionArn, `${devil_func.functionArn}:*`],
      })
    );

    roleForApiGw.addToPolicy(
      new aws_iam.PolicyStatement({
        effect: aws_iam.Effect.ALLOW,
        actions: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
        ],
        resources: ["*"],
      })
    );

    // apigatway
    const apigw = new aws_apigateway.RestApi(this, "MirrorApiGateway", {
      restApiName: "MirrorApi",
      cloudWatchRole: true,
    });

    // resource 1
    const angel = apigw.root.addResource("angel");

    // method and lambda integration
    angel.addMethod(
      "POST",
      new aws_apigateway.LambdaIntegration(angel_func, {
        credentialsRole: roleForApiGw,
      })
    );

    // enable cors
    angel.addCorsPreflight({
      allowOrigins: ["*"],
      allowMethods: ["GET", "POST", "OPTIONS"],
      allowHeaders: ["*"],
    });

    // resource 2
    const devil = apigw.root.addResource("devil");

    // method and lambda integration
    devil.addMethod(
      "POST",
      new aws_apigateway.LambdaIntegration(devil_func, {
        credentialsRole: roleForApiGw,
      })
    );

    // enable cors
    devil.addCorsPreflight({
      allowOrigins: ["*"],
      allowMethods: ["GET", "POST", "OPTIONS"],
      allowHeaders: ["*"],
    });
  }
}

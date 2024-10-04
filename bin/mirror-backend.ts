import * as cdk from "aws-cdk-lib";
import { MirrorAPIStack } from "../lib/mirror-api-stack";
import { AwsSolutionsChecks, NagSuppressions } from "cdk-nag";

// parameter
const REGION = "us-west-2";
const ACCOUNT = process.env.CDK_DEFAULT_ACCOUNT;

const app = new cdk.App();

// add the cdk-nag with extra verbose logging
cdk.Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));

const backendStack = new MirrorAPIStack(app, "MirrorApiStack", {
  env: {
    region: REGION,
    account: ACCOUNT,
  },
});

NagSuppressions.addResourceSuppressions(
  backendStack,
  [
    {
      id: "AwsSolutions-IAM5",
      reason: "allow lambda to call all FM models in bedrock",
    },
    {
      id: "AwsSolutions-L1",
      reason: "allow to run lambda runtime python 3.11",
    },
    {
      id: "AwsSolutions-IAM4",
      reason: "allow to use managed policy for some",
    },
    {
      id: "AwsSolutions-APIG1",
      reason: "skip api gw loggings",
    },
    {
      id: "AwsSolutions-APIG2",
      reason: "allow api gateway logs",
    },
    {
      id: "AwsSolutions-APIG6",
      reason: "skip api gateway logs",
    },
    {
      id: "AwsSolutions-APIG4",
      reason: "allow public api wo auth",
    },
    {
      id: "AwsSolutions-COG4",
      reason: "allow public api wo auth",
    },
  ],
  true
);

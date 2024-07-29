const crypto = require("crypto");
const moment = require("moment");
const saltedMd5 = require("salted-md5");
const {
   PutItemCommand,
   DynamoDBClient,
} = require("@aws-sdk/client-dynamodb");
const { buildResponse } = require("./utilities");

const config = { region: "us-east-1" };
const client = new DynamoDBClient(config);
const TableName = "tokens";

const handler = async (event) => {
   try {
      const deviceId = "frontEnd-001"
      const expired = 360
      const currentDate = moment();
      const token = saltedMd5(moment().unix(), crypto.randomBytes(16));
      const expiredDate = moment(currentDate)
         .add(expired, "days")
         .toISOString();

      const params = {
         TableName,
         Item: {
            token: { S: token },
            deviceid: { S: deviceId },
            expiredDate: { S: expiredDate },
            createdAt: { S: moment(currentDate).toISOString() },
         },
         ConditionExpression: "attribute_not_exists(deviceId)",
      };

      const command = new PutItemCommand(params);
      await client.send(command);

      const resBody = {
         token,
         deviceId,
         expired: expiredDate,
         createdAt: moment(currentDate).toISOString(),
      };

      return buildResponse(200, "Generate token success", resBody);
   } catch (e) {
      console.info(event)
      console.error("Error generate token : " + e);
      return buildResponse(500, "Generate token error!", e);
   }
};

handler()
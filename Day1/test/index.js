import {SSMClient, GetParametersCommand } from "@aws-sdk/client-ssm"
const ssmClient = new SSMClient({ region: "us-east-1" });

async function waw(){
    const params = {
        Names: [
            "/lks/database/dbname",
            "/lks/database/username",
            "/lks/database/password",
            "/lks/database/endpoint",
         ],
        WithDecryption: true,
     };
  
     try {
        const command = new GetParametersCommand(params);
        const response = await ssmClient.send(command);
        const parameters = {};
  
        response.Parameters.forEach((param) => {
           const keyParts = param.Name.split("/");
           const simplifiedKey = keyParts[keyParts.length - 1];
  
           parameters[simplifiedKey] = param.Value;
        });
  
        console.log(parameters);
     } catch (error) {
        console.error("Error while get parameters: ", error);
        throw error;
     }
}
waw()
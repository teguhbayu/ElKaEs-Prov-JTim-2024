const { buildResponse } = require("./utilities.js");
const { getEvent, getEventById } = require("./lib/controller");

const handler = async () => {
   try {
      const httpMethod = "GET";
      const pathRequest = "/event";

      if (httpMethod == "GET" && pathRequest == "/event") {
         console.log(await getEvent());
      } else if (httpMethod == "GET" && pathRequest == "/event/{id}") {
         const eventId = event.pathParameters.id;
         return await getEventById(eventId);
      } else {
         return buildResponse(400, "BAD REQUEST!", null);
      }
   } catch (e) {
      console.error(`Got error while read Product : ${e}`);
      return buildResponse(500, "Internal Server Error", null);
   }
};

handler()

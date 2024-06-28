// Load the jsonld.js library
const jsonld = require('jsonld');
const fs = require('fs').promises;
const path = require('path');
const { isContext } = require('vm');

// const fs = require('fs');

// Function to read a JSON file
async function readJSONFile(filename) {
  try {
    const data = await fs.readFile(filename, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error(`Error reading file ${filename}:`, err);
    return null;
  }
}


async function main() {
  try {


    // Read graph data
    const graphData = await readJSONFile('graph_data.json');
    if (graphData) {
      console.log('Graph Data:');
      console.log(graphData);
    }

    // Read context data
    const contextData = await readJSONFile('context_data.json');
    if (contextData) {
      console.log('\nContext Data:');
      console.log(contextData);
    }



    // await fs.writeFile('output.json', JSON.stringify(filesObj, null, 2));
    // console.log('Files object written to output.json');


    console.warn('-----------------------')

    // basic (all) data
    const frame0 = {
      "@type": "cmip:institution"
    };

    const frame1 = {
      "@context":
        { "@vocab": "institution:" },
      "@type": "cmip:institution",
    };

    const frame2 = {
      "@context":
        { "@vocab": "institution:" },
      "@type": "cmip:institution",
      "@explicit": true,
    };


    const frame3 = {
      "@context":
        { "@vocab": "institution:" },
      "@type": "cmip:institution",
      "@explicit": true,
      "name": "",
      "ror": ""
    };


    const frame4 = {
      "@context":
      {
        ...contextData,
        "@vocab": "institution:"
      },
      "@type": "cmip:institution",
      "@explicit": true,
      "name": "",
      "ror": "",
      "location": {},
    };


    const frame5 = {
      "@context":
      {
        "@vocab": "institution:",
        "location": {
          "@context": {
            "@vocab": "location:"
          }
        },
      },
      "@type": "cmip:institution",
      "@explicit": true,
      "name": "",
      "location": { "@explicit": true, "lat": {}, "lon": {} },
    };



    const reverseframe = {
      "@context": {
        "@vocab": "institution:",
        "locationOf": {
          "@reverse": "institution:location"
        }
      },
      "@type": "institution:location",

      "@explicit": true,
      "location:country": "",
      "locationOf": { "@explicit": true, "institution:name": "" }
    }


    // const frame = {
    //   "@context": 
    //   {
    //     ...contextData,
    //     // "@vocab": "institution:",


    //   }
    //   ,
    //   "@explicit": true,
    //   "@type": ["cmip:institution", "cmip:consortium"],
    //   'cmip_acronym':"",
    //   'cmip_acronym':["consortium:cmip_acronym","institution:cmip_acronym"]

    // };









    // "@type": ["schema:Book", "schema:Magazine"],

    await jsonld.frame(graphData, frame4)

      // .then((framed) => {

      //   return JSON.stringify(framed)
      // })
      .then(d => d['@graph'][0])//.slice(0,10))
      .then(console.warn);



  } catch (error) {
    console.error('Error:', error);
  }


}

main();

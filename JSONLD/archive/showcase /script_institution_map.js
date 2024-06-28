// Load the jsonld.js library
const jsonld = require('jsonld');
const fs = require('fs').promises;
const path = require('path');
const { isContext } = require('vm');

// const fs = require('fs');

// Function to remove entries with "@" tags recursively
function removeAtTags(obj) {
  for (const key in obj) {
    if (typeof obj[key] === 'object') {
      removeAtTags(obj[key]); // Recursively call for nested objects
    } else if (Array.isArray(obj[key])) {
      obj[key].forEach((item) => removeAtTags(item)); // Recursively call for arrays
    } else if (key.startsWith('@')) {
      delete obj[key]; // Delete entry if key starts with "@"
    }
  }
  return obj;
}




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
    const contextData = await readJSONFile('context_data.json');



    // await fs.writeFile('output.json', JSON.stringify(filesObj, null, 2));
    // console.log('Files object written to output.json');


    console.warn('-----------------------')


    const mapframe = {
      "@context": 
        { "@vocab": "institution:",
        "location": {
          "@context": {
              "@vocab": "location:"
          }
      },
        },
      "@type": "cmip:institution",
      "@explicit": true,
      "name":"",
      "location":{"@explicit":true,"lat":{},"lon":{}},
    };












    // "@type": ["schema:Book", "schema:Magazine"],

    await jsonld.frame(graphData, mapframe)

      // .then((framed) => {

      //   return JSON.stringify(framed)
      // })
      .then(d => {
        
        const newd = removeAtTags(d['@graph'])


        fs.writeFile('sample_generated/latlon_data.json', JSON.stringify(newd,null,4), (err) => {
          if (err) {
            console.error('Error writing to file:', err);
            return;
          }
          console.log('JSON data has been written to data.json');
        });

        return newd

      })
      .then(console.warn);



  } catch (error) {
    console.error('Error:', error);
  }


}

main();

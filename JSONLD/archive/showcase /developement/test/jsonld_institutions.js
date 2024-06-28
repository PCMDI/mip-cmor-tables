// Load the jsonld.js library
const jsonld = require('jsonld');
const fs = require('fs').promises;
const path = require('path');
const { isContext } = require('vm');


async function readDirectory(dirPath) {
  const filesObj = {};

  const files = await fs.readdir(dirPath);
  
  await Promise.all(files.map(async file => {
      const filePath = path.join(dirPath, file);
      const stats = await fs.stat(filePath);
      
      if (stats.isDirectory()) {
          filesObj[file] = await readDirectory(filePath);
      } else {
          if (path.extname(file) === '.json') {
              try {
                  const data = await fs.readFile(filePath, 'utf8');
                  filesObj[file] = JSON.parse(data);
              } catch (error) {
                  console.error(`Error reading JSON file ${filePath}:`, error);
              }
          }
      }
  }));

  return filesObj;
}


async function main() {
    try {
        const directoryPath = './Institutions';
        const filesObj = await readDirectory(directoryPath);

        values = Object.values(filesObj)

        console.log(values)

        // await fs.writeFile('output.json', JSON.stringify(filesObj, null, 2));
        // console.log('Files object written to output.json');



        const frame = {
          "@context":{
            "id": "@id",
            "type": "@type",
            "long_name":"institution:name",
            "ror":"institution:ror",
            // "location":"institution:location",
            "location":{"@context":{
            "@vocab":"location:",
            }
            },
            // "@explicit": true
            "@base":"institution:",
            "@vocab":"institution:",

          },
          "@type": "cmip:institution",
          "long_name": "", // Use the 'a:name' property in the frame
          "ror":"",
          "location":{},
          // "schema:memberOf":{"name":""},
          "@explicit": true,
          "@omitDefault": true,
          "@embed": "@always",
          "@propagateNamespaceRefs": false
        };
        



        await jsonld.frame(values, frame)
        
        // .then((framed) => {

        //   return JSON.stringify(framed)
      
        // })
        .then(d=>d['@graph'][0])
         .then(console.warn);



    } catch (error) {
        console.error('Error:', error);
    }




    const framelatlon = {
      "@context":{
        // "id": "@id",
        // "type": "@type",
        // "long_name":"institution:name",
        // "ror":"institution:ror",
        // "location":"institution:location",
        "@base":"location",
        // "@vocab":"location:"
        "location":"institution:location",
        "@base":"location",
        "@vocab":"location:",

        // "location": {
        //   "@id": "institution:location",
        //   "@type": "@id"
        // },
        // "institute": {
        //   "@id": "cmip:institution",
        //   "@type": "@id"
        // }
        // "@explicit": true
      },
      // "location":{},
      "institution":{},

      // "@type": "location",
      // "location:lat":{},
      // "location:lon":"",
      // "lon":"",
      
      // "long_name": "", // Use the 'a:name' property in the frame
      // "ror":"",
      // "location":{ "@explicit": true,},
      // // "schema:memberOf":{"name":""},
      "@explicit": true,
      // "@omitDefault": true,
      // "@embed": "@always",
      // "@propagateNamespaceRefs": false

    };
    

    // await jsonld.frame(values, framelatlon)
    //  .then(console.warn);


  }

  /*

"@container": "@set",
    "@value": ["Alice", "Bob", "Charlie"]

  "address": {
    "@nest": {
      "street": "123 Main Street",
      "city": "Anytown",
      "country": "USA"
    }

    {
  "@context": {
    "@vocab": "http://schema.org/"
  },
  "@type": "Person",
  "name": "John Doe",
  "jobTitle": "Software Engineer"
}
In this example, the @context sets @vocab to "http://schema.org/", which means that properties like name and jobTitle will be expanded to "http://schema.org/name" and "http://schema.org/jobTitle" respectively when the JSON-LD document is processed.
  
  */

main();

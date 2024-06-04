// Load the jsonld.js library
const jsonld = require('jsonld');
const fs = require('fs').promises;
const path = require('path');
const { isContext } = require('vm');


async function readDirectory(dirPath) {
  const filesObj = { 'context': {}, 'graph': {} };

  const files = await fs.readdir(dirPath);

  await Promise.all(files.map(async file => {
    const filePath = path.join(dirPath, file);
    const stats = await fs.stat(filePath);

    var kind = filePath.includes('context.json') ? 'context' : 'graph'

    if (stats.isDirectory()) {

      if (kind === 'context') {
        filesObj[kind] = { ...filesObj[kind], ...await readDirectory(filePath) }
      } else {
        filesObj[kind][file] = await readDirectory(filePath);
      }
    } else {
      if (path.extname(file) === '.json') {
        try {
          const data = await fs.readFile(filePath, 'utf8');
          if (kind === 'context') {
            filesObj[kind] = { ...filesObj[kind], ...filesObj[kind][file] = JSON.parse(data) }
          } else {
            filesObj[kind][file] = JSON.parse(data)
          }

        } catch (error) {
          console.error(`Error reading JSON file ${filePath}:`, error);
        }
      }
    }
  }));

  // filesObj was a dictionary with filename and contents. 
  // must have context in repo

  console.log(Object.values(filesObj))


  const combinedData = Object.values(filesObj).filter().reduce((result, item) => {
    // Combine context objects
    result.context = { ...result.context, ...item.context };

    // Combine graph objects
    Object.values(item.graph).forEach(obj => {
      result.graph.push(obj);
    });

    return result;

  }, { context: {}, graph: [] });

  return combinedData;
}




async function main() {
  try {
    const directoryPath = './';
    const filesObj = await readDirectory(directoryPath);



    entries = filesObj.map(d=>d['graph'])

    console.log(entries)

    // await fs.writeFile('output.json', JSON.stringify(filesObj, null, 2));
    // console.log('Files object written to output.json');



    const frame = {
      "@context": {
        "id": "@id",
        "type": "@type",
        "long_name": "institution:name",
        "ror": "institution:ror",
        // "location":"institution:location",
        "location": {
          "@context": {
            "@vocab": "location:",
          }
        },
        // "@explicit": true
        "@base": "institution:",
        "@vocab": "institution:",

      },


      "@type": "cmip:institution",
      "long_name": "", // Use the 'a:name' property in the frame
      "ror": "",
      "location": {},
      // "schema:memberOf":{"name":""},
      "@explicit": true,
      "@omitDefault": true,
      "@embed": "@always",
      "@propagateNamespaceRefs": false
    };



    console.log(entries)


    await jsonld.frame(entries, frame)

      // .then((framed) => {

      //   return JSON.stringify(framed)
      // })
      .then(d => d['@graph'][0])
      .then(console.warn);



  } catch (error) {
    console.error('Error:', error);
  }


}

main();


// Load the jsonld.js library
const cld = require('cmip_jld');
// push each function into the global scope
Object.keys(cld).forEach(key => {
  global[key] = cld[key];
});

async function main() {

    const graphData = await cld.readFileFS('graph_data.json');

    const mapframe = {
      "@context":{
        "@vocab":'institution:',
        "location":{"@context":{"@vocab":"location:"}}
      },
      "@type": "cmip:institution",
      "@explicit": true,
      "name": "",
      "location": { "@explicit": true,"lat":"", "lon":"" },
    };

    await jsonld.frame(graphData, mapframe)
      .then(stringify).then(rmld).then(str2JSON)
      .then(json=>writeFile(json,'./lat_lon.json'))


}

main();

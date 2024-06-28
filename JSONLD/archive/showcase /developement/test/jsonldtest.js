// Load the jsonld.js library
const jsonld = require('jsonld');

// Define your JSON-LD data
const data = [
  {
    "@id": "http://example.org/organizations/1",
    "@type": "schema:Organization",
    "schema:name": "Organization A"
  },
  {
    "@id": "http://example.org/organizations/2",
    "@type": "schema:Organization",
    "schema:name": "Organization B"
  },
  {
    "@id": "http://example.org/people/1",
    "@type": "schema:Person",
    "schema:name": "John Doe",
    "memberOf": {
      "@id": "http://example.org/organizations/1"
    }
  },
  {
    "@id": "http://example.org/people/2",
    "@type": "schema:Person",
    "schema:name": "Jane Smith",
    "schema:memberOf": {
      "@id": "http://example.org/organizations/2"
    }
  },
  {
    "@context":  {"name": "keep:name"},
    "@id": "http://example.org/people/3",
    "@type": "schema:Person",
    "schema:name": "Alice Johnson",
    "schema:memberOf": {
      "@id": "http://example.org/organizations/1"
    }
  }
];


// const frame = {
//   "@context": {
//     // "@base": "http://example.org/",
//     // "@vocab": "http://schema.org/",
//     // "keep":"aaa"
//     [
//     {
//       "@base": "http://example.org/"
//     },
//     {
//       "@base": "keep"
//     }
//     ]
//   },

//     "@type": "schema:Person",
//   	"keep.name": {"@id":{}},
//     // "schema:memberOf": { },
//     "@explicit": true,
//     "@omitDefault": true,
//     "@embed": "@always"
// }


const frame = {
  "@context":{
    "name":"schema:name"
  },
  "@type": "schema:Person",
  "name": "", // Use the 'a:name' property in the frame
  "schema:memberOf":{"name":""},
  "@explicit": true,
  "@omitDefault": true,
  "@embed": "@never",
  "@propagateNamespaceRefs": true,
  "@vocab":"location:",
};

// const context = {
//   "name":"keep:name"
// };


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



function cleanAll(x){
    return x['@graph']
    // .map(removeAtTags)
}
// Remove "@" tagged entries
// const cleanedObject = removeAtTags(jsonldObject);




// frame a document
jsonld.frame(data ,frame,(err, framed) => {
    // document transformed into a particular tree structure per the given frame



    return framed

  }).then(cleanAll).then(d=>{ console.log(d); return JSON.stringify(d)})
   .then(console.warn);


   console.log(jsonld.frame)
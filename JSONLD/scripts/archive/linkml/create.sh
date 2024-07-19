#! /bin/bash

linkml-validate -s personinfo.yaml better-data.yaml

linkml-validate -s linked.yaml data.yaml 

gen-json-schema linked.yaml --top-class Container > linked.schema.json


gen-context --format jsonld institution.yaml > institution.context.jsonld


https://jmespath.org/
https://jmespath.org/tutorial.html

reservations[].instances[?state == 'terminated']

{
  "reservations": [
    {
      "instances": [
        {"state": "running"},
        {"id":2,"state": "stopped"}
      ]
    },
    {
      "instances": [
        {"id":3,"state": "terminated"},
        {"state": "running"}
      ]
    }
  ]
}


# can use loaded objects as python classes with
https://linkml.io/linkml/generators/python.html


gen-jsonld-context linked.yaml > linked.context.json
gen-jsonld linked.yaml > ld.json

> linked.context.json

gen-erdiagram org.yaml 


gen-doc linked.yaml --directory docs

gen-erdiagram linked.yaml > graph.md

gen-excel linked.yaml --output personinfo.xlsx

linkml-lint schema.yaml


rdf linkml-convert -s personinfo.yaml data.json -o data.ttl

https://linkml.io/linkml/examples.html


plaintext
Copy code
*[?matches(@.cmip_acronym, '^PCM.*DI$')]
This example matches objects where cmip_acronym starts with "PCM" and ends with "DI".

Combined Conditions
You can combine conditions using logical operators (&&, ||, !) and parentheses for grouping:

plaintext
Copy code
*[?starts_with(@.cmip_acronym, 'PCM') && ends_with(@.cmip_acronym, 'DI')]





gen-jsonld-context institutions.yaml







# sdalkflksdj

gen-jsonld-context instituitons.yaml > context.json

linkml-validate -s instituitons.yaml cams.yaml
No issues found

gen-jsonld instituitons.yaml > data.jsonld


linkml-convert -s instituitons.yaml cams.yaml -tjson-ld -o ldcams.json
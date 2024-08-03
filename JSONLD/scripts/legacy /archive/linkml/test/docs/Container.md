

# Class: Container



URI: [https://w3id.org/linkml/examples/personinfo/:Container](https://w3id.org/linkml/examples/personinfo/:Container)






```mermaid
 classDiagram
    class Container
    click Container href "../Container"
      Container : persons
        
          
    
    
    Container --> "*" Person : persons
    click Person href "../Person"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [persons](persons.md) | * <br/> [Person](Person.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/examples/personinfo





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/linkml/examples/personinfo/:Container |
| native | https://w3id.org/linkml/examples/personinfo/:Container |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Container
from_schema: https://w3id.org/linkml/examples/personinfo
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/examples/personinfo
    rank: 1000
    multivalued: true
    domain_of:
    - Container
    range: Person
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: Container
from_schema: https://w3id.org/linkml/examples/personinfo
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/examples/personinfo
    rank: 1000
    multivalued: true
    alias: persons
    owner: Container
    domain_of:
    - Container
    range: Person
    inlined: true
    inlined_as_list: true

```
</details>
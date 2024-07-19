```mermaid
erDiagram
Person {
    string id  
    string full_name  
    stringList aliases  
    string phone  
    integer age  
}
Container {

}

Container ||--}o Person : "persons"

```


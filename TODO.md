# WGCM Vocabulary
Everything Vocabulary related  
xxxDD : datadescriptor with :

* Pydantic model of this DD
* Context for ld part of jsonld
* Term in json with a @context pointing to the context.jsonld

# Directory Structure

_archive/   
dataDescriptor/   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;institutionDD/ # as example  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       _context.jsonld  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        _pydantic_model.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        term1.json  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        term2.json   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        ...  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    otherDD/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        samefilestructure   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ...DD/   

src/ # all scripts used to create/fill datadescriptor

license # untouch  
readme.md # untouch  
todo.md # just to see where i am and what im planning to do   

# TODO List : 


## DD List 

| frequencyDD |  Done  |
| --------------- |---------------|
| activityDD|  Done (BUT need predicate def)  |
| experimentDD|  Done (BUT need predicate def) |   
| reportingIntervalDD| (as frequency need rename ?) Done | 
| gridLabelDD|  
| sourceDD|  Done |
| resolutionDD |Done|
| License | Done |
| variableRootDD | 
| datasetVariantDD|  
| directoryDateDD  | 
| datasetEditionDD  |
| brandingSuffixDD | 
| archiveDD | 
| hostCollectionDD|  
| standardNameDD | 
| dataNodeDD  |
| datasetGroupDD|  
| organisationDD|
| institutionDD |
| consortiaDD |
| nominal- ResolutionDD (nominalResolutionDD) |Done| 
| productTypeDD  |
| realmDD |Done |
| model_component | Done (But only from CMIP6Plus) |
| dataRegionDD  |
| sourceTypeDD | Done|  
| varGroupingCDD  |
| datasetStatusDD  |
| inCollectionsDD  |
| temporalLabelDD  |
| verticalLabelDD  |
| horizontalLabelDD | 
| areaLabelDD  |
| realizationDD | 
| initializationDD|  
| physicsDD  |
| forcingDD  |
| dataConventionsDD|  
| dateCreatedDD**  |
| uniqueFileidDD  |
| variableTableDD  |
| longNameDD  |
| varDefQualifierDD|  
| datasetSpecsDD|  
| gridTypeDD  |
| longInstitutionDD|  
 
## Choose DD
### find relevant Ontology to describe each attribute of each DD
### Define each => Pydantic model


## Currently
### Pydantic models
``` mermaid
---
title: es-vocab pydantic models 
---
classDiagram
    Experiment "1" --> "*" Activity
    Experiment "1" --> "*" SubExperiment
    Experiment "1" --> "*" SourceType


    class Frequency{
    id: str 
    description :str
    long_name :str 
    name : str 
    unit : str 
    type : str 
    
    }
    class Activity{

    id: str 
    validation_method: str = "list"
    name: str 
    long_name: str 
    cmip_acronym: str 
    url: Optional[str] 

    }
    
    class Experiment{
        id: str 
    validation_method: str = Field(default ="list")
    activity: List[str] = Field(default_factory=list)
    description: str 
    tiers: Optional[str] 
    experiment_id: str 
    sub_experiment_id: Optional[List[str]] 
    experiment: str 
    required_model_component: Optional[List[str]] 
    additionnal_allowed_model_components: Optional[List[str]] 
    start_year: Optional[int] 
    end_year: Optional[int] 
    min_numbers_yrs_per_sim: Optional[str] 
    parent_activity_id: Optional[List[str]] 
    parent_experiement_id: Optional[List[str]] 

    }
    class SubExperiment{

    id: str 
    description :str
}
     class SourceType{

    id: str 
    description :str
}   


class Resolution {



    id: str 
    description :str
    value :str 
    name : str 
    unit : str 
    type : str 
}
class Realm {



    id: str 
    description :str
    name : str 
    type : str 
}


class ModelComponent{



    id: str 
    description :str
    name : str 
    type : str
    realm : dict
    nominal_resolution : dict
}


ModelComponent "1" --> "1" Realm
ModelComponent "1" --> "1" Resolution
class Source{   
    id: str 
    validation_method: str = Field(default = "list")
    activity_participation: Optional[List[str]] 
    cohort: List[str] = Field(default_factory=list)
    organisation_id: List[str] = Field(default_factory=list)
    label : str
    label_extended: Optional[str] 
    license: Optional[Dict] 
    model_component: Optional[dict] 
    release_year: Optional[int] 
}

Source "1" --> "1_*" ModelComponent
Source "1" --> "1" Activity
Source "1" --> "1" Organisation

class License{

    id: str 
    kind: str 
    license: Optional[str] 
    url: Optional[str] 
}
Source "1" --> "1" License


```
#### TODO : upgrade pydantic with embeded object 
for now the pydantic model only check/code the id (as str) .. do we propagate to include the entire object pointed by the id ?  


## Ontology : predicates use with ld part 
``` mermaid
---
title: es-vocab Ontology

---
classDiagram
    note "
    # fonts
    𝗯𝗼𝗹𝗱 : 𝗺𝗮𝗻𝗱𝗮𝘁𝗼𝗿𝘆
    other : optionnal
    
    # prefixes
    esv : http://es-vocab.ipsl.fr/
    sch : http://schema.org/
    "
    `𝗲𝘀𝘃:𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁` "1" --> "*" `𝗲𝘀𝘃:𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆`
    `𝗲𝘀𝘃:𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁` "1" --> "*" `𝗲𝘀𝘃:𝘀𝘂𝗯_𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁`
    `𝗲𝘀𝘃:𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁` "1" --> "*" `𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲_𝘁𝘆𝗽𝗲`



    class `𝗲𝘀𝘃:𝗳𝗿𝗲𝗾𝘂𝗲𝗻𝗰𝘆`{
    𝗲𝘀𝘃:𝗶𝗱
    𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
    𝘀𝗰𝗵:𝗮𝗹𝘁𝗲𝗿𝗻𝗮𝘁𝗲𝗡𝗮𝗺𝗲
    𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
    𝘀𝗰𝗵:𝘂𝗻𝗶𝘁𝗧𝗲𝘅𝘁
    
    }
    class `𝗲𝘀𝘃:𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆`{
    𝗲𝘀𝘃:𝗶𝗱
    𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
    𝘀𝗰𝗵:𝗮𝗹𝘁𝗲𝗿𝗻𝗮𝘁𝗲𝗡𝗮𝗺𝗲
    𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
    ??? for cmip_acronym
    sch:url 

    }
    
    class `𝗲𝘀𝘃:𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁`{
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        ??? tier
        ??? sub_experiment_id
        𝘀𝗰𝗵: 𝗱𝗶𝘀𝗮𝗺𝗯𝗶𝗴𝘂𝗮𝘁𝗶𝗻𝗴𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 
        ??? 𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁
        ??? additional_allowed_model_component
        sch:startDate To be consistent it would be ISO8601 date format
        sch:endDate To be consistent it would be ISO8601 date format
        ??? min_number_yrs_per_sim
        esv:activity
        esv:experiment
    }

     class `𝗲𝘀𝘃:𝘀𝘂𝗯_𝗲𝘅𝗽𝗲𝗿𝗶𝗺𝗲𝗻𝘁`{
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        } 

    class  `𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲_𝘁𝘆𝗽𝗲`{
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        } 

    class `𝗲𝘀𝘃:𝗿𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻`{
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        𝘀𝗰𝗵:𝘃𝗮𝗹𝘂𝗲

        𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
        𝘀𝗰𝗵:𝘂𝗻𝗶𝘁𝗧𝗲𝘅𝘁

} 
    class `𝗲𝘀𝘃:𝗿𝗲𝗮𝗹𝗺 ` {
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        𝘀𝗰𝗵:𝗻𝗮𝗺𝗲


} 

    class `𝗲𝘀𝘃:𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁` {
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
        𝗲𝘀𝘃:𝗿𝗲𝗮𝗹𝗺 
        𝗲𝘀𝘃:𝗿𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻`


} 

`𝗲𝘀𝘃:𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁` "1" --> "1" `𝗲𝘀𝘃:𝗿𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻`

`𝗲𝘀𝘃:𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁` "1" --> "1" `𝗲𝘀𝘃:𝗿𝗲𝗮𝗹𝗺 `

    class `𝗲𝘀𝘃:𝗹𝗶𝗰𝗲𝗻𝘀𝗲` {
            𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
        𝘀𝗰𝗵:𝘂𝗿𝗹
}


    class `𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲` {
        𝗲𝘀𝘃:𝗶𝗱
        𝘀𝗰𝗵:𝗻𝗮𝗺𝗲
        𝘀𝗰𝗵:𝗱𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻
        sch:alternativeName
        ??? esv:cohort
        ??? 𝗲𝘀𝘃:𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆_𝗽𝗮𝗿𝘁𝗶𝗰𝗶𝗽𝗮𝘁𝗶𝗼𝗻
        𝗲𝘀𝘃:𝗼𝗿𝗴𝗮𝗻𝗶𝘀𝗮𝘁𝗶𝗼𝗻

        sch:releaseDate 
        𝗲𝘀𝘃:𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁_𝗰𝗼𝗺𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻
        𝗲𝘀𝘃:𝗿𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻`


} 

`𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲`  "1" --> "1_*" `𝗲𝘀𝘃:𝗺𝗼𝗱𝗲𝗹_𝗰𝗼𝗺𝗽𝗼𝗻𝗲𝗻𝘁` 
`𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲`  "1" --> "1" `𝗲𝘀𝘃:𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆`
`𝗲𝘀𝘃:𝘀𝗼𝘂𝗿𝗰𝗲`  "1" --> "1" `e𝘀𝘃:𝗼𝗿𝗴𝗮𝗻𝗶𝘀𝗮𝘁𝗶𝗼𝗻`



```
# Define together Mandatory/optionnal 
for now, it is only a first guess 

# Predicate to find or define

* every type/DD  
   
* cmip_acronym
* tier
* sub_experiment => DD ?
* model_component => DD
* additionnal_allowed_component => DD
* min_number_yrs_per_sim
* cohort for sourceDD
* model_component_composition ?? 
* activity_participation
* region in grid ??


# Subtlety :

* i changed all id in lower case => is it an issue ?
=> Have to TEST the framing to see if "-" or "_" works 

* in experiement terms : the key "experiment" seems to be a description ?? why "experiment" ? 


* i changed the "none" and "" into null in experiment terms for min_numbers_yrs_per_sim => issues ?
this one is for CMOR => we have if CMOR can deal None ? null ? caution : "not specified"

* it is in experiment_id there is an issue : why not : "source_type" and "additionnal_allowed_source_type" ?
=> change into source_type if CMOR doesnt look for that

* in CMIP6Plus JsonldIII =>
source_id => giss-e2-1-g
model-component with id : "varies with pysics" appears 2 times (OK) pointing to same object (Not OK)

* license is "sub class" in source to add specific info
=> Perfect
---

* Organisations Terms are build from institutions AND consortia => (Review in consortia  (with "_" at start) appears in organisation

* grid region seems wrong 


# To investigate

### LD Consortia 
* in consortia context => consortium ?? consortia
* status => Need enumrate ? + Need predicate
* phase ?? mip-era ?? or everything possible ? 


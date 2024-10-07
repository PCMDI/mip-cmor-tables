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

frequencyDD  Done
activityDD  
    find or define predicate cmip_acronym  
experimentDD  
reportingIntervalDD  
gridLabelDD  
sourceDD  
variableRootDD  
datasetVariantDD  
directoryDateDD   
datasetEditionDD  
brandingSuffixDD  
archiveDD  
hostCollectionDD  
standardNameDD  
dataNodeDD  
datasetGroupDD  
sourceInstitutionDD  
nominal- ResolutionDD (nominalResolutionDD)  
productTypeDD  
realmDD  
dataRegionDD  
sourceTypeDD  
varGroupingCDD  
datasetStatusDD  
inCollectionsDD  
temporalLabelDD  
verticalLabelDD  
horizontalLabelDD  
areaLabelDD  
realizationDD  
initializationDD  
physicsDD  
forcingDD  
dataConventionsDD  
dateCreatedDD**  
uniqueFileidDD  
  
variableTableDD  
longNameDD  
varDefQualifierDD  
datasetSpecsDD  
gridTypeDD  
longInstitutionDD  

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


```
### Ontology
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


```
# Predicate to find or define

* cmip_acronym
* tier
* sub_experiment => DD ?
* model_component => DD
* additionnal_allowed_component => DD
* min_number_yrs_per_sim

# Subtlety :

* i changed all id in lower case => is it an issue ? 

* in experiement terms : the key "experiment" seems to be a description ?? why "experiment" ? 

* i changed the "none" and "" into null in experiment terms for min_numbers_yrs_per_sim => issues ?

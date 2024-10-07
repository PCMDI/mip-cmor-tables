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

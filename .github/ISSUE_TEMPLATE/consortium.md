---
name: Consortium
about: Adding a new, or updating an existing, consortium
title: 'Review request for change in consortium'
labels: 'consortium'
assignees: ''

---

# Add Consortium Template

To request a new item, please amend the template below to reflect the items you are interested in.

Relevant conditions and naming conventions for this item can be found using the wiki pages [here]().

## Amending Information on an Existing Item

If you wish to amend an item, please supply only the fields you are interested in and ensure that you change the *action* field to *update*.

``` action = update ```

<!---  info 

We are trialing the addition of new components using the configuration file format. 
To use this, please fill out the template below, keeping the spacing and indentation of the file.

--->

## Contents (What We Wish to Add)



``` configfile


[consortium]
    Acronym = "CMIP"
    Name = "Coupled Model Intercomparison Project"
    
    [institutions]
        cmip6_acronyms = [
                "CMIP-IPO",
                "WCRP"
            ]
    # nest institutions here, use the cmip acnronyms which they have been registered with.


```


## To test what should a model file look like and how to implement it

### Goal
* have a position property (so the position of the model is same after serialized)
* have connectors and connections property (so the lines are loaded properly)
* have all the field data serialized (so the lines are connected to the 
correct connector and load the content in a constant field)


### Example content of the model file

    model1
        prop = ...
        prop = ...
        connector = {ref, ref, ref}
        
    ref  # connector
        prop = ...
        pos = (x, y)
        line = {ref, ref}
        
    ref  # connector
        ...
    
    ref # line
        connectorA = ...  # parent
        connectorB = ...
        
    executable
        # content of the executable file; the current content in the .dat
        model:
            ...
        namespace:
            ...
            

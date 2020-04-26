### Suggestions Welcome!
All suggestion must come from the "issue" tracker and tagged as "suggestion".
If your suggestions gets approved, you'll see your issue tag on the
TODO list!

### Releasing Bug Information
Bugs go through the issue tracker. This is still under heavy-development,
so small bugs no need to be issued *for now*.

##### Software
[Desktop Platform (Win10, Linux:Gnome, MacOS, etc.)]  
[Software Version (Indev 1.0, 0.2.1, etc.)]

##### Effect
What effect had it made on software or interfering external application?

##### Expected Result
What did you expect?

##### Things Attempted
What things have you attempted?

Things can try. __(At your own risk!)__
* Force close the software
* Re-install the software

## Known Issue

## TODO

#### Next Release Candidates
- Add an option "Load Empty" when the file failed to load
- README.md: Add an installation info
- ... we'll be using Cx_freeze for making executables for distribution
- The text size changes on the QComboBox on the side of each Model Workspace
- Add an delete button on top corners of each Node to delete the relative Node
- Add a pre-process normalize image node
- Add read image node
- Ask to save the project (if not saved) after the user decides to quit
- Don't save model to the `project.yaml` if the user hadnt click [save model]
- When adding new model, instead of always locating at the same position, choose diff. pos.
- Add a tree to organize the nodes that is starting to get a lot
- Add zooming and panning for bigger nodes

#### Near Future (Ordered)
- A better way to create nodes
- Serializing Constant Field based on objects instead of relying on names (possible duplicate names)
- More descriptive errors
- Support circular reference for executing nodes (will implemented when needed)
- Text break when the Model Workspace Title reach pass a limit
- Add a boosting/bagging model

#### Vision
- Move codebase from Python to possibly C++/C, Rust
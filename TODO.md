### Suggestions Welcome!
All suggestion must come from the "issue" tracker and tagged as "suggestion".
If your suggestions gets approved, you'll see your issue tag on the
TODO list!

### Releasing Bug Information
Bugs go through the issue tracker. This is still under heavy-development,
so small bugs no need to be issued *for now*.

##### Software
Platform:
Version: (the software is not strictly following versions yet)

##### Effect
What effect had it made on software or interfering external application?

##### Expected Result
What did you expect?

##### Things Attempted
What things have you attempted?

Things you can try. __(At your own risk!)__
* Force close the software
* Re-install the software

## Known Issue

## TODO

#### Next Release Candidates
- Add an option "Load Empty" when the file failed to load
* The text size changes on the QComboBox on the side of each Model Workspace
* Add an delete button on top corners of each Node to delete the relative Node
- Add a pre-process normalize image node
- Add read image node
- Ask to save the project (if not saved) after the user decides to quit
- Update the status bar
- Add grid-lines for workspace to diff. between moving view and discrete nodes
- Executor check for checked errors

#### Near Future (Ordered)
- A better way to create nodes
- Serializing Constant Field based on objects instead of relying on names (possible duplicate names)
- More descriptive errors
- Support circular reference for executing nodes (will implemented when needed)
- Text break when the Model Workspace Title reach pass a limit
- Add a boosting/bagging model
- Reogranize internal nodes and executor functionality of nodes
- Texture.data file of some sort for storing default textures/colors
- Maybe merge neural network to matrix
- Report unused variables per fields in nodes

###### Nodes
- The CSV Read nodes should able to hold multiple output (y-values) too
- Uniform output (esp. Pandas needs be with Numpy's output format)

#### Vision
- Move codebase from Python to possibly C++/C, Rust
- Canidates:
  - Rust / 2D Rust Lib
  - C Backend / Python
  - C++ / Qt5
  - Rust
  - C++ & QML/JS

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
* Add an delete button on top corners of each Node to delete the relative Node
- Add a pre-process normalize image node
- Add read image node
- Ask to save the project (if not saved) after the user decides to quit
- #Update the status bar
- Add grid-lines for workspace to diff. between moving view and discrete nodes
- Executor check for checked errors
- Maybe merge neural network to matrix (reogranize name)
- Changed all the Sklearn backend to Tensorflow (resulting smaller binaries)

#### Near Future (Ordered)
- Error suite:
  - show red border (or other symbols) to signify where the error occured in the node
  - show console of where the error is instead of showing a Dialogue Box
  - be descriptive
  - Report unused variables per fields in nodes (internal)

- A better way to create nodes
- Serializing Constant Field based on objects instead of relying on names (possible duplicate names)

- Text break when the Model Workspace Title reach pass a limit
- Add a boosting/bagging model
- Texture.data file of some sort for storing default textures/colors
- Support circular reference for executing nodes (will implemented when needed)

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

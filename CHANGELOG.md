## Indev 13.2 [March 21, 2020]
* Fixed the `executor` problem
* Further improvement on serialization though broken still
* Models are removable from the project reference
    * Users has to manually delete the actual file data
* Changed `pip` to `pip3` in .travis.yml
    *  <https://stackoverflow.com/questions/59981615/receiving-error-when-trying-to-install-pyqt5-package-on-pycharm-on-ubuntu-18-04>

## Indev 13.1b [March 20, 2020]
* removed os from .travis.yml to default

## Indev 13.1a [March 20, 2020]
* .travis.yaml -> .travis.yml

## Indev 13.1 [March 20, 2020]
* Cleaned up the repository and files
* Added unit/integration tests

## Indev 13.0 [March 20, 2020]
* Fixed the connector's initiation position
* **Models are now serializable!** (Or at least somewhat)
  * Allows for deployment
  * Added multiple model workspace
  * Saves the visual progress (e.g. lines, node position)
  * And many more features yet to come stemming from this
  * NOTE: load_proj() currently returns partially restored object state
* Refactored some components (Project File Interface & Model Manager)
* Re-organized some GUI components

## Indev 12.2 [Feb 24, 2020]
* Added Standard Decision Tree Classifier
* Added SVM (Support Vector Machine)
* Added a colored version for numerical only input line
    * WHITE: Generic (names, files, ...)
    * GREEN: Integer Only (numerical, operand, ...)

## Indev 12.1 [Feb 23, 2020]
* Code Cleanup
* Added KMean
* Added an example

## Indev 12.0 [Feb 23, 2020]
* Revamp on executor
* More models
* More major changes

## Indev 11.0 [Jan 12, 2020]
* The model input and output now uses tag names instead of file location (ease of use)
* Changed the project input into a file dialogue
* Added ML models
* Added the project directory on the left-panel (WIP)

## Indev 10.2 [Jan 3, 2020]
* Reorganized the project workspace
* Changed some other front-end feature (meaning some new things have no
back-end code to execute it)

## Indev 10.1 [Jan 3, 2020]
* Fixed the problems with the output data of the model
* Changed README.md

## Indev 10.0 [Jan 2, 2020]
* Full Code Refactoring
* PyQt Library states I can use Apache License so long I only distribute 
only my part of the source code
    * <https://softwareengineering.stackexchange.com/a/235846>
    * <https://github.com/Werkov/PyQt4/blob/master/GPL_EXCEPTION.TXT>

## Indev 9.1 [Nov 25, 2019]
* Working makeshift AI models
* Other minor changes

## Indev 9.0 [Nov 17, 2019]
* Added (defunct) AI models
* Replaced version 3.6 to 3.8 in Travis
* Added dummy type system to the executor (later to be actual type system)
* Refactored the components
* Added a search bar instead of using keyboard to select models individually

## Indev 8.1 [Nov 11, 2019] (MVP)
* Working models
* New project listed in the config.yaml automatically gets initialized
* Polished the execution process
    * Added input backflow
    * Other small changes...

## Indev 8.0 [Nov 8, 2019]
* Execution process working

## Indev 7.0 [Nov 5, 2019]
* Added Models
* Working on execution process

## Indev 6.0 [Nov 3, 2019]
* Added input text field

## Indev 5.1 [Oct 16, 2019] (TGR1b)
* __The Great Refactor #1__ ends
* cleaning-up refactor artifacts
* refactor polishing
    * remove, now, useless files and directory
    * bug: input field can connect to the output field of the same box
* sphinx was overkill

## Indev 5.0 [Oct 15, 2019]
* finish redirecting code
* code cleanup
    * 50 lines of mess is cleaned up in `main.py`
    * removed old codebase
* documenting documentation for users

## Indev 4.0 [Oct 9, 2019]
* redirected the main code to the new codebase
* smooth clicking on nodes

## Indev 3.0 [Oct 1, 2019] (TGR1a)
* __The Great Refactor #1__ starts
    * added the code to setup for change of codebase
    * original code still running

## Indev 2.1(a, b, c, d) [Sep 27, 2019]
* Minor change to README
* Testing Travis #1-4

## Indev 2.0 [Sep 27, 2019]
* Added the basic framework for the backend (AI part)
* Minor Changes to the frontend (GUI)
* Organized Code
* Added Travis-CI to the project
    * Learning how CI works!

## Indev 1.1 [Sep 25, 2019]
* Added CHANGELOG for tracking updates
* Added more stuff into README
* TODO added for anyone suggesting stuff
* DOC added for now as a software reference and tutorial

## Indev 1.0 [Sep 25, 2019]
* Published project to the GitHub repository
* Project code-named "Hexacone" (don't ask why)
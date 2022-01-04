import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:convert';


enum AttributeLocation {
  input,
  output
}


enum AttributeDataType {
  fileContentInp,
  fileContentOut,
}


class AttrDescriptor {
  AttrDescriptor(
      String this.name,
      AttributeLocation this.location,
      AttributeDataType this.dtype);

  String name;
  AttributeLocation location;
  AttributeDataType dtype;
  var attrData;  // defined later
  var fileName = "Empty File";  // optional
}


class ModelExecute extends StatefulWidget {
  ModelExecute({Key? key}) : this.state = _ModelExecuteState(), super(key: key);

  _ModelExecuteState state;

  @override
  _ModelExecuteState createState() {
    return state;
  }
}

class _ModelExecuteState extends State<ModelExecute> {
  final _formKey = GlobalKey<FormState>();

  List<AttrDescriptor> modelInpAttrData = [];
  List<AttrDescriptor> modelOutAttrData = [];

  void addAttr(String name, AttributeLocation location, AttributeDataType dtype) {
    if(location == AttributeLocation.input) {
      modelInpAttrData.add(AttrDescriptor(name, location, dtype));
    } else {
      modelOutAttrData.add(AttrDescriptor(name, location, dtype));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Model Execute"),
      ),
      body: Form(
        key: _formKey,
        child: Column(
          children: <Widget>[
            Row(
              children: <Widget>[
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      children: <Widget>[
                        const Text(
                          "Input/Source Location(s)",
                          style: TextStyle(
                            fontSize: 24,
                          ),
                        ),
                        Container(
                          height: 500,
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: Colors.black,
                              width: 3,
                            ),
                          ),
                          child: ListView.builder(
                            scrollDirection: Axis.vertical,
                            padding: const EdgeInsets.all(7.0),
                            itemCount: modelInpAttrData.length,
                            itemBuilder: (BuildContext context, int index) {
                              if(modelInpAttrData[index].dtype == AttributeDataType.fileContentInp) {
                                return constructAttrFileInp(modelInpAttrData[index]);
                              } else if(modelInpAttrData[index].dtype == AttributeDataType.fileContentOut) {
                                return constructAttrFileOut(modelInpAttrData[index]);
                              }
                              return const Text("None");
                            }
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                Container(
                  width: 20,
                  child: const VerticalDivider(
                    color: Colors.black,
                    thickness: 3,
                    indent: 10.0,
                    endIndent: 10.0,
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      children: <Widget>[
                        const Text(
                          "Output/Destination Location(s)",
                          style: TextStyle(
                            fontSize: 24,
                          ),
                        ),
                        Container(
                          height: 500,
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: Colors.black,
                              width: 3,
                            ),
                          ),
                          child: ListView.builder(
                              scrollDirection: Axis.vertical,
                              padding: const EdgeInsets.all(7.0),
                              itemCount: modelOutAttrData.length,
                              itemBuilder: (BuildContext context, int index) {
                                if(modelOutAttrData[index].dtype == AttributeDataType.fileContentInp) {
                                  return constructAttrFileInp(modelOutAttrData[index]);
                                } else if(modelOutAttrData[index].dtype == AttributeDataType.fileContentOut) {
                                  return constructAttrFileOut(modelOutAttrData[index]);
                                }
                                return const Text("None");
                              }
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            Container(
              padding: EdgeInsets.all(5.0),
              child: ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text("Executing model...")),
                      );
                    }
                  },
                  child: Text("Execute")
              ),
            ),
            Container(
              padding: EdgeInsets.all(5.0),
              child: ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: Text("Find new model")
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget constructAttrFileInp(AttrDescriptor attrDescrp) {
    return Container(
      height: 50,
      width: 50,
      color: Colors.black12,
      alignment: Alignment.center,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          const SizedBox(width: 20),
          Text(
            attrDescrp.name,
            style: const TextStyle(
              fontSize: 24,
              backgroundColor: Colors.amber,
            ),
          ),
          const SizedBox(width: 20),
          ElevatedButton(
              onPressed: () async {
                FilePickerResult? result = await FilePicker.platform.pickFiles();

                if (result != null) {
                  debugPrint(utf8.decode(result.files.single.bytes ?? <int>[]));
                  debugPrint(result.files.single.name);

                  setState(() {
                    attrDescrp.fileName = result.files.single.name;
                    attrDescrp.attrData = utf8.decode(result.files.single.bytes ?? <int>[]);
                  });
                } else {
                  // User canceled the picker
                }
              },
              child: const Text("Open File")
          ),
          const SizedBox(width: 20),
          Text(
            "${attrDescrp.fileName}",
            style: const TextStyle(
              fontStyle: FontStyle.italic,
            ),
          )
        ],
      ),
    );
  }

  Widget constructAttrFileOut(AttrDescriptor attrDescrp) {
    return Container(
      height: 50,
      width: 50,
      color: Colors.black12,
      alignment: Alignment.center,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          const SizedBox(width: 20),
          Text(
            attrDescrp.name,
            style: const TextStyle(
              fontSize: 24,
              backgroundColor: Colors.amber,
            ),
          ),
          const SizedBox(width: 20),
          ElevatedButton(
              onPressed: () async {
                String? outputFile = await FilePicker.platform.saveFile(
                  dialogTitle: 'Please select an output file:',
                  fileName: 'output_${attrDescrp.name}.pdf',
                );

                if (outputFile != null) {
                  debugPrint(outputFile);
                } else {
                  // User canceled the picker
                }
              },
              child: const Text("Open File")
          ),
          const SizedBox(width: 20),
          Text(
            "${attrDescrp.fileName}",
            style: const TextStyle(
              fontStyle: FontStyle.italic,
            ),
          )
        ],
      ),
    );
  }
}

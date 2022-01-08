import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:file_picker_cross/file_picker_cross.dart';
import 'dart:typed_data';
import 'package:http/http.dart' as http;


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
  var attrData = "";  // defined later
  var fileName = "Empty File";  // optional, TODO: make this nullable to clarify from the empty file string counterpart
  String? fileExt;  // optional
}


class ModelExecute extends StatefulWidget {
  ModelExecute({required this.modelKey, Key? key}) : this.state = _ModelExecuteState(modelKey: modelKey), super(key: key);

  final String modelKey;
  _ModelExecuteState state;

  @override
  _ModelExecuteState createState() {
    return state;
  }
}

class _ModelExecuteState extends State<ModelExecute> {
  _ModelExecuteState({required this.modelKey}) : super();

  // TODO: add modelName attribute to identify model name
  final String modelKey;
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
                          child: ListView.separated(
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
                            },
                            separatorBuilder: (BuildContext context, int index) {
                              return const SizedBox(
                                height: 7,
                              );
                            },
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
                          child: ListView.separated(
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
                            },
                            separatorBuilder: (BuildContext context, int index) {
                              return const SizedBox(
                                height: 7,
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            Container(
              padding: const EdgeInsets.all(5.0),
              child: ElevatedButton(
                  onPressed: () async {
                    if (_formKey.currentState!.validate()) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text("Executing model...")),
                      );

                      // preparing inp/out attribute description to be sent to the executor
                      Map<String, List<dynamic>> inp = {};
                      Map<String, List<dynamic>> out = {};

                      // TODO: temp solution, we are assuming the only data type is the file-content
                      for(AttrDescriptor attr in modelInpAttrData) {
                        switch (attr.dtype) {
                          case AttributeDataType.fileContentInp: {
                            inp[attr.name] = ["file-content", attr.attrData, attr.fileName.split(".").last];
                          } break;
                          case AttributeDataType.fileContentOut: {
                            // none
                          } break;
                        }
                      }

                      for(AttrDescriptor attr in modelOutAttrData) {
                        switch (attr.dtype) {
                          case AttributeDataType.fileContentInp: {
                            // none
                          } break;
                          case AttributeDataType.fileContentOut: {
                            out[attr.name] = ["file-content", "", ""];
                          } break;
                        }
                      }

                      // execute the model and sets data to the output attributes

                      debugPrint("model key $modelKey");
                      await http.post(
                        Uri.parse('http://127.0.0.1:5000/predict_model/$modelKey'),
                        headers: {
                          "Access-Control-Allow-Origin": "*",
                          "Content-Type": "application/json",
                        },
                        body: json.encode({
                          "inp": inp,
                          "out": out,
                        }),
                      ).then((resp) {
                        print("EXEC SUCCESS");
                        switch(resp.statusCode) {
                          case 500: {
                            print("Model execution encountered error. Please check the server error log for further info.");
                            // TODO: maybe in the future, return the error from server to the flutter ui
                          } break;
                          case 200: {
                            print("Model successfully executed.");

                            Map<String, dynamic> data = json.decode(resp.body);

                            print("Body data: $data");

                            modelOutAttrData.asMap().forEach((ind, el) {
                              if(data.containsKey(el.name)) {
                                setState(() {
                                  if(modelOutAttrData[ind].dtype == AttributeDataType.fileContentOut) {
                                    modelOutAttrData[ind].fileName = "Content Updated";
                                    modelOutAttrData[ind].attrData = data[el.name][1];
                                    modelOutAttrData[ind].fileExt = data[el.name][2];
                                  }
                                });
                              }
                            });
                          } break;
                          default: {
                            print("Status code <${resp.statusCode}> not handled.");
                          } break;
                        }
                      }).onError((error, _stackTrace) {
                        print("EXEC ERROR: ${error}");
                      });
                    }
                  },
                  child: const Text("Execute")
              ),
            ),
            Container(
              padding: const EdgeInsets.all(5.0),
              child: ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: const Text("Find new model")
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
                await FilePickerCross.importFromStorage(
                  type: FileTypeCross.any
                ).then((file) {
                  debugPrint(file.fileName);
                  setState(() {
                    attrDescrp.fileName = file.fileName!;
                    attrDescrp.attrData = file.toString();
                  });
                });
              },
              child: const Text("Open File")
          ),
          const SizedBox(width: 20),
          Text(
            attrDescrp.fileName,
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
                // for attr file out, the attribute description would be already filled if the execution has finished
                //  by the time the user presses this button
                // TODO: maybe a mechanism to notify the user when this attribute gets updated

                if(attrDescrp.attrData != "" && attrDescrp.fileName != "") {
                  FilePickerCross(Uint8List.fromList(attrDescrp.attrData.codeUnits)).exportToStorage(
                    subject: "subject",
                    text: "text",
                    fileName: attrDescrp.name+(attrDescrp.fileExt ?? ".attribute"),
                  );
                }
              },
              child: const Text("Download File")
          ),
          const SizedBox(width: 20),
          Text(
            attrDescrp.fileName,
            style: const TextStyle(
              fontStyle: FontStyle.italic,
            ),
          )
        ],
      ),
    );
  }
}

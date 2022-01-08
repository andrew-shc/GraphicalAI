import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:end_user_app/model_execute.dart';


class ModelEntry extends StatefulWidget {
  const ModelEntry({Key? key}) : super(key: key);

  @override
  _ModelEntryState createState() => _ModelEntryState();
}

class _ModelEntryState extends State<ModelEntry> {
  final _formKey = GlobalKey<FormState>();
  String testMessage = "Empty Data";
  final mdlIdTxtController = TextEditingController();

  Future<http.Response> fetchExampleData() {
    return http.get(Uri.parse('http://127.0.0.1:5000/'));
  }

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    mdlIdTxtController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Model Entry"),
      ),
      body: Column(
        children: <Widget>[
          const Text(
            "Model Entries",
            style: TextStyle(
              fontSize: 32,
              color: Colors.black,
            ),
          ),
          Form(
            key: _formKey,
            child: Column(
              children: <Widget>[
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 200.0),
                  padding: const EdgeInsets.all(10.0),
                  child: TextFormField(
                    controller: mdlIdTxtController,
                    decoration: const InputDecoration(
                      hintText: "Model ID",
                    ),
                    validator: (String? value) {
                      if(value == null || value.isEmpty) {
                        return "Please enter some text";
                      }
                      return null;
                    },
                  )
                ),
                ElevatedButton(
                    onPressed: () async {
                      if (_formKey.currentState!.validate()) {
                        // loads the model and specify the required attributes for the next page

                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Processing input...")),
                        );

                        await http.get(
                            Uri.parse('http://127.0.0.1:5000/load_model/${mdlIdTxtController.text}'),
                            headers: {
                              "Access-Control-Allow-Origin": "*"
                            }
                        ).then((resp) {
                          print("NO ERROR!");
                          print(resp.statusCode);
                          switch(resp.statusCode) {
                            case 404: {
                              print("ERROR: Model Key <${mdlIdTxtController.text}> not found.");
                            } break;
                            case 200: {
                              Map<String, dynamic> data = jsonDecode(resp.body);

                              debugPrint(resp.body);

                              ModelExecute modelExec = ModelExecute(
                                modelKey: mdlIdTxtController.text,
                              );

                              data["req-inp"].forEach((key, value) {
                                if(value == "file") {  // TODO: should techn. be file-content
                                  modelExec.state.addAttr(key, AttributeLocation.input, AttributeDataType.fileContentInp);
                                }
                              });
                              data["req-out"].forEach((key, value) {
                                if(value == "file") {  // TODO: should techn. be file-content
                                  modelExec.state.addAttr(key, AttributeLocation.output, AttributeDataType.fileContentOut);
                                }
                              });

                              Navigator.push(
                                  context,
                                  MaterialPageRoute(builder: (context) => modelExec)
                              );
                            } break;
                            default: {
                              print("Status code <${resp.statusCode}> not handled.");
                            } break;
                          }
                        }).onError((error, _stackTrace) {
                          print("ERROR: ${error}");
                        });
                      }
                    },
                    child: const Text("Submit"),
                ),
              ]
            ),
          ),
        ],
      ),
    );
  }
}

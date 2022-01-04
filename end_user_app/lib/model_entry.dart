import 'package:end_user_app/model_execute.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;


class ModelEntry extends StatefulWidget {
  const ModelEntry({Key? key}) : super(key: key);

  @override
  _ModelEntryState createState() => _ModelEntryState();
}

class _ModelEntryState extends State<ModelEntry> {
  final _formKey = GlobalKey<FormState>();
  String testMessage = "Empty Data";

  Future<http.Response> fetchExampleData() {
    return http.get(Uri.parse('http://127.0.0.1:5000/'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Model Entry"),
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
                    decoration: InputDecoration(
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
                    onPressed: () {
                      if (_formKey.currentState!.validate()) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Processing input...")),
                        );

                        ModelExecute modelExec = ModelExecute();
                        modelExec.state.addAttr("Input Attr", AttributeLocation.input, AttributeDataType.fileContentInp);
                        modelExec.state.addAttr("Output Attr", AttributeLocation.output, AttributeDataType.fileContentOut);

                        Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => modelExec)
                        );
                      }
                    },
                    child: Text("Submit"),
                ),
                Text(
                  "$testMessage"
                ),
                ElevatedButton(
                  onPressed: () async {
                    http.Response resp = await http.get(
                        Uri.parse('http://127.0.0.1:5000/'),
                        headers: {
                          "Access-Control-Allow-Origin": "*"
                        }
                    );

                    setState(() {
                      testMessage = resp.body;
                    });
                    print(testMessage);
                  },
                  child: Text("Submit"),
                ),
              ]
            ),
          ),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';


class ModelExecute extends StatefulWidget {
  const ModelExecute({Key? key}) : super(key: key);

  @override
  _ModelExecuteState createState() => _ModelExecuteState();
}

class _ModelExecuteState extends State<ModelExecute> {
  final _formKey = GlobalKey<FormState>();

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
            IntrinsicHeight(
              child: Row(
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
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: "Dataset <file>",
                              floatingLabelBehavior: FloatingLabelBehavior.always,
                            ),
                            validator: (String? value) {
                              if(value == null || value.isEmpty) {
                                return "Please enter some text";
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  Container(
                    width: 20,
                    child: VerticalDivider(
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
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: "Results <file>",
                              floatingLabelBehavior: FloatingLabelBehavior.always,
                            ),
                            validator: (String? value) {
                              if(value == null || value.isEmpty) {
                                return "Please enter some text";
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text("Executing model...")),
                    );
                    Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const ModelExecute())
                    );
                  }
                },
                child: Text("Execute")
            ),
            ElevatedButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text("Find new model")
            ),
          ],
        ),
      ),
    );
  }
}

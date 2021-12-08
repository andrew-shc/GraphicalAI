import 'package:end_user_app/model_execute.dart';
import 'package:flutter/material.dart';


class ModelEntry extends StatefulWidget {
  const ModelEntry({Key? key}) : super(key: key);

  @override
  _ModelEntryState createState() => _ModelEntryState();
}

class _ModelEntryState extends State<ModelEntry> {
  final _formKey = GlobalKey<FormState>();

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
                TextFormField(
                  decoration: InputDecoration(
                    hintText: "Model ID",
                  ),
                  validator: (String? value) {
                    if(value == null || value.isEmpty) {
                      return "Please enter some text";
                    }
                    return null;
                  },
                ),
                ElevatedButton(
                    onPressed: () {
                      if (_formKey.currentState!.validate()) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Processing input...")),
                        );
                        Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => const ModelExecute())
                        );
                      }
                    },
                    child: Text("Submit"),
                )
              ]
            ),
          ),
        ],
      ),
    );
  }
}

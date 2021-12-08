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
            Row(
              children: <Widget>[
                Expanded(
                  child: Column(
                    children: <Widget>[
                      const Text("Input attributes and fields"),
                      TextFormField(
                        decoration: const InputDecoration(
                          hintText: "Input Field (Could be text, file, or other source of input)",
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
                Expanded(
                  child: Column(
                    children: <Widget>[
                      const Text("Output locations and fields"),
                      TextFormField(
                        decoration: const InputDecoration(
                          hintText: "Output Field (Could be file location, console output, or other collector of output)",
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
              ],
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

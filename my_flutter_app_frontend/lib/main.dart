import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

// Main App
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Comments App',
      home: Scaffold(
        appBar: AppBar(title: Text('My Flutter Web Page')),
        body: SingleChildScrollView(
          child: Column(
            children: [
              // HTML content with viewport
              Html(
                data: """
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <h1>Welcome to My Web Page</h1>
                  <p>This is responsive across all screen sizes.</p>
                """,
              ),
              SizedBox(height: 20),
              // Comment Section
              CommentSection(),
            ],
          ),
        ),
      ),
    );
  }
}

// Comment Section Widget
class CommentSection extends StatefulWidget {
  const CommentSection({super.key});

  @override
  _CommentSectionState createState() => _CommentSectionState();
}

class _CommentSectionState extends State<CommentSection> {
  final _controller = TextEditingController();
  List<String> comments = [];

  @override
  void initState() {
    super.initState();
    fetchComments();
  }

  // To fetch comments from the backend
  void fetchComments() async {
    try {
      final response = await http.get(Uri.parse('http://localhost:8000/comments'));
      if (response.statusCode == 200) {
        setState(() {
          comments = List<String>.from(jsonDecode(response.body).map((c) => c['text']));
        });
      } 
    } catch (e) {
      print('Error fetching comments: $e');
    }
  }

  // Posting comments to backend
  void postComment() async {
    if (_controller.text.isEmpty) return;

    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/comments'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"text": _controller.text}),
      );
      if (response.statusCode == 200) {
        fetchComments();
        _controller.clear();
      }
    } catch (e) {
      print('Error posting comment: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          TextField(
            controller: _controller,
            decoration: InputDecoration( 
              labelText: 'Write a comment',
              border: OutlineInputBorder(),
            ),
          ),
          SizedBox(height: 10),
          ElevatedButton(onPressed: postComment, child: Text('Post')),
          SizedBox(height: 20),
          ...comments.map((c) => ListTile(title: Text(c))),
        ],
      ),
    );
  }
}
 
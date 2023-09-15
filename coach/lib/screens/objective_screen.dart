import 'package:coach/components/themed_button.dart';
import 'package:coach/screens/overview_screen.dart';
import 'package:flutter/material.dart';

class ObjectiveScreen extends StatefulWidget {
  const ObjectiveScreen({super.key});

  @override
  State<ObjectiveScreen> createState() => _ObjectiveScreenState();
}

class _ObjectiveScreenState extends State<ObjectiveScreen> {
  void _navigateToOverview() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const OverviewScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('Your Objective'),
            ThemedButton(title: 'Continue', onPressed: _navigateToOverview),
          ],
        ),
      ),
    );
  }
}

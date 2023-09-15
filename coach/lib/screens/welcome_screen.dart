import 'package:coach/components/themed_button.dart';
import 'package:coach/screens/objective_screen.dart';
import 'package:flutter/material.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key, required this.title});

  final String title;

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {
  void _navigateToObjective() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const ObjectiveScreen()),
    );
  }

  void _authCalendar() {}

  void _authWhoop() {}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 32.0),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              ThemedButton(
                  title: 'Authenticate Google Calendar',
                  onPressed: _authCalendar),
              const SizedBox(height: 16),
              ThemedButton(title: 'Authenticate WHOOP', onPressed: _authWhoop),
              const SizedBox(height: 128),
              ThemedButton(title: 'Continue', onPressed: _navigateToObjective),
            ],
          ),
        ),
      ),
    );
  }
}

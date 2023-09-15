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
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                ),
                onPressed: _authCalendar,
                child: const Text("Authenticate Google Calendar"),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                ),
                onPressed: _authWhoop,
                child: const Text("Authenticate WHOOP"),
              ),
              const SizedBox(height: 128),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                ),
                onPressed: _navigateToObjective,
                child: const Text("Continue"),
              )
            ],
          ),
        ),
      ),
    );
  }
}

import 'package:coach/api/service.dart';
import 'package:coach/api/whoop_client.dart';
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
  bool _isWhoopAuthenticated = false;
  String? _whoopToken;
  bool _sentTokens = false;

  void _navigateToObjective() {
    if (!_sentTokens) {
      sendTokens(whoop: _whoopToken);
      _sentTokens = true;
    }

    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const ObjectiveScreen()),
    );
  }

  void _authCalendar() {}

  void _authWhoop() async {
    var client = WhoopClient(customUriScheme: '');
    var response = await client.getTokenWithAuthCodeFlow(
        clientId: '4a0e2745-5588-4c17-a109-ffdca04a1f98',
        clientSecret:
            '4b325183d2c2bb3bb0dddf7834289c458a915445efacb3bffa748d0dee6409b6',
        scopes: [
          'offline',
          'read:recovery',
          'read:cycles',
          'read:sleep',
          'read:workout',
          'read:profile',
          'read:body_measurement',
        ]);
    if (response.isValid()) {
      print(response.accessToken);
      setState(() {
        _isWhoopAuthenticated = true;
        _whoopToken = response.accessToken;
      });
    }
  }

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
              ThemedButton(
                title: _isWhoopAuthenticated
                    ? 'Authenticated WHOOP'
                    : 'Authenticate WHOOP',
                onPressed: _authWhoop,
                isSuccess: _isWhoopAuthenticated,
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _navigateToObjective,
        label: const Text('Go to Objective'),
        extendedPadding: const EdgeInsets.symmetric(horizontal: 64),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

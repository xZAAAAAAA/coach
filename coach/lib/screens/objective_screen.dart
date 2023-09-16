import 'package:coach/components/sports_entry.dart';
import 'package:coach/components/target_dropdown.dart';
import 'package:coach/components/themed_button.dart';
import 'package:coach/screens/overview_screen.dart';
import 'package:flutter/material.dart';

class ObjectiveScreen extends StatefulWidget {
  const ObjectiveScreen({super.key});

  @override
  State<ObjectiveScreen> createState() => _ObjectiveScreenState();
}

class _ObjectiveScreenState extends State<ObjectiveScreen> {
  final _selectedSports = List<String?>.of([null]);
  String? _objective;

  void _navigateToOverview() {
    // Backend call to propagate initial preferences.

    // Navigator.pushReplacement(
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const OverviewScreen()),
    );
  }

  void _addSportEntry() {
    setState(() {
      _selectedSports.add(null);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Objective')),
      body: Padding(
        padding: const EdgeInsets.only(left: 32, right: 32, top: 128),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Text('SPORTS',
                  style: Theme.of(context)
                      .textTheme
                      .labelLarge!
                      .copyWith(fontWeight: FontWeight.bold)),
            ),
            for (final (index, sport) in _selectedSports.indexed)
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: SportsEntry(
                    hint: sport == null ? 'Select sport' : null,
                    value: sport,
                    onChange: (value) {
                      _selectedSports[index] = sport;
                    }),
              ),
            ThemedButton(title: 'Add sport', onPressed: _addSportEntry),
            const SizedBox(height: 32),
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Text('OBJECTIVE',
                  style: Theme.of(context)
                      .textTheme
                      .labelLarge!
                      .copyWith(fontWeight: FontWeight.bold)),
            ),
            TargetDropdown(onChange: (e) => {_objective = e})
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _navigateToOverview,
        label: const Text('Continue'),
        extendedPadding: const EdgeInsets.symmetric(horizontal: 128),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

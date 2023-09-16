import 'dart:async';

import 'package:coach/api/service.dart';
import 'package:coach/components/workout.dart';
import 'package:flutter/material.dart';
import 'package:rxdart/subjects.dart';

class OverviewScreen extends StatefulWidget {
  const OverviewScreen({super.key});

  @override
  State<OverviewScreen> createState() => _OverviewScreenState();
}

class _OverviewScreenState extends State<OverviewScreen> {
  TrainingState? _previousState;
  bool _showSpinner = false;

  final BehaviorSubject<bool> _showSpinnerSubject =
      BehaviorSubject<bool>.seeded(false);
  late StreamSubscription<bool> showSpinnerSubscription;

  @override
  void initState() {
    showSpinnerSubscription =
        _showSpinnerSubject.stream.listen(_showSpinnerChanged);
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
    showSpinnerSubscription.cancel();
  }

  void _showSpinnerChanged(bool value) {
    setState(() {
      _showSpinner = value;
    });
  }

  Widget _buildSummary(TrainingState state) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text(
                  'SUMMARY',
                  style: Theme.of(context)
                      .textTheme
                      .labelLarge!
                      .copyWith(fontWeight: FontWeight.bold),
                ),
              ),
              Text(
                state.summary,
                maxLines: 10,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNextSteps(TrainingState state) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text(
                  'NEXT UP',
                  style: Theme.of(context)
                      .textTheme
                      .labelLarge!
                      .copyWith(fontWeight: FontWeight.bold),
                ),
              ),
              Text(
                state.explanation,
                maxLines: 10,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              ...state.workouts
                  .map((w) => Workout(
                        title: w.title,
                        description: w.summary,
                        sportsType: w.sportsType,
                        date: w.date,
                        duration: w.duration,
                        intensity: w.intensity,
                      ))
                  .toList()
            ],
          ),
        ),
      ),
    );
  }

  void _openAdaptBottomSheet() {
    showModalBottomSheet<void>(
        context: context,
        builder: (BuildContext context) {
          return Container(
            padding: const EdgeInsets.all(32),
            height: 250,
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Text('ADAPT',
                        style: Theme.of(context)
                            .textTheme
                            .labelLarge!
                            .copyWith(fontWeight: FontWeight.bold)),
                  ),
                  const Text(
                      'Tell us how you would like to adapt your training plan. For example: "I have a date tonight" or "I want a harder next session."'),
                  const SizedBox(height: 16),
                  TextField(
                    onSubmitted: (text) {
                      _showSpinnerSubject.add(true);
                      sendAdapt(text);
                      Navigator.pop(context);
                    },
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'What\'s happening?',
                    ),
                  ),
                ],
              ),
            ),
          );
        });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Overview'), actions: [
        if (_showSpinner)
          const Padding(
            padding: EdgeInsets.only(right: 16),
            child: SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
              ),
            ),
          )
      ]),
      body: Center(
        child: StreamBuilder(
          stream: Stream.periodic(const Duration(seconds: 5))
              .asyncMap((i) => fetchState()),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              if (_previousState == null ||
                  snapshot.data!.summary != _previousState!.summary) {
                _showSpinnerSubject.add(false);
                _previousState = snapshot.data!;
              }

              return ListView(
                children: <Widget>[
                  _buildSummary(snapshot.data!),
                  _buildNextSteps(snapshot.data!),
                  const SizedBox(height: 80),
                ],
              );
            } else {
              return const CircularProgressIndicator();
            }
          },
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _openAdaptBottomSheet,
        label: const Text('Adapt'),
        extendedPadding: const EdgeInsets.symmetric(horizontal: 64),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

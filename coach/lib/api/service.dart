import 'dart:convert';

import 'package:http/http.dart' as http;

const String kEndpoint = "https://c503-85-214-57-62.ngrok-free.app";

class WorkoutState {
  final String title;
  final String summary;
  final String date;
  final int duration;
  final String intensity;
  final String sportsType;

  const WorkoutState({
    required this.title,
    required this.summary,
    required this.date,
    required this.duration,
    required this.intensity,
    required this.sportsType,
  });

  factory WorkoutState.fromJson(Map<String, dynamic> json) {
    return WorkoutState(
      title: json['title'],
      summary: json['summary'],
      date: json['date'],
      duration: json['duration'],
      intensity: json['intensity'],
      sportsType: json['sport_type'],
    );
  }
}

class TrainingState {
  final String summary;
  final String explanation;
  final List<WorkoutState> workouts;

  const TrainingState({
    required this.summary,
    required this.explanation,
    required this.workouts,
  });

  factory TrainingState.fromJson(Map<String, dynamic> json) {
    return TrainingState(
      summary: json['summary'],
      explanation: json['explanation'],
      workouts: (json['workouts'] as List)
          .map((e) => WorkoutState.fromJson(e))
          .toList(),
    );
  }
}

Future<void> sendTokens({String? whoop, String? calendar}) async {
  if (whoop == null && calendar == null) {
    return;
  }

  final uri = Uri.parse('$kEndpoint/tokens');

  Map<String, String> data = {};

  if (whoop != null) {
    data.putIfAbsent('whoop', () => whoop);
  }

  if (calendar != null) {
    data.putIfAbsent('calendar', () => calendar);
  }

  http.post(
    uri,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(data),
  );
}

Future<void> sendSetup(List<String> sports, String objective) {
  final uri = Uri.parse('$kEndpoint/setup');

  return http.post(
    uri,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body:
        jsonEncode(<String, Object>{'sports': sports, 'objective': objective}),
  );
}

Future<void> sendAdapt(String text) {
  final uri = Uri.parse('$kEndpoint/adapt');

  return http.post(
    uri,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, Object>{'text': text}),
  );
}

Future<TrainingState> fetchState() async {
  final uri = Uri.parse('$kEndpoint/state');

  final result = await http.get(uri);
  print(result.body);

  return TrainingState.fromJson(jsonDecode(result.body));
}

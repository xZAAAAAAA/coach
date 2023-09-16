import 'dart:convert';

import 'package:http/http.dart' as http;

const String kEndpoint = "https://c503-85-214-57-62.ngrok-free.app";

class UserState {
  final int age;
  final double weightKg;
  final double heightCm;
  final double avgSleepScore;
  final double avgRecoveryScore;
  final double lastSleepScore;
  final double lastRecoveryScore;
  final String trainingObjective;

  const UserState({
    required this.age,
    required this.weightKg,
    required this.heightCm,
    required this.avgSleepScore,
    required this.avgRecoveryScore,
    required this.lastSleepScore,
    required this.lastRecoveryScore,
    required this.trainingObjective,
  });

  factory UserState.fromJson(Map<String, dynamic> json) {
    return UserState(
      age: json['age'],
      weightKg: json['weight'],
      heightCm: json['height'] * 100,
      avgSleepScore: json['avg_sleep_score'],
      avgRecoveryScore: json['avg_recovery_score'],
      lastSleepScore: json['last_sleep_score'],
      lastRecoveryScore: json['last_recovery_score'],
      trainingObjective: json['training_objective'],
    );
  }
}

class WorkoutState {
  final String title;
  final String summary;
  final String startTime;
  final String date;
  final int duration;
  final String intensity;
  final String sportsType;

  const WorkoutState({
    required this.title,
    required this.summary,
    required this.startTime,
    required this.date,
    required this.duration,
    required this.intensity,
    required this.sportsType,
  });

  factory WorkoutState.fromJson(Map<String, dynamic> json) {
    return WorkoutState(
      title: json['title'],
      summary: json['summary'],
      startTime: json['start_time'],
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
  final String? changeReason;
  final List<WorkoutState> workouts;
  final UserState user;

  const TrainingState({
    required this.summary,
    required this.explanation,
    required this.changeReason,
    required this.workouts,
    required this.user,
  });

  factory TrainingState.fromJson(Map<String, dynamic> json) {
    return TrainingState(
      summary: json['summary'],
      explanation: json['explanation'],
      changeReason:
          json.containsKey('change_reason') ? json["change_reason"] : null,
      workouts: (json['workouts'] as List)
          .map((e) => WorkoutState.fromJson(e))
          .toList(),
      user: json.containsKey('user')
          ? UserState.fromJson(json['user'])
          : const UserState(
              age: 30,
              weightKg: 70,
              heightCm: 180,
              avgSleepScore: 92,
              avgRecoveryScore: 56,
              lastSleepScore: 67,
              lastRecoveryScore: 91,
              trainingObjective: 'Maintain fitness',
            ),
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

Future<void> sendSetup(List<String?> sports, String? objective) {
  final uri = Uri.parse('$kEndpoint/setup');

  final data = {};

  if (objective != null) {
    data.putIfAbsent('objective', () => objective);
  }

  final sportsFiltered = sports.where((element) => element != null).toList();
  if (sportsFiltered.isNotEmpty) {
    data.putIfAbsent('sports', () => sportsFiltered);
  }

  return http.post(
    uri,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(data),
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

Future<TrainingState?> fetchState() async {
  final uri = Uri.parse('$kEndpoint/state');

  final result = await http.get(uri);
  print(result.body);

  final content = jsonDecode(result.body) as Map;

  if (content.isEmpty) {
    return null;
  }

  return TrainingState.fromJson(content as dynamic);
}

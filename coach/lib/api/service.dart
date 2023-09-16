import 'dart:convert';

import 'package:http/http.dart' as http;

const String kEndpoint = "https://bf8f-85-214-57-62.ngrok-free.app";

class TrainingState {
  final String summary;
  final String nextSteps;

  const TrainingState({required this.summary, required this.nextSteps});

  factory TrainingState.fromJson(Map<String, dynamic> json) {
    return TrainingState(
      summary: json['summary'],
      nextSteps: json['next_steps'],
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

Future<http.Response> fetchState(List<String> sports, String objective) {
  final uri = Uri.parse('$kEndpoint/state');

  return http.get(uri);
}

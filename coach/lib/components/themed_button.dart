import 'package:flutter/material.dart';

class ThemedButton extends StatelessWidget {
  const ThemedButton({
    super.key,
    required this.title,
    required this.onPressed,
    this.isSuccess = false,
  });

  final String title;

  final bool isSuccess;

  final void Function() onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
          minimumSize: const Size.fromHeight(50),
          backgroundColor: isSuccess ? Colors.greenAccent.withAlpha(30) : null,
          foregroundColor:
              isSuccess ? Colors.greenAccent.withAlpha(200) : null),
      onPressed: onPressed,
      child: Text(title),
    );
  }
}

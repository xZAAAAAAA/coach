import 'package:flutter/material.dart';

class ThemedButton extends StatelessWidget {
  const ThemedButton({super.key, required this.title, required this.onPressed});

  final String title;

  final void Function() onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size.fromHeight(50),
      ),
      onPressed: onPressed,
      child: Text(title),
    );
  }
}

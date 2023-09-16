import 'package:flutter/material.dart';

class ThemedChip extends StatelessWidget {
  const ThemedChip(
      {super.key, required this.label, this.color, this.isSport = false});

  final String label;
  final bool isSport;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 2, horizontal: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(2),
        color: color?.withAlpha(60) ?? Colors.blueAccent.withAlpha(30),
      ),
      child: Row(
        children: [
          Text(label,
              style: Theme.of(context).textTheme.labelMedium!.copyWith(
                  color: color?.withAlpha(250) ?? Colors.blueGrey.shade100)),
        ],
      ),
    );
  }
}

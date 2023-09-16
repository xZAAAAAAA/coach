import 'package:flutter/material.dart';

class ThemedChip extends StatelessWidget {
  const ThemedChip({super.key, required this.label, this.color});

  final String label;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 2, horizontal: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(2),
        color: color ?? Colors.blueGrey.shade200,
      ),
      child: Row(
        children: [
          Text(label,
              style: Theme.of(context)
                  .textTheme
                  .labelMedium!
                  .copyWith(color: Colors.blueGrey.shade900)),
        ],
      ),
    );
  }
}

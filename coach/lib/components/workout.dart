import 'package:coach/components/chip.dart';
import 'package:flutter/material.dart';

class Workout extends StatefulWidget {
  const Workout({
    super.key,
    required this.title,
    required this.description,
    required this.sportsType,
    required this.date,
    required this.duration,
    required this.intensity,
  });

  final String title;
  final String description;
  final String sportsType;

  final String date;
  final int duration;
  final String intensity;

  @override
  State<Workout> createState() => _WorkoutState();
}

class _WorkoutState extends State<Workout> {
  Color? textToColor(String text) {
    if (text == 'high') {
      return Colors.redAccent;
    } else if (text == 'medium') {
      return Colors.orangeAccent;
    } else if (text == 'low') {
      return Colors.greenAccent;
    } else {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.greenAccent.withAlpha(40),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
      child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Flexible(
                    child: Text(widget.title,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: Theme.of(context).textTheme.titleSmall!),
                  ),
                  Row(children: [
                    ThemedChip(
                      label: widget.sportsType.toUpperCase(),
                      color: Colors.cyanAccent,
                    ),
                  ]),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                widget.description,
                maxLines: 5,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.bodySmall,
              ),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      ThemedChip(label: widget.date),
                      const SizedBox(width: 4),
                      ThemedChip(label: '${widget.duration} min'),
                    ],
                  ),
                  ThemedChip(
                    label: widget.intensity.toUpperCase(),
                    color: textToColor(widget.intensity),
                  ),
                ],
              )
            ],
          )),
    );
  }
}

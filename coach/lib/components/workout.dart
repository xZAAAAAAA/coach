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
      return Colors.redAccent.shade200;
    } else if (text == 'medium') {
      return Colors.orangeAccent.shade200;
    } else if (text == 'low') {
      return Colors.blueGrey.shade200;
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
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
                    decoration: BoxDecoration(
                      color: Colors.greenAccent.withAlpha(60),
                      borderRadius: BorderRadius.circular(2),
                    ),
                    child: Text(
                      widget.sportsType.toUpperCase(),
                      style: Theme.of(context).textTheme.labelSmall!.copyWith(
                          color: Colors.greenAccent.shade200,
                          fontWeight: FontWeight.w600),
                    ),
                  )
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
                children: [
                  ThemedChip(label: widget.date),
                  const SizedBox(width: 4),
                  ThemedChip(label: '${widget.duration} min'),
                  const SizedBox(width: 4),
                  ThemedChip(
                    label: widget.intensity,
                    color: textToColor(widget.intensity),
                  ),
                ],
              )
            ],
          )),
    );
  }
}

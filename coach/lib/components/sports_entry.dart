import 'package:flutter/material.dart';

const List<String> entries = <String>['Cycling', 'Running'];

class SportsEntry extends StatefulWidget {
  const SportsEntry({super.key});

  @override
  State<SportsEntry> createState() => _SportsEntryState();
}

class _SportsEntryState extends State<SportsEntry> {
  String dropdownValue = entries.first;

  @override
  Widget build(BuildContext context) {
    return DropdownMenu<String>(
      inputDecorationTheme: InputDecorationTheme(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16),
        fillColor: Theme.of(context).colorScheme.primary,
        focusColor: Theme.of(context).colorScheme.inverseSurface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(64),
          borderSide: BorderSide(color: Theme.of(context).disabledColor),
        ),
      ),
      initialSelection: entries.first,
      onSelected: (String? value) {
        // This is called when the user selects an item.
        setState(() {
          dropdownValue = value!;
        });
      },
      dropdownMenuEntries:
          entries.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}

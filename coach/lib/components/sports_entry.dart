import 'package:flutter/material.dart';

// const List<String> entries = <String>['Cycling', 'Running', 'Swimming'];

List<String> getEntries() {
  final entries = [
    'Cycling',
    'Running',
    'Swimming',
    'Squash',
    'Tennis',
    'Badminton',
    'Rowing',
  ];
  entries.sort();
  return entries;
}

class SportsEntry extends StatefulWidget {
  const SportsEntry({super.key, required this.onChange, this.hint, this.value});

  final String? hint;
  final String? value;
  final void Function(String) onChange;

  @override
  State<SportsEntry> createState() => _SportsEntryState();
}

class _SportsEntryState extends State<SportsEntry> {
  final TextEditingController controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return DropdownMenu<String>(
      width: MediaQuery.of(context).size.width - 64,
      inputDecorationTheme: InputDecorationTheme(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16),
        fillColor: Theme.of(context).colorScheme.inversePrimary,
        focusColor: Theme.of(context).colorScheme.inverseSurface,
        filled: true,
        activeIndicatorBorder: BorderSide.none,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(64),
          borderSide: BorderSide.none,
        ),
      ),
      initialSelection: widget.value,
      onSelected: (String? value) {
        widget.onChange(value!);
      },
      hintText: widget.hint,
      dropdownMenuEntries:
          getEntries().map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}

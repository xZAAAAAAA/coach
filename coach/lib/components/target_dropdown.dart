import 'package:flutter/material.dart';

const List<String> entries = <String>[
  'Increase fitness',
  'Maintain fitness',
  'Lose weight'
];

class TargetDropdown extends StatefulWidget {
  const TargetDropdown({super.key, required this.onChange});

  final void Function(String) onChange;

  @override
  State<TargetDropdown> createState() => _TargetDropdownState();
}

class _TargetDropdownState extends State<TargetDropdown> {
  // String? _currentValue;

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
      onSelected: (String? value) {
        widget.onChange(value!);
        // setState(() {
        //   _currentValue = value;
        // });
      },
      hintText: 'Select objective',
      dropdownMenuEntries:
          entries.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}

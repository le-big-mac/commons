# The arithmetic of the three sheets' scores. The verdicts are typed in from dawn.out, dawn2025.out and stars_sheet.out
# (1 held, 0 failed, None void); the odds are those of the sheets.
sheets = {
 'first sheet, 2024 (L1 to L8), as the program ran': [(.85, 1), (.70, 1), (.65, 1), (.50, 0), (.55, 1), (.70, 1), (.60, 1), (.65, 1)],
 'second sheet, 2025 (R1 to R10), as the program ran': [(.85, 0), (.85, 1), (.80, 1), (.70, 1), (.60, 1), (.70, 1), (.65, None), (.75, 1), (.80, 1), (.75, 1)],
 'second sheet with R5 counted as failed (it holds by one night and fails under the checker\'s other clear sets)': [(.85, 0), (.85, 1), (.80, 1), (.70, 1), (.60, 0), (.70, 1), (.65, None), (.75, 1), (.80, 1), (.75, 1)],
 'third sheet, 2022 and 2023 (S1 to S13), as the program ran': [(.65, 1), (.75, 1), (.55, 0), (.75, 1), (.65, 1), (.70, 1), (.75, 1), (.80, 1), (.80, 1), (.70, 1), (.85, 1), (.70, None), (.85, 1)],
}
for name, L in sheets.items():
    S = [(p, o) for p, o in L if o is not None]
    print(f'{name}: {sum(o for p, o in S)} held of {len(S)} scored ({len(L) - len(S)} void); the odds add up to {sum(p for p, o in S):.1f}; score {sum((p - o) ** 2 for p, o in S) / len(S):.2f} (0.25 is what saying 50 in 100 to everything scores; lower is better)')

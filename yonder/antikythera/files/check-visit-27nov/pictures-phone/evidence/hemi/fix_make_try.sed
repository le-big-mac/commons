s|fontsize=8.5, colors=INK, inline_spacing=2, manual={spots!r})\\n")|fontsize=8.5, colors={COLS}, inline_spacing=2, manual={spots!r})\\n")|
s|^spots = \(.*\)$|spots = \1\nCOLS = '[SURF, SURF, INK]' if len(sys.argv) > 3 and sys.argv[3] == 'pale' else 'INK'      # pale: the numbers of the two innermost lines in the paper's colour, since they stand on the darkest blues|

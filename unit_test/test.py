import blessed

term = blessed.Terminal()

with term.fullscreen(), term.cbreak():
    print(term.move_y(term.height // 2) + term.center("press any key").rstrip())
    while True:
        b = term.inkey()
        term.move_xy(term.width // 2, 19)
        # term.clear_bol()
        print(print(term.on_green(f"This will not standout on a vt220")))

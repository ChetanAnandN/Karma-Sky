"""Safety shield: 30 s worst-case look-ahead, 100 m drone / 500 m helicopter separation, fallback slow down.

Priority order: manned aircraft > shield > credits > policy. Output: allowed[drone_id] = [bool, bool, bool].

Owner: Member 4 (evaluation, safety, attacks).
TODO: Implement with hand-made unit tests; log intervention rate.
Status: placeholder, no implementation yet.
"""

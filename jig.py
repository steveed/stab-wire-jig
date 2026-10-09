"""Stabiliser-wire bending jig: an aluminium bar, a sliding carriage for a Du-Bro E/Z Bender, and a
fixed block that holds the wire.

    docker compose run --rm cad python jig.py      (make)

Writes build/: a STEP file for each part and the assembly, and SVG views.

Coordinates: x along the bar (the wire's direction), y across it (-y towards you), z up; the bar's
top face is z = BAR_H.  The fixed block is on the right, the bender slides on the left (the bender
only bends clockwise, so the wire is turned over between its two bends; see README.md).
"""

import os

import cadquery as cq

OUT = 'build'

# --- the bender (Du-Bro E/Z Bender, SKU 481), measured
BENDER_HOLES = 101.14      # mounting hole centres, along its long axis; the pivot is midway
BENDER_LEN = 115.58        # overall length
BENDER_W = 41.21           # width at the middle
BENDER_SLOT = 41.15        # base bottom to the bottom of the wire slot between its pins
BENDER_TAP = 'M4'          # thread for its mounting screws (assumed: check the bender's holes)
TAP_DRILL = {'M4': 3.3, 'M5': 4.2, 'M6': 5.0}
PIN = 7.8                  # the centre pin the wire wraps round
WIRE = 1.5                 # 304 stainless rod
BEND_OFFSET = PIN / 2 + WIRE / 2   # a bent leg's centreline sits this far from the pivot

# --- spans between leg centres, Cherry-style stabilisers (README)
SPANS = {'6.25U': 100.0, '7U': 114.3, '8U': 133.35, '9U': 152.4}

# --- bar
BAR_L, BAR_W, BAR_H = 300.0, 40.0, 15.0
SLOT_THROAT, SLOT_THROAT_D = 6.5, 5.0      # T-slot for M6 T-nuts: throat at the top...
SLOT_UNDER, SLOT_UNDER_D = 11.0, 5.0       # ...and the wider undercut below it
SLOT_END = 230.0                           # the slot runs from the left end to here
# bench tabs: the bar runs on past each end, milled down to the T-slot's floor so T-nuts still slide
# in from the left, with a slotted hole for a screw or bolt into the bench
TAB_L = 25.0
TAB_T = BAR_H - SLOT_THROAT_D - SLOT_UNDER_D
TAB_SLOT = (12.0, 6.5)                     # slotted hole, along the bar

# --- carriage (the bender bolts to it; it slides in the T-slot and locks with two thumb screws)
CAR_X, CAR_Y, CAR_T = 76.0, 130.0, 8.0
CAR_CLAMP_X = 30.0                         # thumb screws at x = +-30 from the pivot, clear of the bender
TONGUE_W, TONGUE_D = 6.3, 3.0              # rides in the slot's throat, keeps the carriage square

# --- fixed block (holds the wire: a straight groove and a cross slot for the bent leg, and a clamp)
BLOCK_X0, BLOCK_X1 = 255.0, 285.0
LEG_X = 270.0                              # the cross slot's centre: the scale's zero
GROOVE_D = 1.2                             # wire stands 0.3 proud, so the clamp washer grips it
GROOVE_W = 1.6
LEG_SLOT_W = 1.8                           # a little room for the already-bent leg
CLAMP = (6.0, -6.0)                        # M5 clamp screw, from the groove/slot junction; fender washer
FLOOR_Z = BAR_H + CAR_T + BENDER_SLOT      # wire's underside, the same height as in the bender
BLOCK_TOP = FLOOR_Z + GROOVE_D
BLOCK_SCREWS = [(BLOCK_X0 + 7.5, 12.0), (BLOCK_X1 - 7.5, -12.0)]   # M5, from under the bar

# --- scale: read at the carriage's left edge
SCALE_Y = (4.0, 19.0)                      # the strip of bar top between the slot and the back edge
ENGRAVE = 0.3


def drill(x, y, z0, z1, d):
    """A plain cylinder from z0 up to z1, to cut a hole."""
    return cq.Workplane('XY').workplane(offset=z0).center(x, y).circle(d / 2).extrude(z1 - z0)


def pivot_for(span):
    """Pivot x for a span between leg centres (the second leg forms BEND_OFFSET right of the pivot)."""
    return LEG_X - span - BEND_OFFSET


def bar():
    b = cq.Workplane('XY').box(BAR_L, BAR_W, BAR_H, centered=(False, True, False))
    for x0 in (-TAB_L, BAR_L):                                  # bench tabs at both ends
        tab = cq.Workplane('XY').box(TAB_L, BAR_W, TAB_T, centered=(False, True, False)).translate((x0, 0, 0))
        hole = (cq.Workplane('XY').center(x0 + TAB_L / 2, 0).slot2D(TAB_SLOT[0], TAB_SLOT[1])
                .extrude(TAB_T + 2).translate((0, 0, -1)))
        b = b.union(tab.cut(hole))
    throat = (cq.Workplane('XY').workplane(offset=BAR_H - SLOT_THROAT_D)
              .center(SLOT_END / 2, 0).rect(SLOT_END, SLOT_THROAT).extrude(SLOT_THROAT_D + 1))
    under = (cq.Workplane('XY').workplane(offset=BAR_H - SLOT_THROAT_D - SLOT_UNDER_D)
             .center(SLOT_END / 2, 0).rect(SLOT_END, SLOT_UNDER).extrude(SLOT_UNDER_D))
    b = b.cut(throat).cut(under)
    # block screws: clearance holes, counterbored from underneath
    for x, y in BLOCK_SCREWS:
        b = b.cut(drill(x, y, -1, BAR_H + 1, 5.5)).cut(drill(x, y, -1, 5.5, 9.5))
    # scale: ticks every millimetre of span, longer every 5 and 10, the named spans labelled
    marks = cq.Workplane('XY')
    for span10 in range(950, 1601, 10):
        span = span10 / 10
        x = pivot_for(span) - CAR_X / 2
        n = round(span)
        if abs(span - n) > 1e-6:
            continue
        ln = 6.0 if n % 10 == 0 else 4.0 if n % 5 == 0 else 2.5
        marks = marks.union(cq.Workplane('XY').center(x, SCALE_Y[0] + ln / 2)
                            .rect(0.25, ln).extrude(ENGRAVE).translate((0, 0, BAR_H - ENGRAVE)))
        if n % 10 == 0:
            marks = marks.union(cq.Workplane('XY').workplane(offset=BAR_H - ENGRAVE)
                                .center(x, SCALE_Y[0] + 8.5).text(str(n), 3.0, ENGRAVE, kind='bold'))
    for name, span in SPANS.items():
        x = pivot_for(span) - CAR_X / 2
        marks = marks.union(cq.Workplane('XY').center(x, (SCALE_Y[0] + SCALE_Y[1]) / 2)
                            .rect(0.4, SCALE_Y[1] - SCALE_Y[0]).extrude(ENGRAVE).translate((0, 0, BAR_H - ENGRAVE)))
        marks = marks.union(cq.Workplane('XY').workplane(offset=BAR_H - ENGRAVE)
                            .center(x + 4.5, SCALE_Y[1] - 2.5).text(name, 2.5, ENGRAVE, kind='bold'))
    return b.cut(marks)


def carriage():
    c = cq.Workplane('XY').box(CAR_X, CAR_Y, CAR_T).translate((0, 0, CAR_T / 2))
    c = c.union(cq.Workplane('XY').box(CAR_X, TONGUE_W, TONGUE_D).translate((0, 0, -TONGUE_D / 2)))
    for y in (BENDER_HOLES / 2, -BENDER_HOLES / 2):          # tapped for the bender's screws
        c = c.cut(drill(0, y, -1, CAR_T + 1, TAP_DRILL[BENDER_TAP]))
    for x in (CAR_CLAMP_X, -CAR_CLAMP_X):                    # thumb screws to the T-nuts
        c = c.cut(drill(x, 0, -TONGUE_D - 1, CAR_T + 1, 6.6))
    # index line at the pivot on the front edge, and at the left edge where the scale is read
    idx = (cq.Workplane('XY').center(0, -CAR_Y / 2 + 4).rect(0.4, 8).extrude(ENGRAVE)
           .union(cq.Workplane('XY').center(-CAR_X / 2 + 2, BAR_W / 2 - 2).rect(4, 0.4).extrude(ENGRAVE))
           .translate((0, 0, CAR_T - ENGRAVE)))
    return c.cut(idx)


def block():
    w, h = BLOCK_X1 - BLOCK_X0, BLOCK_TOP - BAR_H
    k = cq.Workplane('XY').box(w, BAR_W, h).translate(((BLOCK_X0 + BLOCK_X1) / 2, 0, BAR_H + h / 2))
    groove = cq.Workplane('XY').box(w + 2, GROOVE_W, GROOVE_D + 1).translate(
        ((BLOCK_X0 + BLOCK_X1) / 2, 0, FLOOR_Z + (GROOVE_D + 1) / 2))
    leg = cq.Workplane('XY').box(LEG_SLOT_W, BAR_W / 2 + 1, GROOVE_D + 1).translate(
        (LEG_X, -BAR_W / 4, FLOOR_Z + (GROOVE_D + 1) / 2))
    k = k.cut(groove).cut(leg)
    k = k.cut(drill(LEG_X + CLAMP[0], CLAMP[1], BLOCK_TOP - 12, BLOCK_TOP + 1, TAP_DRILL['M5']))   # clamp, tapped M5
    for x, y in BLOCK_SCREWS:                                                                      # tapped M5 from below
        k = k.cut(drill(x, y, BAR_H - 1, BAR_H + 12, TAP_DRILL['M5']))
    return k


def main():
    os.makedirs(OUT, exist_ok=True)
    b, c, k = bar(), carriage(), block()
    c7 = c.translate((pivot_for(SPANS['7U']), 0, BAR_H))
    for name, part in (('bar', b), ('carriage', c), ('block', k)):
        cq.exporters.export(part, f'{OUT}/{name}.step')
    asm = cq.Assembly()
    asm.add(b, name='bar', color=cq.Color(0.75, 0.75, 0.78))
    asm.add(c7, name='carriage', color=cq.Color(0.55, 0.6, 0.7))
    asm.add(k, name='block', color=cq.Color(0.6, 0.65, 0.6))
    asm.save(f'{OUT}/jig-assembly.step')
    whole = b.union(c7).union(k)
    opts = dict(width=1400, height=600, marginLeft=20, marginTop=20, showAxes=False,
                strokeWidth=0.4, showHidden=False)
    cq.exporters.export(whole, f'{OUT}/jig-iso.svg', opt=dict(opts, projectionDir=(1, -1.4, 1.1)))
    cq.exporters.export(whole, f'{OUT}/jig-top.svg', opt=dict(opts, projectionDir=(0, 0, 1)))
    cq.exporters.export(k, f'{OUT}/block-iso.svg', opt=dict(opts, width=700, height=600, projectionDir=(1, -1.2, 1.3)))
    print(f'wire floor {FLOOR_Z:.2f} mm above the table; pivot for 7U at x {pivot_for(SPANS["7U"]):.2f}; '
          f'carriage travels {pivot_for(160):.1f}..{pivot_for(95):.1f}')


if __name__ == '__main__':
    main()

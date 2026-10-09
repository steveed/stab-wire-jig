# stab-wire-jig

A machinable jig for bending the wires of long keyboard stabilisers (6.25U, 7U, 8U and 9U space bars),
which are hard to buy and usually bent by hand.

The jig is an aluminium bar with a fixed block on the right that holds the wire, and a carriage on
the left that carries a [Du-Bro E/Z Bender](https://www.dubro.com/products/e-z-bender-wire-forming-tool)
wire-forming tool. The carriage slides along the bar and locks at the span you want, read off an
engraved scale; the first leg sits in the block's slot, so the second bend lands the right distance
from it every time.

The design is generated from parametric scripts: STEP files and a dimensioned PDF drawing for a
machine shop.

## How it works

One bender, used twice, with the wire turned over between the bends (the E/Z Bender only bends
clockwise, so two bends without the flip would give a Z, not a U):

1. Bend the first leg: lay the straight wire through the block's straight groove and the bender, and
   bend. (Or bend it freehand.)
2. Turn the wire over and lay that leg in the block's cross slot, pointing towards you, with the
   wire along the straight groove and through the bender.
3. Clamp it with the block's screw and washer, set the carriage to the span on the scale, lock it,
   and bend the second leg.

## Parts

`jig.py` (CadQuery) generates them; `make model` writes STEP files and SVG views to `build/`, and
`make drawing` writes the dimensioned shop drawing, `build/jig-drawing.pdf` (`drawing.py`, from the
same parameters). For a machine shop, send the PDF and the three part STEP files.

- **Bar:** 6061 aluminium, 350 x 40 x 15 mm: a 300 mm working length with a T-slot (6.5 mm throat,
  11 mm undercut) for M6 T-nuts and the scale engraved on its top, and a 25 mm bench tab at each end,
  milled down to 5 mm (the T-slot's floor, so T-nuts still slide in from the left) with a 6.5 x 12 mm
  slotted hole for a screw or bolt into the bench.
- **Carriage:** 76 x 130 x 8 mm. The bender bolts to it through its two holes (101.14 mm apart,
  tapped M4), its long axis across the bar. A tongue underneath rides in
  the slot to keep it square; two M6 thumb screws lock it. Its left edge is the scale's index.
- **Block:** fixed on the right with two M5 screws from under the bar. Its top holds the wire at the
  bender's height: the floor of its grooves is 41.15 mm above the carriage, the height of the bottom
  of the bender's wire slot above its base. It has a straight groove along the wire's line and a
  cross slot for the bent leg, both 1.2 mm deep so the 1.5 mm wire stands proud, and a tapped M5 hole
  where a screw and fender washer clamp the wire in both.
- **Scale:** reads the span between leg centres at the carriage's left edge, every millimetre from 95
  to 160 mm, with the four spans marked. It assumes the second leg forms 4.65 mm (half the 7.8 mm pin
  plus half the wire) from the pivot towards the block; check it with the first bends and mark your
  own positions.

## Spans

The distance between the two bends (centre to centre of the wire's legs), Cherry-style stabilisers:

| Space bar | Span |
|---|---|
| 6.25U | 100.0 mm |
| 7U | 114.3 mm |
| 8U | 133.35 mm |
| 9U | 152.4 mm |

From 7U up the span is (n - 1) x 19.05 mm. The bar is engraved with each span's name at its holes.

## Wire

1.5 mm 304 stainless rod, 300 mm lengths, for example
[this one](https://www.amazon.com/dp/B09636CL3N). 1.5 mm (0.059") is within the E/Z Bender's
1.45-2.40 mm range (SKU 481) and under Du-Bro's 0.062" limit for hardened wire. A 9U wire needs about
152 mm plus two legs, so one rod makes one wire.

## Measured

From the E/Z Bender and a finished wire (reference photos are kept locally, not in the repo):

- mounting holes 101.14 mm apart, the pivot exactly midway; overall length 115.58 mm, 41.21 mm wide;
- 41.15 mm from the bottom of its base to the bottom of the wire slot between its pins;
- centre pin 7.8 mm, the opening between the pins 2.2 mm; it bends clockwise only;
- legs 12.05 mm (tip to the outside of the long bar).

## Status

Model and shop drawing done. The scale's 4.65 mm offset is to be confirmed with the first test bends.

## License

[CC0 1.0](LICENSE): public domain. Use, change, make or sell it with no conditions.

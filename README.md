# stab-wire-jig

A machinable jig for bending the wires of long keyboard stabilisers (6.25U, 7U, 8U and 9U space bars),
which are hard to buy and usually bent by hand.

The jig is an aluminium bar that holds two [Du-Bro E/Z Bender](https://www.dubro.com/products/e-z-bender-wire-forming-tool)
wire-forming tools a set distance apart: one fixed at a datum, one on a carriage that pins into reamed
holes for each span. Lay a straight wire in the bar's groove against the end stop, bend both legs, and
the distance between the bends comes out right every time.

The design will be generated from one parametric script, with a dimensioned PDF drawing, a DXF of the
hole pattern and a STEP model for a machine shop.

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

## To measure

Photos and measurements go in [`photos/`](photos/):

- the E/Z Bender's base: footprint, mounting holes (size and spacing), and the wire's height above the
  base;
- which way it bends: where the bend forms relative to the tool (a photo mid-bend);
- a finished wire: leg length, and any bend at the tips.

## Status

Collecting measurements; no design yet.

## License

[CC0 1.0](LICENSE): public domain. Use, change, make or sell it with no conditions.

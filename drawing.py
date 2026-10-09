"""Dimensioned shop drawing for the jig, from the same parameters as the model (jig.py).

    docker compose run --rm cad python drawing.py      (make drawing)

Writes build/jig-drawing.pdf: one page per part.  Every part is dimensioned from its left end and
its front edge (the edge towards you); the bar's x datum is its left end, tab included.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import jig as J

OUT = 'build/jig-drawing.pdf'
INK = '#111'
HIDDEN = dict(color=INK, lw=0.6, ls=(0, (4, 2)))
GENERAL = ('Material: 6061-T6 aluminium.  Units: mm.  General tolerance +-0.1 unless noted.  '
           'Break sharp edges.  Engraving 0.3 deep.')


def page(title, notes):
    fig = plt.figure(figsize=(17, 11))           # tabloid, landscape
    fig.text(0.03, 0.96, title, fontsize=18, weight='bold')
    fig.text(0.03, 0.935, 'stab-wire-jig  -  github.com/steveed/stab-wire-jig  -  CC0', fontsize=9, color='#555')
    y = 0.08
    for n in reversed([GENERAL] + notes):
        fig.text(0.03, y, n, fontsize=10)
        y += 0.022
    return fig


def view(fig, rect, xlim, ylim, label):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(label, fontsize=11, loc='left')
    return ax


def box(ax, x0, y0, w, h, **kw):
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, ec=INK, lw=kw.pop('lw', 1.2), **kw))


def hole(ax, x, y, d, **kw):
    ax.add_patch(Circle((x, y), d / 2, fill=False, ec=INK, lw=kw.pop('lw', 1.0), **kw))
    ax.plot([x - d * 0.8, x + d * 0.8], [y, y], color=INK, lw=0.3)
    ax.plot([x, x], [y - d * 0.8, y + d * 0.8], color=INK, lw=0.3)


def dim(ax, a, b, off, text=None, vertical=False, fs=8):
    """Dimension between points a and b, drawn `off` away (perpendicular), with extension lines."""
    (x1, y1), (x2, y2) = a, b
    t = text or f'{abs((y2 - y1) if vertical else (x2 - x1)):.2f}'.rstrip('0').rstrip('.')
    if vertical:
        x = max(x1, x2) + off if off > 0 else min(x1, x2) + off
        for xx, yy in (a, b):
            ax.plot([xx, x + (1 if off > 0 else -1)], [yy, yy], color=INK, lw=0.3)
        ax.annotate('', (x, y1), (x, y2), arrowprops=dict(arrowstyle='<->', lw=0.6, color=INK, shrinkA=0, shrinkB=0))
        ax.text(x + (1.2 if off > 0 else -1.2), (y1 + y2) / 2, t, rotation=90, va='center',
                ha='left' if off > 0 else 'right', fontsize=fs)
    else:
        y = max(y1, y2) + off if off > 0 else min(y1, y2) + off
        for xx, yy in (a, b):
            ax.plot([xx, xx], [yy, y + (1 if off > 0 else -1)], color=INK, lw=0.3)
        ax.annotate('', (x1, y), (x2, y), arrowprops=dict(arrowstyle='<->', lw=0.6, color=INK, shrinkA=0, shrinkB=0))
        ax.text((x1 + x2) / 2, y + (0.8 if off > 0 else -0.8), t, ha='center',
                va='bottom' if off > 0 else 'top', fontsize=fs)


def note(ax, x, y, tx, ty, text, fs=8):
    ax.annotate(text, (x, y), (tx, ty), fontsize=fs, arrowprops=dict(arrowstyle='-', lw=0.5, color=INK))


def bar_page(pdf):
    L, W, H, T = J.BAR_L + 2 * J.TAB_L, J.BAR_W, J.BAR_H, J.TAB_T
    ox = J.TAB_L                                  # model x -> drawing x (datum: left end, tab included)
    fy = J.BAR_W / 2                              # model y -> drawing y (datum: front edge)
    span_x = {n: J.pivot_for(s) - J.CAR_X / 2 + ox for n, s in J.SPANS.items()}
    fig = page('BAR  (1 off)', [
        f'T-slot: {J.SLOT_THROAT} throat x {J.SLOT_THROAT_D} deep, {J.SLOT_UNDER} undercut x {J.SLOT_UNDER_D}; '
        f'open at the left end, closed at {J.SLOT_END + ox:g}.  Takes M6 T-nuts.',
        f'Tabs milled to {T:g} thick (the T-slot floor), so T-nuts slide in over the left tab.',
        'Block screws: 5.5 thru, counterbored 9.5 x 5.5 deep from underneath (M5 socket head).',
        'Scale (engraved on top, behind the slot): a tick every 1 mm of span from 95 to 160, 2.5 long, 4 at '
        'every 5, 6 at every 10 with the number; span s sits at x = '
        f'{J.LEG_X + ox - J.BEND_OFFSET - J.CAR_X / 2:.2f} - s.',
        'Named spans, full-height line and label: ' + ', '.join(f'{n} at x {x:.2f}' for n, x in span_x.items()) + '.',
    ])
    top = view(fig, [0.04, 0.45, 0.92, 0.45], (-20, L + 45), (-55, W + 25), 'Top')
    box(top, 0, 0, L, W)
    top.plot([J.TAB_L, J.TAB_L], [0, W], color=INK, lw=0.8)
    top.plot([L - J.TAB_L, L - J.TAB_L], [0, W], color=INK, lw=0.8)
    for cx in (J.TAB_L / 2, L - J.TAB_L / 2):
        sl, sw = J.TAB_SLOT
        top.add_patch(FancyBboxPatch((cx - sl / 2, fy - sw / 2), sl, sw,
                                     boxstyle=f'round,pad=0,rounding_size={sw / 2}', fill=False, ec=INK, lw=1))
    box(top, ox, fy - J.SLOT_THROAT / 2, J.SLOT_END, J.SLOT_THROAT, lw=0.9)
    top.plot([ox, ox + J.SLOT_END], [fy - J.SLOT_UNDER / 2] * 2, **HIDDEN)
    top.plot([ox, ox + J.SLOT_END], [fy + J.SLOT_UNDER / 2] * 2, **HIDDEN)
    for x, y in J.BLOCK_SCREWS:
        hole(top, x + ox, y + fy, 5.5)
        top.add_patch(Circle((x + ox, y + fy), 9.5 / 2, fill=False, **HIDDEN))
    for n, x in span_x.items():
        top.plot([x, x], [fy + J.SCALE_Y[0], fy + J.SCALE_Y[1]], color=INK, lw=0.6)
        top.text(x + 0.8, fy + J.SCALE_Y[1] - 3, n, fontsize=6)
    dim(top, (0, W), (L, W), 14)
    dim(top, (0, W), (J.TAB_L, W), 6)
    dim(top, (L - J.TAB_L, W), (L, W), 6)
    dim(top, (0, 0), (ox + J.SLOT_END, 0), -16)
    dim(top, (0, 0), (J.TAB_L / 2, 0), -8)
    dim(top, (0, 0), (span_x['9U'], 0), -24, f'{span_x["9U"]:.2f} (9U tick)')
    for i, (x, y) in enumerate(J.BLOCK_SCREWS):
        dim(top, (0, 0), (x + ox, 0), -32 - 8 * i)
        dim(top, (L, 0), (L, y + fy), 8 + 8 * i, vertical=True)
    dim(top, (L, 0), (L, W), 26, vertical=True)
    dim(top, (0, 0), (0, fy), -8, vertical=True)
    note(top, J.TAB_L / 2 + 4, fy + 3, 20, W + 20, f'slot {J.TAB_SLOT[0]:g} x {J.TAB_SLOT[1]:g}, 2 places')

    sec = view(fig, [0.04, 0.20, 0.30, 0.22], (-12, W + 30), (-8, H + 12), 'Section through the slot (from the left)')
    pts = [(0, 0), (W, 0), (W, H), (fy + J.SLOT_THROAT / 2, H), (fy + J.SLOT_THROAT / 2, H - J.SLOT_THROAT_D),
           (fy + J.SLOT_UNDER / 2, H - J.SLOT_THROAT_D), (fy + J.SLOT_UNDER / 2, T), (fy - J.SLOT_UNDER / 2, T),
           (fy - J.SLOT_UNDER / 2, H - J.SLOT_THROAT_D), (fy - J.SLOT_THROAT / 2, H - J.SLOT_THROAT_D),
           (fy - J.SLOT_THROAT / 2, H), (0, H), (0, 0)]
    sec.plot(*zip(*pts), color=INK, lw=1.2)
    dim(sec, (0, 0), (W, 0), -4)
    dim(sec, (W, 0), (W, H), 4, vertical=True)
    dim(sec, (fy - J.SLOT_THROAT / 2, H), (fy + J.SLOT_THROAT / 2, H), 4, f'{J.SLOT_THROAT} +0.1/-0')
    dim(sec, (fy - J.SLOT_UNDER / 2, T), (fy + J.SLOT_UNDER / 2, T), -3)
    dim(sec, (W, T), (W, 0), 13, f'{T:g} (tab)', vertical=True)
    dim(sec, (W, H - J.SLOT_THROAT_D), (W, H), 20, vertical=True)

    tab = view(fig, [0.40, 0.20, 0.30, 0.22], (-15, 60), (-8, H + 12), 'Left end, from the front')
    tab.plot([0, J.TAB_L, J.TAB_L, J.TAB_L + 30], [T, T, H, H], color=INK, lw=1.2)
    tab.plot([0, 0, J.TAB_L + 30], [T, 0, 0], color=INK, lw=1.2)
    dim(tab, (0, 0), (J.TAB_L, 0), -4)
    dim(tab, (0, 0), (0, T), -4, vertical=True)
    pdf.savefig(fig)
    plt.close(fig)


def carriage_page(pdf):
    X, Y, T = J.CAR_X, J.CAR_Y, J.CAR_T
    cx, cy = X / 2, Y / 2                       # the pivot, in drawing coordinates (left end, front edge)
    fig = page('CARRIAGE  (1 off)', [
        f'Bender holes: tapped {J.BENDER_TAP} thru ({J.TAP_DRILL[J.BENDER_TAP]} drill), {J.BENDER_HOLES} apart +-0.05 '
        '(they take the bender\'s two mounting screws).',
        f'Thumb-screw holes: 6.6 thru (M6), to T-nuts in the bar.',
        f'Tongue: {J.TONGUE_W} -0.05/-0.1 wide x {J.TONGUE_D} high, the full length, centred: a sliding fit in the '
        f'bar\'s {J.SLOT_THROAT} slot.',
        'Engrave: a 0.4 line 8 long at the pivot on the front edge; a 0.4 x 4 index line at the left edge, '
        f'{J.BAR_W / 2 - 2:g} behind the pivot line, where the bar\'s scale is read.',
    ])
    top = view(fig, [0.05, 0.20, 0.42, 0.66], (-30, X + 45), (-30, Y + 25), 'Top')
    box(top, 0, 0, X, Y)
    for y in (cy - J.BENDER_HOLES / 2, cy + J.BENDER_HOLES / 2):
        hole(top, cx, y, J.TAP_DRILL[J.BENDER_TAP])
    for x in (cx - J.CAR_CLAMP_X, cx + J.CAR_CLAMP_X):
        hole(top, x, cy, 6.6)
    top.plot([0, X], [cy - J.TONGUE_W / 2] * 2, **HIDDEN)
    top.plot([0, X], [cy + J.TONGUE_W / 2] * 2, **HIDDEN)
    top.plot([cx, cx], [0, 8], color=INK, lw=0.8)
    top.plot([0, 4], [cy + J.BAR_W / 2 - 2] * 2, color=INK, lw=0.8)
    dim(top, (0, Y), (X, Y), 8)
    dim(top, (0, 0), (cx, 0), -8)
    dim(top, (0, 0), (cx - J.CAR_CLAMP_X, 0), -16)
    dim(top, (0, 0), (cx + J.CAR_CLAMP_X, 0), -24)
    dim(top, (X, 0), (X, Y), 30, vertical=True)
    dim(top, (X, 0), (X, cy - J.BENDER_HOLES / 2), 8, vertical=True)
    dim(top, (X, cy - J.BENDER_HOLES / 2), (X, cy + J.BENDER_HOLES / 2), 8, f'{J.BENDER_HOLES} +-0.05', vertical=True)
    dim(top, (0, 0), (0, cy), -10, vertical=True)
    dim(top, (0, cy), (0, cy + J.BAR_W / 2 - 2), -20, vertical=True)
    note(top, cx + 2, cy - J.BENDER_HOLES / 2, cx + 20, cy - J.BENDER_HOLES / 2 - 18, f'{J.BENDER_TAP} thru, 2 places')
    note(top, cx + J.CAR_CLAMP_X + 2, cy + 2, cx + J.CAR_CLAMP_X + 10, cy + 20, '6.6 thru, 2 places')

    end = view(fig, [0.55, 0.45, 0.40, 0.40], (-30, Y + 30), (-15, T + 20), 'End view (from the left)')
    pts = [(0, 0), (cy - J.TONGUE_W / 2, 0), (cy - J.TONGUE_W / 2, -J.TONGUE_D), (cy + J.TONGUE_W / 2, -J.TONGUE_D),
           (cy + J.TONGUE_W / 2, 0), (Y, 0), (Y, T), (0, T), (0, 0)]
    end.plot(*zip(*pts), color=INK, lw=1.2)
    dim(end, (0, T), (Y, T), 6)
    dim(end, (Y, 0), (Y, T), 6, vertical=True)
    dim(end, (cy - J.TONGUE_W / 2, -J.TONGUE_D), (cy + J.TONGUE_W / 2, -J.TONGUE_D), -4, f'{J.TONGUE_W} -0.05/-0.1')
    dim(end, (cy + J.TONGUE_W / 2, -J.TONGUE_D), (cy + J.TONGUE_W / 2, 0), 12, vertical=True)
    pdf.savefig(fig)
    plt.close(fig)


def block_page(pdf):
    X, Y, Hb = J.BLOCK_X1 - J.BLOCK_X0, J.BAR_W, J.BLOCK_TOP - J.BAR_H
    lx = J.LEG_X - J.BLOCK_X0                   # leg slot centre, from the left end
    fy = Y / 2
    floor = J.FLOOR_Z - J.BAR_H
    fig = page('WIRE BLOCK  (1 off)', [
        f'Groove floor {floor:.2f} +-0.03 above the bottom: the wire\'s underside must sit at the same height as in '
        f'the bender ({J.BENDER_SLOT} above its base, on the {J.CAR_T:g} carriage).',
        f'Straight groove {J.GROOVE_W} wide x {J.GROOVE_D} deep, the full length, on the centreline.  '
        f'Leg slot {J.LEG_SLOT_W} wide x {J.GROOVE_D} deep, from the groove to the front face.',
        f'Clamp: M5 tapped {12:g} deep ({J.TAP_DRILL["M5"]} drill), for an M5 screw and a fender washer that bears on '
        'the wire in both the groove and the slot.',
        'Underneath: 2x M5 tapped 12 deep, for the screws through the bar.',
    ])
    top = view(fig, [0.05, 0.22, 0.40, 0.64], (-25, X + 45), (-30, Y + 35), 'Top')
    box(top, 0, 0, X, Y)
    box(top, 0, fy - J.GROOVE_W / 2, X, J.GROOVE_W, lw=0.8)
    box(top, lx - J.LEG_SLOT_W / 2, 0, J.LEG_SLOT_W, fy - J.GROOVE_W / 2, lw=0.8)
    hole(top, lx + J.CLAMP[0], fy + J.CLAMP[1], J.TAP_DRILL['M5'])
    for x, y in J.BLOCK_SCREWS:
        top.add_patch(Circle((x - J.BLOCK_X0, y + fy), J.TAP_DRILL['M5'] / 2, fill=False, **HIDDEN))
    dim(top, (0, Y), (X, Y), 8)
    dim(top, (0, 0), (lx, 0), -8, f'{lx:g} (leg slot centre)')
    dim(top, (0, 0), (lx + J.CLAMP[0], 0), -16)
    for i, (x, y) in enumerate(J.BLOCK_SCREWS):
        dim(top, (0, Y), (x - J.BLOCK_X0, Y), 16 + 8 * i)
        dim(top, (X, 0), (X, y + fy), 14 + 8 * i, vertical=True)
    dim(top, (X, 0), (X, Y), 32, vertical=True)
    dim(top, (0, 0), (0, fy), -8, vertical=True)
    dim(top, (0, 0), (0, fy + J.CLAMP[1]), -16, vertical=True)

    front = view(fig, [0.52, 0.25, 0.42, 0.62], (-25, Y + 35), (-10, Hb + 12), 'Front (looking along the groove)')
    pts = [(0, 0), (Y, 0), (Y, Hb), (fy + J.GROOVE_W / 2, Hb), (fy + J.GROOVE_W / 2, floor),
           (fy - J.GROOVE_W / 2, floor), (fy - J.GROOVE_W / 2, Hb), (0, Hb), (0, 0)]
    front.plot(*zip(*pts), color=INK, lw=1.2)
    dim(front, (Y, 0), (Y, Hb), 6, vertical=True)
    dim(front, (0, 0), (0, floor), -8, f'{floor:.2f} +-0.03', vertical=True)
    dim(front, (fy - J.GROOVE_W / 2, Hb), (fy + J.GROOVE_W / 2, Hb), 5)
    dim(front, (Y, floor), (Y, Hb), 16, f'{J.GROOVE_D}', vertical=True)
    dim(front, (0, 0), (Y, 0), -5)
    pdf.savefig(fig)
    plt.close(fig)


def main():
    with PdfPages(OUT) as pdf:
        bar_page(pdf)
        carriage_page(pdf)
        block_page(pdf)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()

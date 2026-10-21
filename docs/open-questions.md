# Open questions

Data in the library that is still unverified or estimated. Corrections (with a source or a
measurement) are welcome as pull requests.

| Entry | Question |
|---|---|
| `lian-li/uni-fan-tl-controller` | Physical size and exact port count/positions of the 2nd generation controller are not published. 80 x 50 x 16 mm is a placeholder. |
| `gskill/trident-z5-rgb-ddr5-8000` | No G.Skill datasheet found for F5-8000J4048G24G. Dimensions come from the Trident Z5 RGB family (a review teardown); LED order along the bar is unverified. |
| `lian-li/uni-fan-tl-*` | How the manufacturer's two light zones map to the measured 13 bottom + 13 top LEDs (zones are named `bottom` and `top`). LED positions within the bars are derived from a grid, not measured. |
| `asus/rog-strix-x870e-e-gaming-wifi` | Positions of the 9 I/O cover LEDs and the exact cover outline; ASUS publishes no lighting zones. |
| `lian-li/o11-dynamic-evo-argb-strip` | Exact course of the built-in strip (the split of 17 front + 30 side LEDs is a guess), its length and LED density. |
| `lian-li/o11-dynamic-evo` (case) | Positions of fan mounts, motherboard tray, PSU area and the whole outline are estimated from the specification; only external dimensions and fan/radiator numbers are manufacturer data. Fans are drawn edge-on in the glass view, which was derived, not checked on photos. The RGB variant is not covered. |
| `alphacool/*` | LED positions of the distro plate, GPU block and CPU block are placeholders. LED counts: plate 18 (manufacturer) vs 20 (measured on a shared splitter channel); GPU block 11; Apex 1 has no published count, 8 measured. |

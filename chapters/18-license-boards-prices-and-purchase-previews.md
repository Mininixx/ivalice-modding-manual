# 18. License boards, prices and purchase previews

[← Chapter index](../README.md#chapters)

Use one authoritative cost view and migrate before granting or purchasing nodes.

## Give each board one authoritative view
Selection, preview, preflight, LP debit and description must use the same board-aware cost view (`irlay_cost_view`). Ownership takes precedence over affordability: an owned license remains owned even at zero LP. The mini-board path at `0x55F96F` calls `0x323600` with flags 0; the open board uses flags 1, so both routes need the ownership policy.

Keep class-specific names, help, icons and equipment grants keyed by class and license. A shared native string or license ID must not silently replace the presentation/effect on another class. Use the assigned primary class for D205 ownership and icon lookup, including aliases 9/10/11.

## Use numeric equipment progression and reachable regions
Name equipment nodes sequentially: Armor 1, Armor 2, Armor 3, and so on. Do not restore Gear A/B labels, free “included” partner nodes or hidden A-before-B equipment requirements. Preserve ordinary board adjacency, explicit level regions and LP payment.

Use the physical `board_phase` region as the source of level/phase metadata. Early-region nodes must not inherit a later level barrier from stale stage metadata. Keep paths reachable from Essentials within the intended region and fit nodes inside the board silhouette. Match icon type and number to the actual grant, not an old title.

The appended paid equipment licenses `1420–1464` retain their IDs, grants and saved ownership. The legacy raw tables remain `9 × 1420`; use the separate bounded appended cost/level tables rather than stretching raw data and invalidating relocations. The class icon map covers `9 × 1465`, with 205 board cells per canonical class in this layout.

Synchronize source/runtime custom-node catalogs, all nine class boards, loaded board binaries, class-qualified native help and icon descriptors. Preserve every supported language atlas. Never infer UI icon correctness from the node name alone.

## Preserve sparse saved ownership
| Battle KEEP field | D205 layout |
| --- | --- |
| `+0x190` | LP, unsigned 32-bit |
| `+0x194` | Sparse ownership-bit region |
| `+0x1BC` | Low five bits for appended ownership |
| `+0x1BE` | Layout marker `0xD205`, 16-bit |
| `+0x1C0` | Receipt `0x70` |
| `+0x1C1` | Marker `0xB6` |
| `+0x1C2` | Level byte |
| `+0x1C3`, `+0x1C4`, `+0x1C5` | Primary, secondary (`255`), visible class |

Use `irfl_has`, `irfl_set` and `irfl_bit_index` instead of treating license ID as a direct bitmap index. A bulk 46-byte zero from `+0x194` overlaps metadata at `+0x1BE` and `+0x1C1`; do not perform it after initializing those markers. Keep native purchase/guard behavior at `0x323910` / `0x323D10` compatible with the mapped layout.

## Apply migrations before purchase
Run a required migration before selection and before automatic grants. Exclude automatically granted licenses from purchase refunds, record migration once and preserve already owned licenses. A new balance bonus on an owned node does not require repurchase or a retroactive LP debit. Preserve intentional skill-upgrade aliases instead of treating every shared owned bit as a blocked-purchase defect.

---

[← Previous chapter](17-saving-new-resources-inside-each-save.md) · [Chapter index](../README.md#chapters) · [Next chapter →](19-extracting-effects-from-final-fantasy-x.md)

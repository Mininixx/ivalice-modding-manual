# 04. Independent menus with native command execution

[← Chapter index](../README.md#chapters)

Render a separate frontend without replacing the game’s rules for an action.

## Keep the frontend and executor separate
Independent menus need their own cursor, page, selected command and selected target. They should still query native availability, inventory, targeting restrictions and action data. The architecture separates a menu model/presenter from command submission and publishes a coherent native catalog snapshot.

A label is not an action ID. Action data can refer to a separate string-table index. Do not derive executable command IDs from menu positions or assume an action table and name table have equal lengths.

## Confirmation is a transaction
Carry the submitting member, action, full target handle and session identity from selection to confirmation. Revalidate them at submission. A target list can become stale while the player is reading it. Releasing a menu must also release its input capture and any native wait-mode bridge it owns.

For the native leader, mirror the native menu state instead of having two unrelated systems each believe they own P1. Native dialogs, story interactions and battle menus need explicit precedence.

## Authenticate identities when painting target information
The target-info panel's Libra query depends on `companion_identities`. Include that authenticated identity API in the installed frozen module and support the no-Libra branch as well as the ordinary party-member branch. Target information and command admission should both use the same validated actor identities.

## Keep player selectors independent
Maintain a separate Character Select owner for P1, P2 and P3. One player's selector must not block another player's opening, and selecting a free character must work from every enabled player slot. Apply ownership changes through the shared role transaction described in the input chapter.

## Respect interaction precedence and menu lifecycle
An actionable native use prompt takes precedence over opening a battle menu on the same Confirm edge. Opening or closing a custom selector must not briefly revoke movement for unrelated players. Distinguish the custom wait bridge from a real Party/Pause frontend, and retire only the input/menu leases owned by the closing UI.

## Keep layout and localization in the same path
Resolve user-facing labels from the selected language throughout the launcher, including secondary explanatory panels. Measure available column width after localization and scaling; wrap or clip within the owning panel instead of placing text over the next column. Keep actions keyed by IDs rather than translated labels. A game's language choice must not change controller assignment or the meaning of Confirm/Cancel.

---

[← Previous chapter](03-binding-controllers-to-live-actor-identities.md) · [Chapter index](../README.md#chapters) · [Next chapter →](05-multiple-native-target-circles.md)

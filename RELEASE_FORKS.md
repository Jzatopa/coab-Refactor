# COAB Release Forks

Effective July 26, 2026, this project is maintained as two sibling releases from the same shared baseline.

## High Res Release

The High Res Release is the preservation-oriented edition. Its goal is to keep Curse of the Azure Bonds gameplay, rules, timing, content, menus, layouts, and progression equivalent to the original while replacing eligible presentation assets with faithful high-resolution counterparts.

Allowed work includes:

- high-resolution replacements for original artwork, portraits, fonts, frames, audio, tiles, and other presentation assets;
- rendering, scaling, platform, input, packaging, and compatibility fixes needed for modern systems;
- bug fixes required to reproduce intended original behavior;
- validation and lifecycle safeguards that prevent HD assets from changing gameplay or obscuring original state transitions.

Creative redesigns, new gameplay systems, rebalanced rules, rewritten encounters, expanded content, and AI-authored departures from the original belong in the Unleased AI Release instead.

## Unleased AI Release

The Unleased AI Release begins from the same engine, compatibility work, HD asset catalog, tests, and validated baseline as the High Res Release. It is the experimental edition where AI-assisted development may improve or reimagine any part of the experience: visuals, audio, interfaces, encounters, systems, writing, animation, accessibility, intelligence, and presentation.

The AI release may diverge freely, but shared engine fixes and original-faithful HD improvements should be implemented or backported to both releases whenever they remain compatible with the High Res mission.

## Synchronization rule

Both releases share tag `release-fork-shared-baseline-2026-07-26`. Shared fixes should be committed in narrowly scoped changes that can be cherry-picked between repositories. A difference is considered intentional only when it is documented as release-specific; otherwise it is treated as synchronization debt.

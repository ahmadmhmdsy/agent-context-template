# Data and asset handling (optional module)

Install with `adopt.py --modules data`. It supplements the root data rules with a
project-fillable classification and recipe table.

## Asset classes

Classify every asset before touching it. The class decides what is safe.

| Class | Meaning | Safe to delete? |
|---|---|---|
| precious | irreplaceable; no source can recreate it | never without a backup |
| regenerable | reclaimed by a recorded recipe that still works | yes, once the recipe is proven |
| generated | produced by the build from tracked sources | yes; rebuild it |
| vendored | external, tracked exactly as published | no; it is the only offline copy |
| temporary | scratch, cache, or intermediate | yes, at the end of the session |

An asset with no working recipe is **precious**, whatever its folder is called.

## Regeneration recipes

Every regenerable asset names its recipe. A blank recipe cell reclassifies the
asset as precious.

| Asset (path) | Class | Recipe (exact command) | Output location | Verified |
|---|---|---|---|---|
| | | | | |

## Retention

- Keep precious and vendored assets for as long as the project lives.
- Rebuild generated assets rather than archiving them.
- Pin one reviewed copy of each regenerable output; drop older copies.
- Treat temporary paths as cleared at session end.

## Deleting this directory loses nothing

Removing this directory changes no asset and no recipe. It is guidance only, and
the project's own paths live in its environment document.


# Brand — A-Team Contracting

The image pipeline reads this. So does the offer-compliance linter.

---

## Color

| Role | Hex | Where it goes |
|---|---|---|
| Orange | `#F58220` | The AFTER chip, the YOUR PRICE box, accents. One bold thing per graphic. |
| Blue | `#1B5B98` | Header and footer bars, structural fields. |
| Charcoal | `#333333` | The BEFORE chip, body text, footer bar on the stacked template. |
| White | `#FFFFFF` | Text on blue or charcoal, ground on light layouts. |

Orange is the accent, not the ground. If a graphic reads as mostly orange,
something has gone wrong.

**Not brand:** bright yellow price text, red starbursts, drop shadows on type,
gradients behind headlines. These show up in generic ad templates and they do not
belong on A-Team work. See the note on `IMG_0399` in `docs/ARCHITECTURE.md`.

## Type

| Role | Face |
|---|---|
| Headlines | Anton |
| Body | Montserrat |
| Accent | Caveat |

Caveat is for a single human touch, never for a price or a service name.

## Logo

- Always the transparent PNG. **Never the gray-background master file.**
- Matched by Drive file ID, not filename. The correct file is
  `ATeam Logo Web 1200.png` (`1Np9lmVCrhkWjz7LvmkcYRqVuujYpooiY`). A copy of the
  gray master sits loose in the Drive root under an untitled upload name, which
  is exactly how the wrong one gets picked up.
- Placement on generated composites: bottom right, 12% of image width, 85%
  opacity.
- Transparency is cut by **edge flood fill from all four corners**, never by
  color key. Color key eats the white interior detail inside the shield.

## Phone number

`(937) 939-2936` appears **in the image graphic only**.

Never in Google Business Profile body text. Never in Nextdoor body text. Google
suppresses posts carrying a 10-digit number and Nextdoor reads it as an ad. Every
branded template Ant already uses bakes the number into the footer, which is the
correct place for it.

## Pricing display

Three lines, in this order, every time a price appears on a graphic:

    Full retail value        e.g.  $450 value
    A-Team Discount          one line, one named discount
    YOUR PRICE               in the orange box

No stacked discounts. No "was/now/plus an extra." No games. One discount, one
final number, in the box.

**A scarcity claim needs a real end date.** "Limited time only" with no date
fails the linter. "Booked before August 22" passes.

## Language that is brand, not copy

- **Family owned.** Always. Never "one-man operation," never "just me."
- **Clean Club** is ongoing. It is never a contract, and the phrase "cancel
  anytime" never appears.
- Tagline: *Jobs are done best when you work with A-Team!*

## Templates in use

Two live templates were found in the Drive folder. Both are on-brand and the
system should match them rather than invent a third.

**Stacked** (`IMG_0228` through `IMG_0232`) — BEFORE panel over AFTER panel,
charcoal BEFORE chip, orange AFTER chip, black footer bar carrying logo, service
name, phone and website. 1080x1350.

**Side by side** (`IMG_0386`) — header bar with logo and service title, orange
vertical divider between the two halves, footer with the tagline, phone and
website. 1080x1350.

## Output sizes

| Use | Size |
|---|---|
| Facebook and Instagram feed | 1080 x 1350 |
| Google Business Profile | 1080 x 1080 |
| Instagram story | 1080 x 1920 |

Filenames follow the convention already in the folder:

    ATeam-BeforeAfter-siding-softwash-1080x1350-facebook-instagram.jpg

## Pairing rule

When a before and an after have different orientations, normalize them to
**equal height with natural widths.** Never crop to force a matching aspect
ratio. Cropping to match ratios has destroyed good pairs before.

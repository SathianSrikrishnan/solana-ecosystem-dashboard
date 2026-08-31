# Solana Observatory demo-video design — 2026-08-30

## Decision

Use the approved full-length dashboard capture as the primary picture and Sathian's complete camera/narration take as a small lower-right picture-in-picture. Preserve the narration in order and at its recorded pace. Add the existing locally composed instrumental bed quietly beneath the complete presentation, with a restrained lift near the close.

This is the best fit for a three-minute product walkthrough: the dashboard remains the evidence, while the presenter remains visibly responsible for the interpretation.

## Alternatives considered

1. **Full-time picture-in-picture — selected.** Keeps the walkthrough personal and submission-friendly without replacing the product with a talking head.
2. **Presenter only at the opening and close.** Leaves more screen space but makes the presentation feel assembled from separate parts.
3. **Voice-only dashboard walkthrough.** Maximizes metric visibility but loses the human presenter requested for the demo.

## Picture treatment

- Master canvas: 1920 x 1080, 30 fps.
- Dashboard capture remains uncropped and defines the 183.166667-second runtime.
- Camera source remains synchronized from source time zero; it is not stretched.
- Camera crop: fixed 480 x 540 portrait crop around the head and shoulders, scaled to 267 x 300. The tighter crop removes the wall and most of the green surround without risking a brittle background key.
- Treatment: lifted exposure and midtones with mild contrast and saturation correction; six-pixel mint border.
- Placement: lower-right with a 42-pixel safe margin.
- Short alpha fades prevent the presenter window from popping on or off.

## Audio treatment

- Preserve Sathian's real camera audio.
- Apply mild high-pass, low-pass, broadband noise reduction, and compression.
- Reuse the deterministic local 84 BPM instrumental composition. It contains no vocals, samples, or third-party music.
- Keep the music substantially below speech, with a gradual close lift and final fade.
- Master the combined program near -16 LUFS with a conservative -2.0 dB true-peak target.

## Gates

- Local review-render creation: approved by Sathian on 2026-08-30; full owner playback remains pending.
- Edit-plan approval: approved by Sathian on 2026-08-30.
- Publication, upload, deployment, and bounty submission: not approved by this render request.
- A public release must follow owner playback approval and a final verified render.

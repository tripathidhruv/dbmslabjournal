# Design System Specification: The Academic Terminal

## 1. Overview & Creative North Star: "The Digital Curator"
This design system rejects the "cookie-cutter" layout of standard documentation. Our Creative North Star is **The Digital Curator**: a high-end intersection where the precision of a modern IDE meets the tactile, thoughtful layout of a premium leather-bound academic journal. 

Instead of a rigid, flat grid, we utilize **Intentional Asymmetry** and **Tonal Depth**. We treat the screen as a canvas of layered intellectual thought. Sections may overlap slightly, and typography scales are pushed to extremes to create an editorial rhythm. The interface should feel like a living document—highly technical, yet deeply human.

---

## 2. Colors & Surface Philosophy

### The Tonal Palette
The palette is rooted in a deep, nocturnal base to reduce eye strain during long lab sessions, punctuated by high-energy "Electric Cyan" for primary actions and "Soft Amber" for technical warnings or highlights.

*   **Background:** `#10141a` (The Canvas)
*   **Primary (Cyan):** `#a8e8ff` (Text/Icon) | `#00d4ff` (Container)
*   **Secondary (Amber):** `#ffb955` (Text/Icon) | `#dc9100` (Container)
*   **Practical Groups (Status Tints):** 
    *   **Group A:** Blue tint (Primary)
    *   **Group B:** Green tint (Success)
    *   **Group C:** Purple tint (Tertiary)
    *   **Group D:** Orange tint (Secondary)

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. Layout boundaries must be defined solely by background shifts. 
*   Use `surface-container-low` for large section blocks sitting on the `surface` background.
*   Use `surface-container-high` for interactive elements or nested modules.

### Glass & Gradient Signature
To move beyond a "flat" app feel:
*   **Glassmorphism:** Floating navigation bars and modal overlays must use a semi-transparent `surface-container` color with a `20px` backdrop-blur.
*   **Signature Textures:** Main CTA backgrounds should use a linear gradient transitioning from `primary` (#a8e8ff) to `primary_container` (#00d4ff) at a 135-degree angle. This provides the "visual soul" of a premium product.

---

## 3. Typography: Editorial Precision
The system pairs the brutalist, fixed-width nature of code with the soft, authoritative elegance of a serif typeface.

*   **Display & Headlines (`Space Grotesk`):** Used for H1 through H3. This creates a "Modern Developer" feel—wide, geometric, and confident.
*   **Body Text (`Newsreader` / `Source Serif 4`):** Used for all long-form documentation. The serif nature mimics a physical lab journal, making complex DBMS concepts easier to digest.
*   **Code & Labels (`JetBrains Mono` / `Inter`):** All technical strings, queries, and UI labels use mono or clean sans-serifs to ensure zero ambiguity.

**Hierarchy Note:** Use a massive scale jump between `display-lg` (3.5rem) and `body-lg` (1rem). This high contrast removes the "template" look and establishes clear visual dominance.

---

## 4. Elevation & Depth: Tonal Layering

### The Layering Principle
Depth is achieved by "stacking" surface tiers. 
1.  **Level 0 (Base):** `surface` (#10141a)
2.  **Level 1 (Sectioning):** `surface-container-low` (#181c22)
3.  **Level 2 (Interactive Card):** `surface-container-highest` (#31353c)

### Ambient Shadows & Ghost Borders
*   **Ambient Shadows:** For floating elements, use a 32px blur, 0px offset, with a 6% opacity shadow tinted with the `primary` color (Cyan). 
*   **The Ghost Border:** If high-contrast separation is required (e.g., in a code block), use the `outline-variant` token at **15% opacity**. Never use 100% opaque lines.
*   **Glow Effects:** Interactive cards on hover should emit a 15px outer glow using the `primary` color at 20% opacity to simulate a "terminal screen" luminance.

---

## 5. Components

### Terminal-Style Code Blocks
*   **Background:** `surface_container_lowest` (#0a0e14).
*   **Styling:** No border. Top-left corner features three "window control" dots (Red, Yellow, Green) for the academic notebook aesthetic.
*   **Interaction:** On hover, a "Copy" action appears in the top-right using `glassmorphism` (surface-variant with blur).

### Editorial Cards
*   **Structure:** No dividers. Use `surface_container_high` backgrounds.
*   **Animation:** Cards must enter the viewport using a staggered "Slide & Fade" (Y-offset: 20px, Duration: 400ms, Easing: Cubic-Bezier 0.2, 0.8, 0.2, 1).
*   **Padding:** Generous internal padding (24px to 32px) to provide "breathing room."

### Viva Accordions (Q&A)
*   **Header:** `title-md` (Serif).
*   **Interaction:** Smooth height transition. When expanded, the background of the accordion should shift from `surface-container-low` to `surface-container-high`.
*   **Indicator:** Use a Soft Amber (`secondary`) chevron to highlight the interactive element.

### Buttons & Chips
*   **Primary Button:** Gradient fill (Cyan), 0.25rem (sm) border-radius. No shadow, but a subtle glow on hover.
*   **Chips:** Use `outline-variant` ghost borders (20% opacity) and `label-sm` (Inter) for metadata (e.g., "SQL", "Normalization").

---

## 6. Do's and Don'ts

### Do
*   **Do** use the dot-matrix background pattern (Opacity: 5%) to add texture to empty spaces.
*   **Do** use asymmetrical layouts (e.g., a wide code block next to a narrow sidebar) to feel like a researcher's notebook.
*   **Do** use "Success Green" strictly for query output results to provide immediate dopamine feedback for students.

### Don't
*   **Don't** use pure white (`#FFFFFF`) for text. Use `on_surface_variant` (#bbc9cf) for body text to maintain the dark-mode aesthetic.
*   **Don't** use standard 1px dividers. If you feel you need a line, use a 48px vertical gap instead.
*   **Don't** use sharp, 0px corners. Use the `0.25rem` (sm) or `0.5rem` (lg) scale to maintain a "high-end hardware" feel.

---

## 7. Motion & Interaction
Movement is the connective tissue of this system.
*   **Micro-interactions:** When hovering over a "Practical Group" card, the background should subtly shift towards the group's specific tint (e.g., Group C's Purple tint at 10% opacity).
*   **The Grid Flow:** The background dot-matrix should have a slow, parallax scroll effect (0.1x speed of the foreground) to create a sense of infinite depth.
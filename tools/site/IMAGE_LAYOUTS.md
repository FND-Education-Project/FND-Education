# Three approved illustration layouts

Course authors can choose **one** of three responsive illustration commands. No inline CSS, extra width options, or new site-builder parsing rules are required.

Use an ordinary Markdown image and a caption inside a semantic HTML `<figure>` wrapper. The `markdown="1"` attribute tells Kramdown to process the nested Markdown image normally.

```markdown
<figure class="image-60left" markdown="1">

![Describe the illustration for screen-reader users](../../../assets/images/example.png)

<figcaption>A short caption explaining the illustration.</figcaption>

</figure>
```

Choose exactly one class:

| Class | Desktop | Mobile (up to 48rem) |
|---|---|---|
| `image-60left` | Figure occupies 60% of content width, floated left; following text wraps on the right. | Full width, no text wrap. |
| `image-60right` | Figure occupies 60% of content width, floated right; following text wraps on the left. | Full width, no text wrap. |
| `image-60center` | Figure occupies 60% of content width and is centered; **no text wraps alongside it**. | Full width, no text wrap. |

The entire figure—including its caption—is positioned, rather than floating the image alone. The responsive rules are in `web/assets/css/site.css`. Subsequent headings clear floated figures to prevent them from spilling into the next section; printers use centered, non-floating figures.

A floated figure should normally be inserted **just after a heading**, before the paragraph text that will wrap around it. If the graphic is dense (a multi-panel scene or labelled diagram), use `image-60center`.

These classes are optional. Existing Markdown images without a figure wrapper continue to use the site's default full-width responsive styling.

## Module 1 choices

- Lesson 1: both the nervous-system diagram and the three-part supporter illustration use `image-60center` so neither diagram shares horizontal space with text.
- Lesson 2: the biopsychosocial brain illustration uses `image-60right` within the discussion of influences.
- Lesson 3: the four-part recovery illustration uses `image-60center` for better detail.
- Lesson 4: the available-capacity bucket uses `image-60left` in the discussion of restoring capacity.

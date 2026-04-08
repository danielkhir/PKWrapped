import textwrap

HideFSButton = """
<style>
div[data-testid="stElementToolbar"] {
display: none !important;
}
</style>
"""


def SpriteMarquee(urls: list[str]):
    width = 64
    gap = 20
    total_move = (width + gap) * len(urls)

    return textwrap.dedent(f"""
<div class="marquee-viewport">
    <div class="marquee-content">
        {"".join([f'<img src="{url}" class="marquee-item">' for url in urls * 2])}
    </div>
</div>

<style>
body {{ margin: 0; padding: 0; overflow: hidden; background-color: transparent; }}

.marquee-viewport {{
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    padding: 10px 0;
}}

.marquee-content {{
    display: flex;
    gap: {gap}px;
    width: max-content;
    animation: scroll 40s linear infinite;
}}

.marquee-content:hover {{
    animation-play-state: paused;
}}

.marquee-item {{
    width: {width}px;
    height: {width}px;
    object-fit: contain;
}}

@keyframes scroll {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-{total_move}px); }}
}}
</style>
    """)


def SpriteRow(images: list[tuple[str, str, str]]):
    figures = ""
    for i in images:
        figures += textwrap.dedent(f"""
        <figure class="sprite-card">
            <img src="{i[0]}" alt="{i[1]}">
            <figcaption>{i[1]}<br>{i[2]}</figcaption>
        </figure>
        """)

    return textwrap.dedent(f"""
<style>
.sprite-row {{
    display: flex;
    // justify-content: center;
    gap: 20px;
    font-family: 'Source Sans Pro', sans-serif;
}}

.sprite-card {{
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80px;
}}

.sprite-card img {{
    width: 64px;
    height: 64px;
    object-fit: contain;
    padding: 4px;
}}

.sprite-card figcaption {{
    margin-top: 8px;
    font-size: 14px;
    font-weight: 600;
    color: white;
    text-align: center;
}}
</style>
<div class="sprite-row">
    {figures}
</div>
    """)

from dash import html

import colors
import styles

STRATEGY_BAR_MAX_WIDTH = 160
STRATEGY_BAR_MIN_PROBABILITY = 0.001


def segmented_control(buttons, active_id, margin_bottom=None):
    return html.Div(
        style=styles.segmented_group_style(margin_bottom),
        children=[
            html.Button(
                label,
                id=btn_id,
                style=styles.BTN_ACTIVE if btn_id == active_id else styles.BTN_INACTIVE,
            )
            for btn_id, label in buttons
        ],
    )


def win_probability_row(value: float) -> html.Div:
    return html.Div(
        f"P1 wins: {value * 100:.1f}%",
        style={"color": colors.MUTED, "fontSize": styles.FONT_SIZE, "marginBottom": "12px"},
    )


def strategy_panel(title: str, color: str, strategy, margin_top: str = "0") -> list:
    return [
        html.Div(
            title,
            style={
                "color": color,
                "fontSize": styles.FONT_SIZE,
                "fontWeight": "600",
                "marginTop": margin_top,
                "marginBottom": "4px",
            },
        ),
        *strategy_bars(strategy, color),
    ]


def strategy_bars(strategy, color: str) -> list:
    entries = [
        (bid, probability)
        for bid, probability in enumerate(strategy)
        if probability > STRATEGY_BAR_MIN_PROBABILITY
    ]
    if not entries:
        return [html.Span("-", style={"color": colors.MUTED_DARK})]
    return [_strategy_bar(bid, probability, color) for bid, probability in entries]


def _strategy_bar(bid: int, probability: float, color: str) -> html.Div:
    return html.Div(
        style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "6px"},
        children=[
            html.Div(
                style={
                    "width": f"{probability * STRATEGY_BAR_MAX_WIDTH:.0f}px",
                    "height": "30px",
                    "backgroundColor": color,
                    "borderRadius": "6px",
                    "minWidth": "6px",
                }
            ),
            html.Span(
                f"bid {bid}: {probability * 100:.2f}%",
                style={"color": colors.MUTED, "fontSize": styles.FONT_SIZE},
            ),
        ],
    )

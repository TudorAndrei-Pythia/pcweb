"""UI and logic for the navbar component."""

import reflex as rx

from pcweb import constants, styles
from pcweb.base_state import State
from pcweb.components.logo import navbar_logo
from pcweb.components.sidebar import sidebar as sb
from pcweb.pages.docs.gallery import gallery
from pcweb.pages.docs.resources import resources
from pcweb.pages.docs.getting_started import introduction
from pcweb.pages.index import index
from typing import Optional

try:
    from pcweb.tsclient import client
except ImportError:
    client = None


class NavMenu(rx.Component):
    library = "@radix-ui/react-navigation-menu"
    tag = "NavigationMenu"

    @classmethod
    def get_alias(cls) -> Optional[str]:
        return "*"


class NavbarState(State):
    """The state for the navbar component."""

    # Whether the sidebar is open.
    sidebar_open: bool = False

    search_modal: bool = False

    search_input: str = ""

    enter: bool = False

    def change_search(self):
        self.search_modal = not (self.search_modal)

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.var
    def search_results(self) -> list[dict[str, dict[str, str]]]:
        """Get the search results."""
        if client is None or self.search_input == "":
            return []
        search_parameters = {
            "q": self.search_input,
            "query_by": "heading, description",
            "query_by_weights": "2,1",
            "sort_by": "_text_match:desc",
        }
        return client.collections["search-auto"].documents.search(search_parameters)[
            "hits"
        ]


def format_search_results(result):
    return rx.vstack(
        rx.link(
            rx.text(
                result["document"]["heading"],
                font_weight=600,
                color="#1F1944",
            ),
            rx.divider(),
            rx.text(
                result["document"]["description"],
                font_weight=400,
                color="#696287",
            ),
            on_click=NavbarState.change_search,
            href=result["document"]["href"],
        ),
        bg="#FAF8FB",
        border_radius="8px",
        align_items="start",
        padding="0.5em",
        shadow=styles.DOC_SHADOW_LIGHT,
        _hover={"background_color": "#F5EFFE", "color": "#5646ED"},
        width="100%",
    )


# Styles to use for the navbar.
logo_style = {
    "height": "1.25em",
}
logo = navbar_logo(**logo_style)


hover_button_style = {
    "_hover": {
        "background": "radial-gradient(82.06% 100% at 50% 100%, rgba(91, 77, 182, 0.04) 0%, rgba(234, 228, 253, 0.2) 100%), #FEFEFF;",
        "box-shadow": "0px 0px 0px 3px rgba(149, 128, 247, 0.6), 0px 2px 3px rgba(3, 3, 11, 0.2), 0px 4px 8px rgba(3, 3, 11, 0.04), 0px 4px 10px -2px rgba(3, 3, 11, 0.02), inset 0px 2px 0px rgba(255, 255, 255, 0.01), inset 0px 0px 0px 1px rgba(32, 17, 126, 0.4), inset 0px -20px 12px -4px rgba(234, 228, 253, 0.36);",
    },
}


def search_bar():
    return rx.hstack(
        rx.fragment(
            rx.icon(tag="search2", style=styles.NAV_SEARCH_STYLE),
            rx.text("Search Docs", style=styles.NAV_SEARCH_STYLE, font_weight=400),
        ),
        rx.spacer(),
        rx.text("/", style=styles.NAV_SEARCH_STYLE),
        on_click=NavbarState.change_search,
        display=["none", "none", "none", "flex", "flex"],
        bg="#FAF8FB",
        min_width="15em",
        padding_x="1em",
        height="2em",
        border_radius="20px",
    )


def search_modal(state: NavbarState):
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_body(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="search2", style=styles.NAV_SEARCH_STYLE),
                            rx.input(
                                placeholder="Search the docs",
                                on_change=NavbarState.set_search_input,
                                focus_border_color="transparent",
                                border_color="transparent",
                            ),
                            width="100%",
                        ),
                        rx.divider(),
                        rx.vstack(
                            rx.foreach(
                                NavbarState.search_results,
                                format_search_results,
                            ),
                            spacing="1em",
                            width="100%",
                            max_height="30em",
                            align_items="start",
                            overflow_y="auto",
                        ),
                    )
                ),
                bg="radial-gradient(82.06% 100% at 50% 100%, rgba(86, 70, 237, 0.12) 0%, rgba(245, 239, 254, 0) 100%), #FFFFFF;",
            )
        ),
        is_open=NavbarState.search_modal,
        on_close=NavbarState.change_search,
        padding_top="1em",
        padding_x="1em",
    )


def github_button():
    return rx.hstack(
        rx.image(src="/github.svg", height="1.25em"),
        rx.text("Star", style=styles.NAV_TEXT_STYLE),
        rx.text(
            "9k+",
            color="#5646ED",
            bg="#F5EFFE",
            padding_x="0.5em",
            border_radius="6px",
            font_weight=600,
        ),
        box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
        padding_x=".5em",
        height="2em",
        border_radius="8px",
        bg="#FFFFFF",
        style=hover_button_style,
    )


def discord_button():
    return rx.center(
        rx.image(src="/icons/discord.svg", height="1.25em"),
        box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
        height="2em",
        width="2em",
        border_radius="8px",
        bg="#FFFFFF",
        style=hover_button_style,
    )


def navbar(sidebar: rx.Component = None) -> rx.Component:
    """Create the navbar component.

    Args:
        sidebar: The sidebar component to use.
    """
    # If the sidebar is not provided, create a default one.
    sidebar = sidebar or sb()

    # Create the navbar component.
    return rx.box(
        rx.hstack(
            rx.hstack(
                logo,
                rx.link(
                    "Docs",
                    href="/docs/getting-started/introduction",
                    style=styles.NAV_TEXT_STYLE,
                ),
                rx.link(
                    "Blog",
                    href="/docs/blog",
                    style=styles.NAV_TEXT_STYLE,
                ),
                rx.popover(
                    rx.popover_trigger(
                        rx.hstack(
                            rx.text("Resources", style=styles.NAV_TEXT_STYLE),
                            rx.icon(tag="chevron_down", style=styles.NAV_TEXT_STYLE),
                        )
                    ),
                    rx.popover_content(
                        rx.grid(
                            rx.grid_item(
                                rx.text("Gallery", style=styles.NAV_TEXT_STYLE),
                                row_span=2,
                                col_span=3,
                                style=styles.NAV_BOX_STYLE,
                            ),
                            rx.grid_item(
                                rx.vstack(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.image(
                                                src="/maps.svg",
                                                height="1.5em",
                                                width="1.5em",
                                            ),
                                            rx.text(
                                                "Roadmap",
                                                style=styles.NAV_TEXT_STYLE,
                                                font_size="1em",
                                            )
                                        ),
                                        rx.text(
                                            "See whats happening with Reflex's open source and hosting.",
                                            font_size="0.75em",
                                        ),
                                        style=styles.NAV_DROPDOWN_STYLE
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.image(
                                                src="/rocket.svg",
                                                height="1.5em",
                                                width="1.5em",
                                            ),
                                            rx.text(
                                                "Contributor Program",
                                                style=styles.NAV_TEXT_STYLE,
                                                font_size="1em",
                                            )
                                        ),
                                        rx.text(
                                            "Get involved in the Reflex community.",
                                            font_size="0.75em",
                                        ),
                                        style=styles.NAV_DROPDOWN_STYLE
                                    ),
                                    margin=".25em",
                                    padding=".25em",
                                ),
                                col_span=5,
                                row_span=2,
                            ),
                            template_rows="repeat(2, 1fr)",
                            template_columns="repeat(8, 1fr)",
                            border_radius="8px",
                            box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
                            bg="#FAF8FB",
                            h="10em",
                            gap=".25em",
                            padding=".5em",
                        ),
                        width="60m",
                        border="transparent",
                    ),
                ),
                spacing="2em",
            ),
            rx.hstack(
                search_bar(),
                github_button(),
                discord_button(),
                height="full",
            ),
            search_modal(NavbarState),
            justify="space-between",
            padding_x=styles.PADDING_X,
        ),
        bg="rgba(255,255,255, 0.9)",
        backdrop_filter="blur(10px)",
        padding_y=["0.8em", "0.8em", "0.5em"],
        border_bottom="2px solid #F4F3F6",
        position="sticky",
        width="100%",
        top="0px",
        z_index="999",
    )

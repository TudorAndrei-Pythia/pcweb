import reflex as rx
from pcweb import constants, styles
from pcweb.base_state import State
import openai
import os

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except Exception as e:
    print("OPENAI_API_KEY environment variable not set.")


def tag(text):
    return rx.text(
        text,
        color="#5646ED",
        bg="#F5EFFE",
        padding_x="0.5em",
        padding_y="0.25em",
        border_radius="8px",
        font_weight=600,
    )


class GptState(State):
    question: str = "What is the best way to learn Python?"
    answer: str = "The best way to learn Python is to learn Python."
    limit = 0

    def get_answer(self):
        if self.limit > 2:
            print("Limit Reached")
            return rx.window_alert("Limit Reached")
        self.limit += 1
        try:
            session = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.question,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.7,
                stream=True,  # Enable streaming
            )
            self.answer = ""
            yield
            # Stream the results, yielding after every word.
            for item in session:
                answer_text = item["choices"][0]["text"]
                self.answer += answer_text
                yield
        except Exception as e:
            print(e)
            self.answer = "Error OpenAI API Key not set"
            yield


def qa():
    return rx.vstack(
        rx.text(
            GptState.question,
            font_family=styles.MONO,
            margin_top=".5em",
            padding="1em",
            font_weight="500",
            font_size="11px",
            border_top="1px solid #EAE4FD",
        ),
        rx.cond(
            GptState.limit > 2,
            rx.text(
                "Limit Reached",
                bg="white",
                padding="1em",
                border_radius="6px",
                border="1px solid #EAE4FD",
                font_family=styles.MONO,
                font_weight="500",
                font_size="11px",
            ),
            rx.text(
                GptState.answer,
                bg="white",
                padding="1em",
                border_radius="6px",
                border="1px solid #EAE4FD",
                font_family=styles.MONO,
                font_weight="500",
                font_size="11px",
            ),
        ),
        width="100%",
        align_items="left",
        padding_x="1em",
    )


def chat_component():
    return rx.vstack(
        rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Search docs...",
                    on_blur=GptState.set_question,
                    style=styles.INPUT_STYLE,
                ),
                rx.spacer(),
                rx.button(
                    "Get answer",
                    on_click=GptState.get_answer,
                    background="radial-gradient(82.06% 100% at 50% 100%, rgba(91, 77, 182, 0.04) 0%, rgba(234, 228, 253, 0.2) 100%), #FEFEFF;",
                    box_shadow="0px 0px 0px 1px rgba(52, 46, 92, 0.14), 0px 2px 3px rgba(3, 3, 11, 0.1), 0px 4px 8px rgba(3, 3, 11, 0.04), 0px 4px 10px -2px rgba(3, 3, 11, 0.02), inset 0px 2px 0px rgba(255, 255, 255, 0.2), inset 0px 0px 0px 1px rgba(255, 255, 255, 0.32), inset 0px -20px 12px -4px rgba(234, 228, 253, 0.2);",
                    border_radius="8px;",
                    href="/docs",
                    px=8,
                    py=4,
                ),
                width="100%",
                padding_x="1em",
                padding_top="1em",
            ),
            qa(),
            min_height="15em",
            width="100%",
            bg="radial-gradient(82.06% 100% at 50% 100%, rgba(86, 70, 237, 0.06) 0%, rgba(245, 239, 254, 0) 100%), #FFFFFF;",
            border_bottom="2px solid #F4F3F6",
            border_radius="8px 8px 0 0",
        ),
        rx.hstack(
            tag("GPT Demo"),
            rx.link(
                "View code",
                href="https://github.com/pynecone-io/pynecone-chat",
                font_weight="600",
                color="#777583",
            ),
            rx.spacer(),
            rx.hstack(
                rx.text("All examples"),
                rx.icon(tag="arrow_forward", color="#494369"),
                border_radius="6px",
                box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
                px=4,
            ),
            width="100%",
            padding_x="1em",
            padding_bottom=".5em",
        ),
        min_width="10em",
        border="1px solid #F4F3F6;",
        box_shadow="0px 0px 0px 1px rgba(52, 46, 92, 0.12), 0px 2px 3px rgba(3, 3, 11, 0.1), 0px 12px 8px rgba(3, 3, 11, 0.04), 0px 8px 12px -4px rgba(3, 3, 11, 0.02);",
        border_radius="8px;",
        width="100%",
        display=["none", "none", "none", "flex", "flex", "flex"],
    )

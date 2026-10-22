"""Small presentation helpers for the ChessBot study room."""

import streamlit as st


def study_room_styles() -> None:
    """Keep custom styling scoped to the shell and native navigation."""
    st.html("""<style>
      h1 { letter-spacing: -0.045em; }
      h2, h3 { letter-spacing: -0.025em; }
      .st-key-study_header { padding-bottom: .25rem; }
      .st-key-study_header h1 { margin-top: 0; padding-top: 0; }
      .st-key-primary_navigation { margin-bottom: .75rem; }
      .st-key-primary_navigation [role="radiogroup"] {
        display: flex; gap: .35rem; padding: .3rem;
        border: 1px solid #354139; border-radius: .8rem;
        background: #111914; width: fit-content; max-width: 100%;
      }
      .st-key-primary_navigation [data-testid="stRadioOption"] {
        padding: .55rem 1.1rem; margin: 0; border-radius: .55rem;
      }
      .st-key-primary_navigation [data-testid="stRadioOption"][data-selected="true"] {
        background: #314a39; color: #f4f1e8;
      }
      .st-key-primary_navigation [data-testid="stRadioOption"]:focus-within {
        outline: 2px solid #9acb9e; outline-offset: 2px;
      }
      .st-key-primary_navigation [data-testid="stRadioOption"] > div > div:first-child {
        display: none;
      }
      .st-key-welcome_review, .st-key-welcome_primer {
        background: #1b241e;
      }
      .st-key-welcome_primer [data-testid="stImage"] {
        max-width: 260px; margin: .3rem auto .7rem;
      }
      .st-key-study_header [data-testid="stCaptionContainer"] {
        letter-spacing: .12em; font-size: .7rem;
      }
      @media (max-width: 640px) {
        .st-key-primary_navigation [data-testid="stRadioOption"] { padding: .5rem .8rem; }
        .st-key-study_header h1 { font-size: 2.4rem; }
      }
    </style>""")

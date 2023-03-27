import streamlit as st


def header():
    st.header("Awesome")


import pathlib

ROOT_DIR = pathlib.Path(__file__).parents[1]

CONTENT_DIR = ROOT_DIR / "content"
DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "log"

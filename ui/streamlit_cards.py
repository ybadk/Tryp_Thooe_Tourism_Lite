from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

import pandas as pd
import streamlit as st


def _clean_text(value: Any, fallback: str = "Not available", max_length: int = 140) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        text = fallback
    else:
        text = str(value).strip() or fallback
    return text if len(text) <= max_length else f"{text[: max_length - 1]}…"


def _label(name: str) -> str:
    return str(name).replace("_", " ").strip().title()


def dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(len(df.index)),
        "columns": int(len(df.columns)),
        "column_names": [str(col) for col in df.columns.tolist()],
    }


def dataframe_preview_records(
    df: pd.DataFrame,
    limit: int = 6,
    max_columns: int = 6,
    text_limit: int = 100,
) -> list[dict[str, str]]:
    preview_df = df.head(limit).copy()
    columns = [str(col) for col in preview_df.columns[:max_columns]]
    records: list[dict[str, str]] = []
    for _, row in preview_df.iterrows():
        records.append({col: _clean_text(row[col], max_length=text_limit) for col in columns})
    return records


def render_section_header(title: str, subtitle: str | None = None, icon: str | None = None) -> None:
    prefix = f"{icon} " if icon else ""
    st.subheader(f"{prefix}{title}")
    if subtitle:
        st.caption(subtitle)


def render_metric_strip(metrics: Sequence[tuple[str, Any, Any | None]]) -> None:
    columns = st.columns(len(metrics))
    for column, (label, value, delta) in zip(columns, metrics):
        with column:
            column.metric(label, value, delta=delta)


def render_record_cards(
    records: Sequence[Mapping[str, Any]],
    title_key: str,
    description_keys: Sequence[str] | None = None,
    meta_keys: Sequence[str] | None = None,
    badge_key: str | None = None,
    link_key: str | None = None,
    columns_count: int = 2,
    key_prefix: str = "card",
) -> None:
    if not records:
        st.info("No records available.")
        return

    description_keys = description_keys or []
    meta_keys = meta_keys or []
    columns = st.columns(columns_count)

    for index, record in enumerate(records):
        with columns[index % columns_count]:
            with st.container(border=True):
                st.markdown(f"#### {_clean_text(record.get(title_key))}")
                if badge_key and record.get(badge_key):
                    st.caption(_clean_text(record.get(badge_key), max_length=60))

                for meta_key in meta_keys:
                    value = _clean_text(record.get(meta_key), max_length=80)
                    if value != "Not available":
                        st.write(f"**{_label(meta_key)}:** {value}")

                for desc_key in description_keys:
                    value = _clean_text(record.get(desc_key), max_length=180)
                    if value != "Not available":
                        st.write(value)
                        break

                if link_key and record.get(link_key):
                    st.link_button("Open", str(record.get(link_key)))


def render_dataframe_cards(
    name: str,
    df: pd.DataFrame,
    key_prefix: str,
    title_key: str | None = None,
    description_keys: Iterable[str] | None = None,
    meta_keys: Iterable[str] | None = None,
    link_key: str | None = None,
    columns_count: int = 2,
    preview_limit: int = 6,
) -> None:
    summary = dataset_summary(df)
    render_section_header(name, f"{summary['rows']} rows • {summary['columns']} columns")
    st.caption("Columns: " + ", ".join(summary["column_names"][:8]))

    if df.empty:
        st.info("No data available.")
        return

    resolved_title_key = title_key or str(df.columns[0])
    preview_records = dataframe_preview_records(df, limit=preview_limit)
    render_record_cards(
        preview_records,
        title_key=resolved_title_key,
        description_keys=list(description_keys or [str(col) for col in df.columns[1:3]]),
        meta_keys=list(meta_keys or [str(col) for col in df.columns[3:6]]),
        link_key=link_key,
        columns_count=columns_count,
        key_prefix=key_prefix,
    )

    with st.expander(f"More about {name}"):
        st.write({
            "rows": summary["rows"],
            "columns": summary["column_names"],
        })

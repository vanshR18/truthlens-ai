import os
import re
from collections import Counter
from html import unescape

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GNEWS_KEY = os.getenv("GNEWS_API_KEY", "").strip()
FACTCHECK_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY", "").strip()

GNEWS_URL = "https://gnews.io/api/v4/search"
FACTCHECK_URL = (
    "https://factchecktools.googleapis.com/v1alpha1/claims:search"
)

st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🔎",
    layout="wide",
)

# Custom CSS for Modern Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Header Styling */
    .hero-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #f8fafc;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    /* Metric Cards */
    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0.25rem;
    }

    /* Article Card Styling */
    .article-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Publisher Badge */
    .badge-source {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-date {
        color: #64748b;
        font-size: 0.8rem;
        margin-left: 8px;
    }
    
    /* Fact Check Badge */
    .rating-badge {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }

    /* General Cleanups */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre;
        background-color: #f8fafc;
        border-radius: 8px;
        color: #475569;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def clean_text(text):
    """Remove HTML tags and normalize article text."""
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def summarize(text, max_sentences=3):
    """Extractive summarizer selecting key sentences."""
    text = clean_text(text)
    if not text:
        return "No article description is available to summarize."

    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) >= 5]

    if len(sentences) <= max_sentences:
        return " ".join(sentences) if sentences else text

    stopwords = set("""
        the a an and or but is are was were be been being to of in on
        for with by from at as it its this that these those he she they
        them their his her we you i has have had will would can could
        may might about after before into over under than then also
    """.split())

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    frequencies = Counter(word for word in words if word not in stopwords)

    scored = []
    for index, sentence in enumerate(sentences):
        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        score = sum(frequencies[word] for word in tokens if word not in stopwords)
        score = score / max(len(tokens), 1)
        scored.append((score, index, sentence))

    selected = sorted(
        sorted(scored, reverse=True)[:max_sentences],
        key=lambda item: item[1],
    )
    return " ".join(item[2] for item in selected)


@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(topic, api_key):
    params = {
        "q": topic,
        "lang": "en",
        "country": "in",
        "max": 10,
        "sortby": "relevance",
        "apikey": api_key,
    }
    response = requests.get(GNEWS_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("articles", [])


@st.cache_data(ttl=600, show_spinner=False)
def fetch_factchecks(topic, api_key):
    params = {
        "query": topic,
        "languageCode": "en",
        "pageSize": 10,
        "key": api_key,
    }
    response = requests.get(FACTCHECK_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("claims", [])


def show_factchecks(claims):
    if not claims:
        st.info("ℹ️ No matching fact-checks were returned for this specific topic.")
        return

    st.caption("Existing fact-checks related to your search. Check that each review refers to the exact claim.")
    st.write("")

    for claim in claims:
        claim_text = clean_text(claim.get("text", "Claim"))
        claimant = claim.get("claimant", "Claimant not specified")

        with st.container(border=True):
            st.markdown(f"#### 💬 Claim: \"{claim_text}\"")
            st.caption(f"**Claimant:** {claimant}")
            st.divider()

            reviews = claim.get("claimReview", [])
            if not reviews:
                st.write("No review details were provided.")
                continue

            for review in reviews:
                publisher = review.get("publisher", {}).get("name", "Fact-check publisher")
                title = clean_text(review.get("title", "Read review"))
                rating = review.get("textualRating", "Rating not provided")
                url = review.get("url", "")

                col_rev1, col_rev2 = st.columns([3, 1])
                with col_rev1:
                    st.markdown(f"<span class='rating-badge'>Rating: {rating}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Reviewer:** {publisher}")
                    st.write(f"*{title}*")
                with col_rev2:
                    if url.startswith(("https://", "http://")):
                        st.link_button("Read Review 🔗", url, use_container_width=True)


# Sidebar Configuration
with st.sidebar:
    st.title("🔎 TruthLens AI")
    st.caption("AI-Powered News Summarizer & Fact Checker")
    st.markdown("---")
    
    st.markdown("### 🛠️ How It Works")
    st.markdown("""
    1. **Search**: Enter any trending topic or query.
    2. **Aggregate**: Collects news articles from GNews API.
    3. **Summarize**: Uses NLP logic to summarize key facts.
    4. **Verify**: Queries Google FactCheck API for verification.
    """)
    st.markdown("---")
    st.caption("💡 *Educational Prototype v1.0*")


# Hero Banner
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🔎 TruthLens AI</div>
    <div class="hero-subtitle">Understand the news. Investigate claims with automated summaries and multi-source verification.</div>
</div>
""", unsafe_allow_html=True)

# Search Bar Form
with st.form("search_form"):
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        topic = st.text_input(
            "Search Query",
            value="India space mission",
            placeholder="e.g. Chandrayaan mission, Economic policy...",
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("🔍 Search", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a search topic.")
        st.stop()

    if not GNEWS_KEY:
        st.error("GNews API key missing! Add `GNEWS_API_KEY` to your `.env` file.")
        st.stop()

    with st.spinner("Fetching news articles..."):
        try:
            articles = fetch_news(topic.strip(), GNEWS_KEY)
        except requests.RequestException as exc:
            st.error("Could not fetch news. Check your connection or API key.")
            st.caption(str(exc))
            st.stop()
        except (ValueError, KeyError) as exc:
            st.error(f"Could not parse news response: {exc}")
            st.stop()

    st.session_state["articles"] = articles
    st.session_state["topic"] = topic.strip()
    st.session_state["claims"] = None

# Results Section
if "articles" in st.session_state:
    topic = st.session_state["topic"]
    articles = st.session_state["articles"]

    st.markdown(f"### Results for: **{topic}**")

    # Metric Cards Layout
    m1, m2, m3 = st.columns(3)
    publishers_count = len({
        a.get("source", {}).get("name", "")
        for a in articles if a.get("source", {}).get("name")
    })
    
    with m1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Articles Found</div>
            <div class="kpi-value">{len(articles)}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Unique Sources</div>
            <div class="kpi-value">{publishers_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        status_text = "Connected" if FACTCHECK_KEY else "Not Configured"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Fact-Check API</div>
            <div class="kpi-value" style="font-size: 1.3rem; margin-top: 0.6rem;">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Navigation Tabs
    news_tab, fact_tab, about_tab = st.tabs([
        "📰 News & Summaries",
        "🛡️ Fact Checks",
        "ℹ️ Insights & Info"
    ])

    with news_tab:
        if not articles:
            st.warning("No articles found. Try a broader search keyword.")

        for index, article in enumerate(articles, start=1):
            title = clean_text(article.get("title", "Untitled article"))
            description = clean_text(article.get("description", ""))
            content = clean_text(article.get("content", ""))
            source = article.get("source", {}).get("name", "Unknown publisher")
            published = article.get("publishedAt", "")[:10]  # Format date standard
            url = article.get("url", "")
            image_url = article.get("image", "")

            text_to_summarize = content or description or title
            summary = summarize(text_to_summarize)

            with st.container(border=True):
                # Side-by-side layout for images & text
                col_img, col_txt = st.columns([1, 2.5]) if image_url.startswith("https://") else (None, st.container())

                if col_img:
                    with col_img:
                        st.image(image_url, use_container_width=True)

                with col_txt:
                    st.markdown(f"#### {index}. {title}")
                    st.markdown(
                        f"<span class='badge-source'>{source}</span><span class='badge-date'>📅 {published}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"**Key Summary:** {summary}")

                    if url.startswith(("https://", "http://")):
                        st.link_button("Read Original Article ↗", url)

    with fact_tab:
        st.markdown("### 🛡️ Claim Verification")

        if not FACTCHECK_KEY:
            st.warning("Add `GOOGLE_FACTCHECK_API_KEY` to `.env` to enable Google Fact Check lookup.")
        else:
            if st.button("🔎 Fetch Related Fact-Checks", type="primary"):
                with st.spinner("Searching fact-check databases..."):
                    try:
                        claims = fetch_factchecks(topic, FACTCHECK_KEY)
                        st.session_state["claims"] = claims
                    except requests.RequestException as exc:
                        st.error("Fact-check search failed. Check key validity.")
                        st.caption(str(exc))
                    except (ValueError, KeyError) as exc:
                        st.error(f"Error parsing response: {exc}")

            claims = st.session_state.get("claims")
            if claims is not None:
                show_factchecks(claims)
            else:
                st.info("Click the button above to cross-reference this topic with fact-checking databases.")

    with about_tab:
        st.markdown("### How to Interpret TruthLens Results")
        st.markdown("""
        * **News Aggregation:** Articles are sourced dynamically via GNews API based on relevance and recency.
        * **Extractive Summarization:** Summaries select key sentences based on word frequency scoring without using generative halluncinations.
        * **Fact-Check Database:** Pulls directly from publisher reviews in Google Fact Check tools.
        * **No Match Result:** A missing fact-check does not verify or disprove a claim—it simply means independent checkers have not indexed a review for those exact terms yet.
        """)
        st.warning("⚠️ **Note:** TruthLens is an educational decision-support tool. Always consult primary original sources.")

else:
    st.info("👆 Enter a news topic above to fetch summaries and claim reviews.")

st.markdown("---")
st.caption("TruthLens AI • Educational Prototype • News and Fact Check data belong to their respective API providers.")
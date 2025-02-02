#modules/agents.py


import json
import openai
import streamlit as st
import requests
import concurrent.futures
import time

def fetch_serper_context(query: str, start_date: str, end_date: str) -> str:
    """Optional: Use Serper API for additional context if needed."""
    headers = {
        "X-API-KEY": st.secrets["SERPER_API_KEY"],
        "Content-Type": "application/json"
    }
    data = {
        "q": query,
        "gl": "us",
        "hl": "en",
        "time": f"{start_date}..{end_date}"  # Include the date range in the query
    }
    try:
        response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
        response.raise_for_status()
        results = response.json()
        snippets = []
        if 'organic' in results:
            for item in results['organic']:
                if 'snippet' in item:
                    snippets.append(item['snippet'])
        return " ".join(snippets[:3])  # Take a few snippets
    except Exception as e:
        st.error(f"Serper API Error: {e}")
        return ""

def trim_data(data: str, max_tokens: int = 4000) -> str:
    """Trim the input data to fit within the max_tokens limit."""
    words = data.split()
    trimmed_data = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + 1 > max_tokens:
            break
        trimmed_data.append(word)
        current_length += word_length + 1

    return " ".join(trimmed_data)

def get_expert_response(prompt: str, role: str, attempts: int = 3):
    for attempt in range(attempts):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0
            )
            return response.choices[0].message.content
        except openai.error.RateLimitError as e:
            if attempt < attempts - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                st.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
        except Exception as e:
            raise e

def run_expert_agent(
    # twitter_data_json: str,
    # google_trends_data_json: str,
    # gdelt_data_json: str,
    acaps_data_json: str = None,
    serper_data_json: str = None,
    start_date: str = None,
    end_date: str = None
):
    # serper_context = ""
    # if serper_data_json and start_date and end_date:
    #     serper_context = fetch_serper_context(serper_data_json, start_date, end_date)

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Trim Google Trends data to fit within token limit
    # max_tokens_for_google_trends = 3000  # Adjust this value as needed
    # google_trends_data_json = trim_data(google_trends_data_json, max_tokens_for_google_trends)

    # Expert 1: Twitter Analyst
    # twitter_prompt = f"""
    # You are a Twitter analyst expert. Analyze the following Twitter data and provide your reasoning and assessment. Include Tweet links as sources in your response.

    # Twitter Data: {twitter_data_json}
    # """

    # Expert 2: Google Trends Analyst
    # google_trends_prompt = f"""
    # You are a Google Trends analyst. Analyze the following Google Trends data. Include links to the supporting sources for your analysis.

    # Google Trends Data: {google_trends_data_json}
    # """

    # Expert 3: GDELT Analyst
    # gdelt_prompt = f"""
    # You are a GDELT analyst. Analyze the following GDELT data. Include links to the supporting sources for your analysis.

    # GDELT Data: {gdelt_data_json}
    # """

    #Expert 4: Serper Search Analyst
    if serper_data_json is not None:
        serper_prompt = f"""
        You are a Serper search analyst. Analyze the following Serper search context. Include links to the supporting sources for your analysis.

        # Serper Search Context: {serper_data_json}
        # """

    # Expert 5: ACAPS Risk List Data Analyst
    if acaps_data_json is not None:
        acaps_prompt = f"""
        You are an ACAPS Risk List data analyst. Analyze the following historical data from the ACAPS Risk List context and provide your opinion based on whether similar events have materialized in the past. Include references to the historical data.

        ACAPS Data: {acaps_data_json}
        """

    expert_responses = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_expert = {}
            # executor.submit(get_expert_response, twitter_prompt, "You are a Twitter analyst expert. Include Tweet links as sources in your response."): "Expert (Twitter)",
            # executor.submit(get_expert_response, google_trends_prompt, "You are a Google Trends analyst. Include links to the supporting sources for your analysis."): "Expert (Google Trends)",
            # executor.submit(get_expert_response, gdelt_prompt, "You are a GDELT analyst. Include links to the supporting sources for your analysis."): "Expert (GDELT)",
        if serper_data_json is not None:
            future_to_expert[executor.submit(get_expert_response, serper_prompt, "You are a Serper search analyst. Include links to the supporting sources in your response.")] = "Expert (Serper)"

        if acaps_data_json is not None:
            future_to_expert[executor.submit(get_expert_response, acaps_prompt, "You are an ACAPS Risk List data analyst. Include references to the historical data in your response.")] = "Expert (ACAPS Historical Data)"

        for future in concurrent.futures.as_completed(future_to_expert):
            expert = future_to_expert[future]
            try:
                response = future.result()
                expert_responses[expert] = response
                st.markdown(f"<h2 style='color: blue; text-decoration: underline;'>{expert}</h2>", unsafe_allow_html=True)
                st.markdown(response.replace("http", "<span style='color: blue;'>http"), unsafe_allow_html=True)
            except Exception as exc:
                st.error(f"{expert} generated an exception: {exc}")

    # Proceed only if there are valid expert responses
    if not expert_responses:
        st.warning("No expert responses available. Unable to proceed with the final judgment.")
        return {"expert_responses": {}, "judge_content": ""}


    # Final Judge: Make a prediction using ACAPS Risk List format
    judge_prompt = f"""
    You are the final judge. Based on the analyses provided by the experts, make a prediction using the ACAPS Risk List format.

    Expert (Twitter): {expert_responses.get("Expert (Twitter)", "")}
    Expert (Google Trends): {expert_responses.get("Expert (Google Trends)", "")}
    Expert (GDELT): {expert_responses.get("Expert (GDELT)", "")}
    Expert (Serper): {expert_responses.get("Expert (Serper)", "")}
    Expert (ACAPS Historical Data): {expert_responses.get("Expert (ACAPS Historical Data)", "")}

    Predict:
    - Impact: ?
    - Probability: ?
    - Risk Level: ?
    - Status: ?
    """
    judge_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are the final judge making a prediction using the ACAPS Risk List format."},
            {"role": "user", "content": judge_prompt}
        ],
        max_tokens=1000,
        temperature=0
    )
    judge_content = judge_response.choices[0].message.content

    # Display the judge's response only once
    st.markdown("<h2 style='color: blue; text-decoration: underline;'>Judge (Final Opinion)</h2>", unsafe_allow_html=True)
    st.markdown(judge_content.replace("http", "<span style='color: blue;'>http"), unsafe_allow_html=True)

    return {
        "expert_responses": expert_responses,
        "judge_content": judge_content
    }

